# HP-001 Balanced Top-8 30-Prompt Dataset Validation

- Run ID: `hp001_balanced_top8_30prompts_v1`
- Dataset path: `data/runs/hp001_balanced_top8_30prompts_v1/benchmark_results.csv`
- Hardware profile path: `data/hardware_profiles/HP-001.json`
- Config snapshot path: `data/runs/hp001_balanced_top8_30prompts_v1/config_snapshot.yaml`
- Prompt snapshot path: `data/runs/hp001_balanced_top8_30prompts_v1/prompts_snapshot.json`
- Total rows: 720
- Successes: 720
- Failures: 0

## Model Coverage

| Model | Rows |
|---|---:|
| llama3.2:1b | 180 |
| llama3.2:3b | 180 |
| mistral:7b | 180 |
| qwen2.5:3b | 180 |

## Prompt Category Coverage

| Category | Rows |
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

| Model | Context | Temperature | Top-p | Rows |
|---|---:|---:|---:|---:|
| llama3.2:1b | 1024 | 0.2 | 0.8 | 90 |
| llama3.2:1b | 2048 | 0.7 | 0.95 | 90 |
| llama3.2:3b | 2048 | 0.2 | 0.8 | 90 |
| llama3.2:3b | 2048 | 0.7 | 0.8 | 90 |
| mistral:7b | 1024 | 0.7 | 0.95 | 90 |
| mistral:7b | 2048 | 0.7 | 0.95 | 90 |
| qwen2.5:3b | 2048 | 0.2 | 0.8 | 90 |
| qwen2.5:3b | 2048 | 0.2 | 0.95 | 90 |

## Raw Output Validation

- Raw output files: 720
- Non-empty raw output files: 720
- Successful rows with an existing non-empty legacy raw output: 720

## Artifact Validation

- Environment metadata exists: True
- Hardware snapshot exists: True
- Config snapshot exists: True
- Prompt snapshot exists: True

## Paper 1 Usability

The dataset is usable for Paper 1 performance, feasibility, and cross-hardware comparison work: it contains all 720 planned cases, no failures, complete family/category coverage, and non-empty raw outputs. Recommendation scores remain partial until human quality scoring is completed.

## Limitations

- Human quality scoring is pending.
- This phase currently covers HP-001 and the Ollama backend only.
- The 30-prompt suite is broader than the initial sweep but remains a bounded research sample.
