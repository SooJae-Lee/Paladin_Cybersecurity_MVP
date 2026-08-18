"""
Tool base system
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import json


@dataclass
class ToolResult:
    success: bool
    data: Any
    error: Optional[str] = None
    raw: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
        }

    def to_string(self) -> str:
        if self.raw is not None:
            return self.raw
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    func: Callable[..., ToolResult]
    tags: List[str] = field(default_factory=list)

    def run(self, **kwargs) -> ToolResult:
        try:
            result = self.func(**kwargs)
            if not isinstance(result, ToolResult):
                result = ToolResult(success=True, data=result)
            return result
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
                "tags": t.tags,
            }
            for t in self._tools.values()
        ]

    def run(self, name: str, **kwargs) -> ToolResult:
        tool = self.get(name)
        if tool is None:
            return ToolResult(success=False, data=None, error=f"Unknown tool: {name}")
        return tool.run(**kwargs)

    def names(self) -> List[str]:
        return list(self._tools.keys())


default_registry = ToolRegistry()


def tool(
    name: str,
    description: str,
    parameters: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
):
    def decorator(func: Callable):
        t = Tool(
            name=name,
            description=description,
            parameters=parameters or {},
            func=func,
            tags=tags or [],
        )
        default_registry.register(t)
        return func
    return decorator