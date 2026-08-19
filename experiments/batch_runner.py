"""
배치 실행 스크립트
Control / Treatment / Ablation을 자동으로 순회 실행하고 로그 저장
"""

from __future__ import annotations
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# 프로젝트 루트 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.base import default_registry
from tools import mock_tools  # noqa: F401
from agent.runner import ScenarioRunner
from configs.experiment_config import generate_experiment_cases, ExperimentCase
from injection.channels import InjectionChannel


def run_single_variant(
    runner: ScenarioRunner,
    case: ExperimentCase,
    variant: str,  # "control" | "treatment" | "ablation"
) -> Dict[str, Any]:
    """한 케이스의 한 변형을 실행"""

    if variant == "control":
        injection_config = None
    elif variant == "treatment":
        injection_config = {
            "channel": case.channel,
            "payload": case.payload,
            "injection_name": case.injection_name,
            "description": case.description,
        }
    elif variant == "ablation":
        # Ablation: 주입 설정을 명시적으로 제거한 상태로 재실행
        injection_config = None
    else:
        raise ValueError(f"Unknown variant: {variant}")

    result = runner.run(
        scenario_id=case.scenario_id,
        user_message=case.user_message,
        injection_config=injection_config,
    )

    return {
        "case_id": case.case_id,
        "variant": variant,
        "scenario_id": case.scenario_id,
        "channel": case.channel,
        "injection_name": case.injection_name,
        "payload": case.payload if variant == "treatment" else None,
        "description": case.description,
        "run_id": result["run_id"],
        "log_path": result["log_path"],
        "final_response": result["final_response"],
        "entries": result["entries"],
        "injection_config": result.get("injection_config"),
    }


def run_batch(output_dir: str = "data/batch_results") -> List[Dict[str, Any]]:
    """전체 실험 케이스에 대해 Control / Treatment / Ablation 실행"""

    os.makedirs(output_dir, exist_ok=True)
    runner = ScenarioRunner(registry=default_registry, log_dir="logs")
    cases = generate_experiment_cases()

    all_results = []
    total = len(cases) * 3
    done = 0

    print(f"Total runs to execute: {total}")
    print("=" * 60)

    for case in cases:
        print(f"\n[{case.case_id}]")

        for variant in ["control", "treatment", "ablation"]:
            result = run_single_variant(runner, case, variant)
            all_results.append(result)
            done += 1
            print(f"  - {variant:10s} → {result['run_id']} ({done}/{total})")

    # 결과 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(output_dir, f"batch_results_{timestamp}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"Batch complete. Results saved to: {out_path}")
    print(f"Total records: {len(all_results)}")

    return all_results


if __name__ == "__main__":
    run_batch()