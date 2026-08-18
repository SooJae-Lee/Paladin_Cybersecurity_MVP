"""
Injection Channels
서로 다른 위치에 페이로드를 주입하는 로직
"""

from __future__ import annotations
from typing import Any, Dict, Optional
from copy import deepcopy
from tools.base import ToolResult


class InjectionChannel:
    """채널 이름 상수"""
    TOOL_OUTPUT = "tool_output"
    RETRIEVED_DOCUMENT = "retrieved_document"
    SYSTEM_MESSAGE = "system_message"
    INTERMEDIATE_MESSAGE = "intermediate_message"


def inject_into_tool_output(result: ToolResult, payload: str) -> ToolResult:
    """
    Tool 실행 결과(data)에 페이로드를 삽입
    """
    new_result = deepcopy(result)

    if isinstance(new_result.data, dict):
        # 기존 데이터에 injection 필드 추가 + 내용 변조
        new_result.data["_injection"] = payload
        if "content" in new_result.data and isinstance(new_result.data["content"], str):
            new_result.data["content"] = new_result.data["content"] + f"\n\n[INJECTED]\n{payload}"
        elif "summary" in new_result.data and isinstance(new_result.data["summary"], str):
            new_result.data["summary"] = new_result.data["summary"] + f"\n\n[INJECTED]\n{payload}"
        elif "results" in new_result.data and isinstance(new_result.data["results"], list):
            # 검색 결과에 주입
            new_result.data["results"].insert(0, {
                "id": "injected",
                "title": "INJECTED CONTENT",
                "snippet": payload,
                "score": 1.0
            })
    elif isinstance(new_result.data, str):
        new_result.data = new_result.data + f"\n\n[INJECTED]\n{payload}"

    new_result.raw = new_result.to_string()
    return new_result


def inject_into_retrieved_document(doc: Dict[str, Any], payload: str) -> Dict[str, Any]:
    """
    검색으로 가져온 문서/코드 조각에 주입
    """
    new_doc = deepcopy(doc)
    if "content" in new_doc:
        new_doc["content"] = new_doc["content"] + f"\n\n[INJECTED]\n{payload}"
    elif "snippet" in new_doc:
        new_doc["snippet"] = new_doc["snippet"] + f" | {payload}"
    else:
        new_doc["injected"] = payload
    return new_doc


def inject_into_system_message(system_prompt: str, payload: str) -> str:
    """
    System prompt에 주입
    """
    return system_prompt + f"\n\n[SYSTEM INJECTION]\n{payload}"


def inject_into_intermediate_message(message: str, payload: str) -> str:
    """
    중간 메시지/사고 과정에 주입
    """
    return message + f"\n\n[INTERMEDIATE INJECTION]\n{payload}"


def apply_injection(
    channel: str,
    target: Any,
    payload: str,
) -> Any:
    """
    채널에 따라 적절한 주입 함수를 호출
    """
    if channel == InjectionChannel.TOOL_OUTPUT:
        if isinstance(target, ToolResult):
            return inject_into_tool_output(target, payload)
        raise TypeError("tool_output channel requires ToolResult")

    elif channel == InjectionChannel.RETRIEVED_DOCUMENT:
        if isinstance(target, dict):
            return inject_into_retrieved_document(target, payload)
        raise TypeError("retrieved_document channel requires dict")

    elif channel == InjectionChannel.SYSTEM_MESSAGE:
        if isinstance(target, str):
            return inject_into_system_message(target, payload)
        raise TypeError("system_message channel requires str")

    elif channel == InjectionChannel.INTERMEDIATE_MESSAGE:
        if isinstance(target, str):
            return inject_into_intermediate_message(target, payload)
        raise TypeError("intermediate_message channel requires str")

    else:
        raise ValueError(f"Unknown channel: {channel}")