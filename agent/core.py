"""
간단한 Agent 코어 (Week 1용)
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from tools.base import ToolRegistry, ToolResult
from agent.logger import AgentLogger


class Agent:
    def __init__(
        self,
        registry: ToolRegistry,
        system_prompt: str = "You are a helpful assistant that uses tools to solve tasks.",
        logger: Optional[AgentLogger] = None,
    ):
        self.registry = registry
        self.system_prompt = system_prompt
        self.logger = logger
        self.history: List[Dict[str, Any]] = []

    def _log(self, type: str, content: Any, tool_name: str = None):
        if self.logger:
            self.logger.log(type=type, content=content, tool_name=tool_name)

    def call_tool(self, name: str, **kwargs) -> ToolResult:
        self._log("tool_call", {"name": name, "arguments": kwargs}, tool_name=name)
        result = self.registry.run(name, **kwargs)
        self._log("tool_result", result.to_dict(), tool_name=name)
        return result

    def run(self, user_message: str, max_steps: int = 5) -> str:
        """
        매우 단순한 실행 (Week 1용)
        나중에 실제 LLM으로 교체 가능
        """
        self._log("system", self.system_prompt)
        self._log("user", user_message)

        response = f"[Agent received] {user_message}"
        self._log("assistant", response)
        return response