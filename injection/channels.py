"""
Injection Channels
서로 다른 위치에 페이로드를 주입하는 로직
"""

from __future__ import annotations
from typing import Any, Dict, Optional
from copy import deepcopy
from tools.base import ToolResult


class InjectionChannel:
    TOOL_OUTPUT = "tool_output"
    RETRIEVED_DOCUMENT = "retrieved_document"
    SYSTEM_MESSAGE = "system_message"
    INTERMEDIATE_MESSAGE = "intermediate_message"


def inject_into_tool_output(
    result: ToolResult,
    payload: str,
    stealth: bool = True,
) -> ToolResult:
    """
    Tool 실행 결과에 페이로드 삽입
    stealth=True 이면 표시 없이 본문에 자연 삽입
    """
    new_result = deepcopy(result)

    def mix(text: str) -> str:
        if stealth:
            return text + "\n" + payload
        return text + f"\n\n[INJECTED]\n{payload}"

    if isinstance(new_result.data, dict):
        if not stealth:
            new_result.data["_injection"] = payload

        if "content" in new_result.data and isinstance(new_result.data["content"], str):
            new_result.data["content"] = mix(new_result.data["content"])
        elif "summary" in new_result.data and isinstance(new_result.data["summary"], str):
            new_result.data["summary"] = mix(new_result.data["summary"])
        elif "results" in new_result.data and isinstance(new_result.data["results"], list):
            item = {
                "id": "doc_extra",
                "title": "Q3 보완 메모" if stealth else "INJECTED CONTENT",
                "snippet": payload,
                "score": 0.99 if stealth else 1.0,
            }
            new_result.data["results"].insert(0, item)
        else:
            new_result.data["note"] = payload
    elif isinstance(new_result.data, str):
        new_result.data = mix(new_result.data)

    new_result.raw = new_result.to_string()
    return new_result


def inject_into_retrieved_document(
    doc: Dict[str, Any],
    payload: str,
    stealth: bool = True,
) -> Dict[str, Any]:
    new_doc = deepcopy(doc)

    def mix(text: str) -> str:
        if stealth:
            return text + "\n" + payload
        return text + f"\n\n[INJECTED]\n{payload}"

    if "content" in new_doc and isinstance(new_doc["content"], str):
        new_doc["content"] = mix(new_doc["content"])
    elif "snippet" in new_doc and isinstance(new_doc["snippet"], str):
        new_doc["snippet"] = new_doc["snippet"] + (" " + payload if stealth else f" | {payload}")
    else:
        new_doc["note"] = payload
    return new_doc


def inject_into_system_message(
    system_prompt: str,
    payload: str,
    stealth: bool = True,
) -> str:
    if stealth:
        return system_prompt + "\n\n" + payload
    return system_prompt + f"\n\n[SYSTEM INJECTION]\n{payload}"


def inject_into_intermediate_message(
    message: str,
    payload: str,
    stealth: bool = True,
) -> str:
    if stealth:
        return message + "\n" + payload
    return message + f"\n\n[INTERMEDIATE INJECTION]\n{payload}"


def apply_injection(
    channel: str,
    target: Any,
    payload: str,
    stealth: bool = True,
) -> Any:
    if channel == InjectionChannel.TOOL_OUTPUT:
        if isinstance(target, ToolResult):
            return inject_into_tool_output(target, payload, stealth=stealth)
        raise TypeError("tool_output channel requires ToolResult")
    elif channel == InjectionChannel.RETRIEVED_DOCUMENT:
        if isinstance(target, dict):
            return inject_into_retrieved_document(target, payload, stealth=stealth)
        raise TypeError("retrieved_document channel requires dict")
    elif channel == InjectionChannel.SYSTEM_MESSAGE:
        if isinstance(target, str):
            return inject_into_system_message(target, payload, stealth=stealth)
        raise TypeError("system_message channel requires str")
    elif channel == InjectionChannel.INTERMEDIATE_MESSAGE:
        if isinstance(target, str):
            return inject_into_intermediate_message(target, payload, stealth=stealth)
        raise TypeError("intermediate_message channel requires str")
    else:
        raise ValueError(f"Unknown channel: {channel}")