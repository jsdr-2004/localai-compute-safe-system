from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="localai_system")
    sub = parser.add_subparsers(dest="area", required=True)

    hardware = sub.add_parser("hardware")
    hardware_sub = hardware.add_subparsers(dest="action", required=True)
    hp = hardware_sub.add_parser("profile")
    hp.add_argument("--output", required=True)
    hardware_sub.add_parser("print")

    benchmark = sub.add_parser("benchmark")
    benchmark_sub = benchmark.add_subparsers(dest="action", required=True)
    for action in ("run", "dry-run", "validate"):
        command = benchmark_sub.add_parser(action)
        command.add_argument("--config", required=True)

    recommend = sub.add_parser("recommend")
    recommend.add_argument("--results", required=True)
    recommend.add_argument("--hardware", required=True)
    recommend.add_argument("--output", required=True)

    report = sub.add_parser("report")
    report_sub = report.add_subparsers(dest="action", required=True)
    graphs = report_sub.add_parser("graphs")
    graphs.add_argument("--results", required=True)
    graphs.add_argument("--output-dir", default="reports/graphs")
    markdown = report_sub.add_parser("markdown")
    markdown.add_argument("--results", required=True)
    markdown.add_argument("--hardware")
    markdown.add_argument("--recommendations")
    markdown.add_argument("--graphs-dir", default="reports/graphs")
    markdown.add_argument("--output", required=True)

    broker = sub.add_parser("broker")
    broker_sub = broker.add_subparsers(dest="action", required=True)
    classify = broker_sub.add_parser("classify")
    classify.add_argument("command")
    classify.add_argument("--policy", default="configs/policy_rules.yaml")

    audit = sub.add_parser("audit")
    audit_sub = audit.add_subparsers(dest="action", required=True)
    audit_list = audit_sub.add_parser("list")
    audit_list.add_argument("--log", default="data/audit/audit.jsonl")
    audit_show = audit_sub.add_parser("show")
    audit_show.add_argument("--event-id", required=True)
    audit_show.add_argument("--log", default="data/audit/audit.jsonl")

    rollback = sub.add_parser("rollback")
    rollback_sub = rollback.add_subparsers(dest="action", required=True)
    rollback_list = rollback_sub.add_parser("list")
    rollback_list.add_argument("--backup-dir", default="data/backups")
    restore = rollback_sub.add_parser("restore")
    restore.add_argument("--rollback-id", required=True)
    restore.add_argument("--backup-dir", default="data/backups")

    assistant = sub.add_parser("assistant")
    assistant.add_argument("--execute", action="store_true", help="Enable approved command execution")
    assistant.add_argument("--policy", default="configs/policy_rules.yaml")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.area == "hardware":
        from localai_system.hardware.profiler import cli
    elif args.area == "benchmark":
        from localai_system.benchmark.runner import cli
    elif args.area == "recommend":
        from localai_system.recommender.engine import cli
    elif args.area == "report":
        from localai_system.reporting.reports import cli
    elif args.area == "broker":
        from localai_system.broker.broker import cli
    elif args.area == "audit":
        from localai_system.audit.logger import cli
    elif args.area == "rollback":
        from localai_system.rollback.manager import cli
    else:
        from localai_system.assistant.cli import cli
    return cli(args)


if __name__ == "__main__":
    raise SystemExit(main())
