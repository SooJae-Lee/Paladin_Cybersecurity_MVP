"""
ToolRegistry → Claude tool schema 변환
"""

from __future__ import annotations
from typing import Any, Dict, List

from tools.base import ToolRegistry


def to_claude_tool(tool_def: Dict[str, Any]) -> Dict[str, Any]:
    """
    내부 tool dict를 Claude tools 항목으로 변환
    """
    parameters = tool_def.get("parameters") or {
        "type": "object",
        "properties": {},
        "required": [],
    }

    # 방어적으로 JSON schema 최소 형태 보장
    if "type" not in parameters:
        parameters["type"] = "object"
    if "properties" not in parameters:
        parameters["properties"] = {}
    if "required" not in parameters:
        parameters["required"] = []

    return {
        "name": tool_def["name"],
        "description": tool_def.get("description", ""),
        "input_schema": parameters,
    }


def registry_to_claude_tools(registry: ToolRegistry) -> List[Dict[str, Any]]:
    """
    ToolRegistry의 모든 툴을 Claude tools 배열로 변환
    """
    tools = []
    for t in registry.list_tools():
        tools.append(to_claude_tool(t))
    return tools


def find_tool_names(registry: ToolRegistry) -> List[str]:
    return registry.names()


if __name__ == "__main__":
    from tools import mock_tools  # noqa: F401
    from tools.base import default_registry

    claude_tools = registry_to_claude_tools(default_registry)
    print(f"Converted tools: {len(claude_tools)}")
    for t in claude_tools:
        print(f"- {t['name']}: {t['description'][:40]}...")