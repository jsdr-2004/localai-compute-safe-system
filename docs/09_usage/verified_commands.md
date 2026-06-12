# v0.2 Verified Commands

Verification date: June 10, 2026. The full 480-case benchmark was **not rerun** during v0.2 verification.

| Command | Purpose | Status | Notes |
|---|---|---|---|
| `python -m localai_system hardware print` | Inspect hardware without writing files | passed | Detected Apple M4, 10 cores/threads, and 16GB RAM. |
| `python -m localai_system benchmark validate --config configs/benchmark_ollama.yaml` | Validate initial HP-001 matrix | passed | Reports 480 tests. |
| `python -m localai_system benchmark dry-run --config configs/benchmark_ollama.yaml` | Print initial HP-001 matrix | passed | Reports 480 planned tests; no model execution. |
| `python -m localai_system benchmark validate --config configs/benchmark_hp004_balanced_top8_30prompts.yaml` | Validate planned HP-004 balanced matrix | passed | Reports 720 tests; HP-004 benchmark was not run. |
| `python -m localai_system benchmark dry-run --config configs/benchmark_hp004_balanced_top8_30prompts.yaml` | Print planned HP-004 balanced matrix | passed | Reports 720 planned tests; no model execution. |
| `python -m localai_system benchmark validate --config configs/benchmark_hp001_top8_30prompts.yaml` | Validate next phase | passed | Reports 720 tests. |
| `python -m localai_system benchmark dry-run --config configs/benchmark_hp001_top8_30prompts.yaml` | Preview next phase | passed | Reports 720 planned tests; not executed. |
| `python -m localai_system report graphs --results data/results/benchmark_results.csv --output-dir reports/graphs/hp001_macbook_air_m4` | Regenerate HP-001 graphs | passed | Generated eight matplotlib PNGs. |
| `python -m localai_system recommend --results data/results/benchmark_results.csv --hardware data/hardware_profiles/HP-001.json --output reports/recommendations.md` | Generate partial-score recommendations | passed | Wrote Markdown and CSV. |
| `python -m localai_system report markdown --results data/results/benchmark_results.csv --hardware data/hardware_profiles/HP-001.json --recommendations reports/recommendations.csv --graphs-dir reports/graphs/hp001_macbook_air_m4 --output reports/benchmark_report.md` | Generate complete benchmark report | passed | Uses preserved HP-001 dataset. |
| `python -m localai_system broker classify "df -h"` | Verify low-risk classification | passed | Decision: allow. |
| `python -m localai_system broker classify "sudo apt install docker.io"` | Verify approval requirement | passed | Decision: approval_required. |
| `python -m localai_system broker classify "rm -rf /"` | Verify forbidden block | passed | Decision: block. |
| `python -m localai_system assistant` | Verify default no-execute mode | passed | `df -h` was classified, logged, and not executed. |
| `python -m localai_system audit list` | Inspect append-only audit records | passed | Displayed assistant proposal event. |
| `pytest` | Run automated verification | passed | 18 tests passed. |

## Not Run

| Command | Status | Notes |
|---|---|---|
| `python -m localai_system benchmark run --config configs/benchmark_ollama.yaml` | not run | The valid 480-case HP-001 dataset already exists. |
| `python -m localai_system benchmark run --config configs/benchmark_hp001_top8_30prompts.yaml` | not run | Prepared for the next phase only. |
| `python -m localai_system assistant --execute` | not run interactively | Execution safety is covered with isolated automated tests. |
