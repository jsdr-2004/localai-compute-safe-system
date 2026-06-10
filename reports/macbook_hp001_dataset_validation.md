# HP-001 MacBook Air M4 Dataset Validation

- Dataset path: `data/results/benchmark_results.csv`
- Hardware profile path: `data/hardware_profiles/HP-001.json`
- Benchmark config path: `configs/benchmark_ollama.yaml`
- Prompt file path: `configs/prompts.json`
- Total rows: 480
- Success rows: 480
- Failed rows: 0
- Duplicate test IDs: 0
- Successful rows with empty/missing raw output: 0
- Invalid rows: 0
- Usable for Paper 1: **yes**

## Model Coverage

| Model | Rows |
|---|---:|
| llama3.2:1b | 120 |
| llama3.2:3b | 120 |
| mistral:7b | 120 |
| qwen2.5:3b | 120 |

## Prompt Coverage

| Prompt ID | Rows |
|---|---:|
| P001 | 96 |
| P002 | 96 |
| P003 | 96 |
| P004 | 96 |
| P005 | 96 |

## Settings Coverage

| Setting | Value | Rows |
|---|---|---:|
| context_length | 1024 | 240 |
| context_length | 2048 | 240 |
| temperature | 0.2 | 240 |
| temperature | 0.7 | 240 |
| top_p | 0.8 | 240 |
| top_p | 0.95 | 240 |
| repeat_id | 1 | 160 |
| repeat_id | 2 | 160 |
| repeat_id | 3 | 160 |

## Invalid-row Summary

No invalid rows were found.

## Limitations

- The benchmark CSV stores raw-output paths rather than embedding output text.
- Human quality scores are blank and must be added before full weighted conclusions.
- This is one hardware profile, one runtime backend, and an initial five-prompt sweep.
