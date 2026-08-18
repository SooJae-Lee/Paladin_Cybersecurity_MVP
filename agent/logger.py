"""
실행 로그 기록
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import os


@dataclass
class LogEntry:
    step: int
    type: str                  # "user", "system", "tool_call", "tool_result", "assistant", "injection"
    content: Any
    tool_name: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AgentLogger:
    def __init__(self, run_id: str, log_dir: str = "logs"):
        self.run_id = run_id
        self.log_dir = log_dir
        self.entries: List[LogEntry] = []
        self.step = 0

        os.makedirs(log_dir, exist_ok=True)

    def log(self, type: str, content: Any, tool_name: Optional[str] = None):
        self.step += 1
        entry = LogEntry(
            step=self.step,
            type=type,
            content=content,
            tool_name=tool_name,
        )
        self.entries.append(entry)
        return entry

    def save(self):
        path = os.path.join(self.log_dir, f"{self.run_id}.json")
        data = {
            "run_id": self.run_id,
            "entries": [asdict(e) for e in self.entries],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def get_entries(self) -> List[Dict]:
        return [asdict(e) for e in self.entries]