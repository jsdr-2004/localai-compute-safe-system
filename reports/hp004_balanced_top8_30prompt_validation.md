# HP-004 Balanced Top-8 30-Prompt Dataset Validation

- Run ID: `hp004_balanced_top8_30prompts_v1`
- Dataset path: `data/runs/hp004_balanced_top8_30prompts_v1/benchmark_results.csv`
- Legacy dataset path: `data/results/hp004_balanced_top8_30prompts_v1.csv`
- Hardware profile path: `data/hardware_profiles/HP-004.json`
- Run hardware snapshot: `data/runs/hp004_balanced_top8_30prompts_v1/hardware_profile.json`
- Config snapshot path: `data/runs/hp004_balanced_top8_30prompts_v1/config_snapshot.yaml`
- Prompt snapshot path: `data/runs/hp004_balanced_top8_30prompts_v1/prompts_snapshot.json`
- Environment metadata path: `data/runs/hp004_balanced_top8_30prompts_v1/environment_metadata.json`

## Result Counts

| Metric | Count |
|---|---:|
| Total rows | 720 |
| Successful rows | 720 |
| Failed rows | 0 |
| JSONL events | 720 |
| Run-local raw output files | 720 |
| Non-empty run-local raw output files | 720 |
| Legacy raw output files | 720 |
| Non-empty legacy raw output files | 720 |

## Model Coverage

| Model | Rows |
|---|---:|
| llama3.2:1b | 180 |
| llama3.2:3b | 180 |
| qwen2.5:3b | 180 |
| mistral:7b | 180 |

## Prompt Category Coverage

| Prompt category | Rows |
|---|---:|
| basic_explanation | 72 |
| coding | 72 |
| command_explanation | 72 |
| debugging | 72 |
| linux_commands | 72 |
| local_assistant_tasks | 72 |
| planning | 72 |
| reasoning | 72 |
| safety_refusal | 72 |
| summarization | 72 |

## Settings Coverage

| Setting | Value | Rows |
|---|---|---:|
| context_length | 1024 | 180 |
| context_length | 2048 | 540 |
| temperature | 0.2 | 360 |
| temperature | 0.7 | 360 |
| top_p | 0.8 | 360 |
| top_p | 0.95 | 360 |

## Integrity Notes

- The benchmark completed all 720 planned tests with no recorded failures.
- Raw model outputs are stored outside the CSV and were verified as present and non-empty for all 720 successful tests.
- The run directory includes CSV, JSONL, hardware snapshot, config snapshot, prompt snapshot, environment metadata, and raw outputs.
- The HP-004 hardware profile records Windows 11 Home as the display OS while preserving Python's platform string: `Windows-10-10.0.26200-SP0`.
- `llama_cpp_path` is intentionally `null`; `C:\Windows\system32\main.CPL` was identified as a Windows PATH false positive, not a llama.cpp executable.

## Paper 1 Usability

This dataset is usable as the HP-004 Windows NVIDIA laptop-GPU comparison point for Paper 1. It should be interpreted as a throughput, latency, memory, and feasibility dataset only until human quality scoring is completed.

## Limitations

- Human quality scores are still pending, so recommendation scores are partial.
- Results are specific to the MSI Crosshair 16 HX AI / RTX 5060 Laptop GPU environment and the installed Ollama runtime.
- The benchmark uses the balanced top-eight HP-001-derived configuration set rather than a full HP-004 hyperparameter sweep.
