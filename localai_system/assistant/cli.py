from __future__ import annotations

from typing import Any

from localai_system.broker.broker import PrivilegeBroker
from localai_system.broker.policy import Policy
from localai_system.assistant.planner import route_request


def cli(args: Any) -> int:
    broker = PrivilegeBroker(Policy.from_yaml(args.policy), execution_enabled=args.execute)
    print("LocalAI Safe Assistant. Type 'exit' to quit.")
    print(f"Execution is {'enabled' if args.execute else 'disabled'}; every proposal still passes through the broker.")
    while True:
        try:
            request = input("\nRequest> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if request.lower() in {"exit", "quit"}:
            return 0
        plan = route_request(request)
        print(f"Plan: {plan.explanation}")
        for command in plan.commands:
            classification = broker.classify(command)
            print(f"\nCommand: {command}\nExplanation: {plan.explanation}\nRisk: {classification.risk_level}\n"
                  f"Decision: {classification.decision}\nReason: {classification.reason}")
            approved = False
            if classification.requires_approval:
                phrase = "CONFIRM" if classification.decision == "explicit_confirmation_required" else "yes"
                approved = input(f"Type {phrase!r} to approve: ").strip() == phrase
            result = broker.handle(request, command, approved=approved)
            print(f"Execution status: {result['event']['execution_status']}")
            if result["stdout"]:
                print(result["stdout"].rstrip())
            if result["stderr"]:
                print(result["stderr"].rstrip())
