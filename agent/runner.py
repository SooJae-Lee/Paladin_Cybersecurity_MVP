"""
시나리오 실행기
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional
import uuid

from tools.base import ToolRegistry
from agent.logger import AgentLogger
from agent.llm_agent import ClaudeAgent


class ScenarioRunner:
    def __init__(
        self,
        registry: ToolRegistry,
        log_dir: str = "logs",
        provider: str = "claude",
        model: Optional[str] = None,
    ):
        self.registry = registry
        self.log_dir = log_dir
        self.provider = (provider or "claude").lower()
        self.model = model

    def create_run_id(self, scenario_id: str) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        short = str(uuid.uuid4())[:8]
        return f"{scenario_id}_{ts}_{short}"

    def _make_agent(self, logger, system_prompt, injection_config):
        if self.provider in ("openai", "gpt"):
            from agent.openai_agent import OpenAIAgent
            return OpenAIAgent(
                registry=self.registry,
                system_prompt=system_prompt,
                logger=logger,
                injection_config=injection_config,
                model=self.model or "gpt-4o-mini",
            )
        return ClaudeAgent(
            registry=self.registry,
            system_prompt=system_prompt,
            logger=logger,
            injection_config=injection_config,
            model=self.model or "claude-sonnet-5",
        )

    def run(
        self,
        scenario_id: str,
        user_message: str,
        system_prompt: Optional[str] = None,
        injection_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        run_id = self.create_run_id(scenario_id)
        logger = AgentLogger(run_id=run_id, log_dir=self.log_dir)
        prompt = system_prompt or "You are a helpful assistant."
        agent = self._make_agent(logger, prompt, injection_config)
        final_response = agent.run(user_message)
        log_path = logger.save()
        return {
            "run_id": run_id,
            "scenario_id": scenario_id,
            "provider": self.provider,
            "final_response": final_response,
            "log_path": log_path,
            "entries": logger.get_entries(),
            "injection_config": injection_config,
        }
