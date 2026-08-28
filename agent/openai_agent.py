"""
OpenAI tool-calling agent
"""

from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional

from tools.base import ToolRegistry, ToolResult
from agent.logger import AgentLogger
from injection.channels import inject_into_tool_output


try:
    from openai import OpenAI
except ImportError as e:
    raise ImportError("pip install openai") from e


def registry_to_openai_tools(registry: ToolRegistry) -> List[Dict[str, Any]]:
    tools = []
    for item in registry.list_tools():
        tools.append({
            "type": "function",
            "function": {
                "name": item["name"],
                "description": item.get("description") or item["name"],
                "parameters": item.get("parameters") or {"type": "object", "properties": {}},
            },
        })
    return tools


class OpenAIAgent:
    def __init__(
        self,
        registry: ToolRegistry,
        system_prompt: str = "You are a helpful assistant that uses tools to solve tasks.",
        logger: Optional[AgentLogger] = None,
        injection_config: Optional[Dict[str, Any]] = None,
        model: str = "gpt-4o-mini",
        max_tokens: int = 1024,
        max_steps: int = 5,
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY 환경변수가 없습니다.")
        self.client = OpenAI(api_key=api_key)
        self.registry = registry
        self.system_prompt = system_prompt
        self.logger = logger
        self.injection_config = injection_config or {}
        self.model = model
        self.max_tokens = max_tokens
        self.max_steps = max_steps
        self.tools = registry_to_openai_tools(registry)

    def _log(self, type: str, content: Any, tool_name: str = None):
        if self.logger:
            self.logger.log(type=type, content=content, tool_name=tool_name)

    def _execute_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        self._log("tool_call", {"name": name, "arguments": arguments}, tool_name=name)
        result = self.registry.run(name, **(arguments or {}))
        cfg = self.injection_config
        if cfg.get("channel") == "tool_output" and isinstance(result, ToolResult):
            target = cfg.get("tool_name")
            if not target or target == name:
                result = inject_into_tool_output(result, cfg.get("payload") or "")
        if cfg.get("channel") == "retrieved_document" and name in ("search_documents", "get_document_content"):
            if isinstance(result, ToolResult):
                result = inject_into_tool_output(result, cfg.get("payload") or "")
        self._log("tool_result", result.to_dict() if hasattr(result, "to_dict") else str(result), tool_name=name)
        if hasattr(result, "to_string"):
            return result.to_string()
        return json.dumps(result, ensure_ascii=False)

    def run(self, user_message: str, max_steps: int = None) -> str:
        self._log("system", self.system_prompt)
        self._log("user", user_message)

        system = self.system_prompt
        if self.injection_config.get("channel") == "system_message":
            system = system + "\n\n" + (self.injection_config.get("payload") or "")

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ]
        final_text = ""
        steps = max_steps or self.max_steps

        for _ in range(steps):
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools or None,
                max_tokens=self.max_tokens,
            )
            msg = resp.choices[0].message
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in (msg.tool_calls or [])
                ] if msg.tool_calls else None,
            })
            if msg.content:
                final_text = msg.content
            if not msg.tool_calls:
                break

            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments or "{}")
                content = self._execute_tool(tc.function.name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": content,
                })

            if self.injection_config.get("channel") == "intermediate_message":
                messages.append({
                    "role": "user",
                    "content": self.injection_config.get("payload") or "",
                })

        self._log("assistant", final_text)
        return final_text or "[No response]"
