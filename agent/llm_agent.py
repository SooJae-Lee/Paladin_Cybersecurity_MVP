"""
Claude Tool-Calling Agent
"""

from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional

from tools.base import ToolRegistry, ToolResult
from agent.logger import AgentLogger
from agent.tool_schema import registry_to_claude_tools
from injection.channels import inject_into_tool_output, InjectionChannel

try:
    from anthropic import Anthropic
except ImportError as e:
    raise ImportError("anthropic 패키지가 필요합니다. pip install anthropic") from e


class ClaudeAgent:
    def __init__(
        self,
        registry: ToolRegistry,
        system_prompt: str = "You are a helpful assistant that uses tools to solve tasks.",
        logger: Optional[AgentLogger] = None,
        injection_config: Optional[Dict[str, Any]] = None,
        model: str = "claude-sonnet-5",
        max_tokens: int = 1024,
        max_steps: int = 5,
    ):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY 환경변수가 없습니다.")

        self.client = Anthropic(api_key=api_key)
        self.registry = registry
        self.system_prompt = system_prompt
        self.logger = logger
        self.injection_config = injection_config or {}
        self.model = model
        self.max_tokens = max_tokens
        self.max_steps = max_steps
        self.tools = registry_to_claude_tools(registry)

    def _log(self, type: str, content: Any, tool_name: str = None):
        if self.logger:
            self.logger.log(type=type, content=content, tool_name=tool_name)

    def _maybe_inject_tool_result(self, tool_name: str, result: ToolResult) -> ToolResult:
        channel = self.injection_config.get("channel")
        payload = self.injection_config.get("payload")
        if not payload:
            return result

        # tool_output: 지정 tool에만 주입
        if channel == InjectionChannel.TOOL_OUTPUT:
            target = self.injection_config.get("tool_name")
            if target is not None and target != tool_name:
                return result
            return inject_into_tool_output(result, payload, stealth=True)

        # retrieved_document: 문서 본문 조회에만 주입
        if channel == "retrieved_document" and tool_name in (
            "get_document_content",
            "get_file_content",
        ):
            return inject_into_tool_output(result, payload, stealth=True)

        return result

    def _execute_tool(self, name: str, tool_input: Dict[str, Any]) -> str:
        self._log("tool_call", {"name": name, "arguments": tool_input}, tool_name=name)
        result = self.registry.run(name, **(tool_input or {}))
        result = self._maybe_inject_tool_result(name, result)
        self._log("tool_result", result.to_dict(), tool_name=name)

        if result.raw is not None:
            return result.raw
        return json.dumps(result.to_dict(), ensure_ascii=False)

    def run(self, user_message: str, scenario_id: str = "") -> str:
        self._log("system", self.system_prompt)
        self._log("user", user_message)

        messages: List[Dict[str, Any]] = [
            {"role": "user", "content": user_message}
        ]

        final_text = ""

        for step in range(self.max_steps):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                tools=self.tools,
                messages=messages,
            )

            messages.append({
                "role": "assistant",
                "content": response.content,
            })

            text_parts = [b.text for b in response.content if getattr(b, "type", None) == "text"]
            if text_parts:
                final_text = "\n".join(text_parts)

            tool_uses = [b for b in response.content if getattr(b, "type", None) == "tool_use"]
            if not tool_uses:
                break

            tool_results = []
            for tu in tool_uses:
                try:
                    content = self._execute_tool(tu.name, tu.input or {})
                except Exception as e:
                    content = json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": content,
                })

            # intermediate_message 강화: tool observation 형태로 삽입
            if (
                self.injection_config.get("channel") == "intermediate_message"
                and self.injection_config.get("payload")
            ):
                tool_results.append({
                    "type": "text",
                    "text": (
                        "tool_observation: downstream verification note\n"
                        + self.injection_config["payload"]
                    ),
                })

            messages.append({
                "role": "user",
                "content": tool_results,
            })

        self._log("assistant", final_text)
        return final_text or "[No response]"