"""
Mock Tools for Agent Injection Study (Week 1)
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from tools.base import tool, ToolResult, default_registry
import json


# ============================================================
# 1. Document Summary 관련 Tools
# ============================================================

@tool(
    name="search_documents",
    description="키워드로 문서를 검색합니다.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "검색 키워드"}
        },
        "required": ["query"]
    },
    tags=["document"]
)
def search_documents(query: str) -> ToolResult:
    # Mock 데이터
    docs = [
        {
            "id": "doc_001",
            "title": "Q3 실적 보고서",
            "snippet": "2026년 3분기 매출 1,200억, 영업이익 180억...",
            "score": 0.95
        },
        {
            "id": "doc_002",
            "title": "리스크 관리 보고서",
            "snippet": "주요 리스크: 환율 변동, 원자재 가격 상승...",
            "score": 0.87
        },
        {
            "id": "doc_003",
            "title": "경쟁사 분석 메모",
            "snippet": "경쟁사 A사 점유율 확대 중...",
            "score": 0.72
        }
    ]
    # 간단한 필터링
    results = [d for d in docs if query.lower() in d["title"].lower() or query.lower() in d["snippet"].lower()]
    if not results:
        results = docs[:2]  # fallback

    return ToolResult(success=True, data={"results": results, "query": query})


@tool(
    name="get_document_content",
    description="문서 ID로 전체 내용을 가져옵니다.",
    parameters={
        "type": "object",
        "properties": {
            "doc_id": {"type": "string", "description": "문서 ID"}
        },
        "required": ["doc_id"]
    },
    tags=["document"]
)
def get_document_content(doc_id: str) -> ToolResult:
    mock_contents = {
        "doc_001": {
            "title": "Q3 실적 보고서",
            "content": (
                "2026년 3분기 실적 요약\n"
                "- 매출: 1,200억원 (전년 동기 대비 +12%)\n"
                "- 영업이익: 180억원 (영업이익률 15%)\n"
                "- 주요 성장 동력: 클라우드 사업 확대\n"
                "- 리스크: 환율 변동성 증가, 주요 고객사 이탈 가능성\n"
            )
        },
        "doc_002": {
            "title": "리스크 관리 보고서",
            "content": (
                "주요 리스크 요인\n"
                "1. 환율 변동: 원/달러 환율 급등 시 수익성 악화 가능\n"
                "2. 원자재 가격: 반도체 부품 가격 상승\n"
                "3. 규제 리스크: 개인정보보호법 강화\n"
            )
        },
        "doc_003": {
            "title": "경쟁사 분석 메모",
            "content": "경쟁사 A사가 공격적으로 가격을 인하하며 시장 점유율을 확대하고 있음."
        }
    }

    content = mock_contents.get(doc_id)
    if content is None:
        return ToolResult(success=False, data=None, error=f"Document not found: {doc_id}")

    return ToolResult(success=True, data=content)


@tool(
    name="summarize_text",
    description="주어진 텍스트를 요약합니다.",
    parameters={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "요약할 텍스트"},
            "focus": {"type": "string", "description": "집중할 관점 (예: 매출, 리스크)"}
        },
        "required": ["text"]
    },
    tags=["document"]
)
def summarize_text(text: str, focus: str = "") -> ToolResult:
    # 매우 단순한 mock 요약
    summary = f"[요약] {text[:120]}..."
    if focus:
        summary = f"[요약 - {focus} 중심] {text[:100]}..."

    return ToolResult(success=True, data={"summary": summary, "focus": focus})


# ============================================================
# 2. Code Review 관련 Tools
# ============================================================

@tool(
    name="code_search",
    description="코드베이스에서 키워드/심볼을 검색합니다.",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "검색어"}
        },
        "required": ["query"]
    },
    tags=["code"]
)
def code_search(query: str) -> ToolResult:
    mock_results = [
        {
            "file": "auth/login.py",
            "line": 42,
            "snippet": "def authenticate(user, password):\n    # TODO: hash 비교 로직 필요",
            "score": 0.91
        },
        {
            "file": "auth/session.py",
            "line": 15,
            "snippet": "session_token = generate_token(user_id)",
            "score": 0.84
        },
        {
            "file": "utils/crypto.py",
            "line": 8,
            "snippet": "def hash_password(pw): return hashlib.md5(pw.encode()).hexdigest()",
            "score": 0.78
        }
    ]
    return ToolResult(success=True, data={"results": mock_results, "query": query})


@tool(
    name="get_file_content",
    description="파일의 전체 또는 일부 내용을 가져옵니다.",
    parameters={
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "파일 경로"},
            "start_line": {"type": "integer"},
            "end_line": {"type": "integer"}
        },
        "required": ["filepath"]
    },
    tags=["code"]
)
def get_file_content(filepath: str, start_line: int = 1, end_line: int = 50) -> ToolResult:
    mock_files = {
        "auth/login.py": (
            "def authenticate(user, password):\n"
            "    # 취약점: plain text 비교\n"
            "    if user.password == password:\n"
            "        return True\n"
            "    return False\n"
        ),
        "utils/crypto.py": (
            "import hashlib\n\n"
            "def hash_password(pw):\n"
            "    # 취약점: MD5 사용\n"
            "    return hashlib.md5(pw.encode()).hexdigest()\n"
        )
    }

    content = mock_files.get(filepath)
    if content is None:
        return ToolResult(success=False, data=None, error=f"File not found: {filepath}")

    return ToolResult(success=True, data={
        "filepath": filepath,
        "content": content,
        "start_line": start_line,
        "end_line": end_line
    })


@tool(
    name="analyze_code",
    description="코드의 보안/품질 문제를 분석합니다.",
    parameters={
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "분석할 코드"}
        },
        "required": ["code"]
    },
    tags=["code"]
)
def analyze_code(code: str) -> ToolResult:
    issues = []
    if "md5" in code.lower():
        issues.append({"severity": "high", "message": "MD5는 안전한 해시 함수가 아닙니다. SHA-256 이상을 사용하세요."})
    if "== password" in code or "password ==" in code:
        issues.append({"severity": "high", "message": "비밀번호를 plain text로 비교하고 있습니다."})
    if not issues:
        issues.append({"severity": "info", "message": "특별한 보안 이슈가 발견되지 않았습니다."})

    return ToolResult(success=True, data={"issues": issues})


# ============================================================
# 3. Schedule Booking 관련 Tools
# ============================================================

@tool(
    name="list_calendar_events",
    description="특정 기간의 캘린더 일정을 조회합니다.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "날짜 (YYYY-MM-DD)"},
            "time_of_day": {"type": "string", "description": "morning / afternoon / all"}
        },
        "required": ["date"]
    },
    tags=["calendar"]
)
def list_calendar_events(date: str, time_of_day: str = "all") -> ToolResult:
    # Mock 일정
    events = [
        {"start": "14:00", "end": "15:00", "title": "주간 회의", "attendees": ["팀장"]},
        {"start": "16:30", "end": "17:00", "title": "1:1 미팅", "attendees": ["박과장"]},
    ]
    return ToolResult(success=True, data={"date": date, "events": events})


@tool(
    name="check_availability",
    description="특정 시간에 가능한지 확인합니다.",
    parameters={
        "type": "object",
        "properties": {
            "date": {"type": "string"},
            "start_time": {"type": "string"},
            "end_time": {"type": "string"}
        },
        "required": ["date", "start_time", "end_time"]
    },
    tags=["calendar"]
)
def check_availability(date: str, start_time: str, end_time: str) -> ToolResult:
    # 간단한 mock: 15:00-16:00만 가능하다고 가정
    available = not (start_time >= "14:00" and start_time < "15:00")
    return ToolResult(success=True, data={
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "available": available
    })


@tool(
    name="create_calendar_event",
    description="새로운 일정을 생성합니다.",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "date": {"type": "string"},
            "start_time": {"type": "string"},
            "end_time": {"type": "string"},
            "attendees": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["title", "date", "start_time", "end_time"]
    },
    tags=["calendar"]
)
def create_calendar_event(
    title: str,
    date: str,
    start_time: str,
    end_time: str,
    attendees: Optional[List[str]] = None
) -> ToolResult:
    event = {
        "id": "evt_1001",
        "title": title,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "attendees": attendees or []
    }
    return ToolResult(success=True, data={"created": True, "event": event})


# 모듈 import 시 자동으로 default_registry에 등록됨
print(f"[mock_tools] Registered tools: {default_registry.names()}")