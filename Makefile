.PHONY: install test profile dry-run sample-report

install:
	python3 -m pip install -e ".[dev]"

test:
	python3 -m pytest

profile:
	python3 -m localai_system hardware profile --output data/hardware_profiles/HP-001.json

dry-run:
	python3 -m localai_system benchmark dry-run --config configs/benchmark_ollama.yaml

sample-report:
	python3 -m localai_system report markdown --results data/results/sample_benchmark_results.csv --output reports/benchmark_report.md
