"""
시나리오 실행기
"""

from __future__ import annotations
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

from tools.base import ToolRegistry
from agent.core import Agent
from agent.logger import AgentLogger


class ScenarioRunner:
    def __init__(self, registry: ToolRegistry, log_dir: str = "logs"):
        self.registry = registry
        self.log_dir = log_dir

    def create_run_id(self, scenario_id: str) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        short = str(uuid.uuid4())[:8]
        return f"{scenario_id}_{ts}_{short}"

    def run(
        self,
        scenario_id: str,
        user_message: str,
        system_prompt: Optional[str] = None,
        injection_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        시나리오 한 번 실행
        - system_message 채널: system prompt에 주입
        - tool_output 채널: Agent.call_tool 시 결과에 주입
        """
        run_id = self.create_run_id(scenario_id)
        logger = AgentLogger(run_id=run_id, log_dir=self.log_dir)

        base_prompt = system_prompt or "You are a helpful assistant."

        # system_message 채널 주입
        if injection_config and injection_config.get("channel") == "system_message":
            payload = injection_config.get("payload", "")
            base_prompt = base_prompt + f"\n\n[SYSTEM INJECTION]\n{payload}"

        agent = Agent(
            registry=self.registry,
            system_prompt=base_prompt,
            logger=logger,
            injection_config=injection_config,
        )

        if injection_config:
            logger.log("injection", injection_config)

        final_response = agent.run(user_message, scenario_id=scenario_id)

        log_path = logger.save()

        return {
            "run_id": run_id,
            "scenario_id": scenario_id,
            "final_response": final_response,
            "log_path": log_path,
            "entries": logger.get_entries(),
            "injection_config": injection_config,
        }