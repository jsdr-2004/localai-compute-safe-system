# HP-001 MacBook Air M4 Balanced Top-8 30-Prompt Benchmark Report

- Date generated: 2026-06-10
- Run ID: hp001_balanced_top8_30prompts_v1
- Results: `data/runs/hp001_balanced_top8_30prompts_v1/benchmark_results.csv`

## Balanced Top-Eight Design

The original partial-score top eight contained only `llama3.2:1b` because missing human quality scores caused speed and memory efficiency to dominate. This phase instead fixes two high-performing HP-001 configurations from each of four model families, enabling research-valid comparison across 1B, 3B, alternative 3B, and 7B classes. All recommendation scores remain partial until human quality scoring is complete.

## 30-Prompt Suite

The expanded suite contains 30 prompts across ten categories: basic explanation, coding, command explanation, debugging, Linux commands, local assistant tasks, planning, reasoning, safety refusal, and summarization. Eight configurations multiplied by 30 prompts and three repeats produced 720 measured tests.

## Hardware Profile

- Profile: HP-001
- CPU: Apple M4
- Cores/threads: 10/10
- RAM: 16.0 GB
- GPU: Apple M4
- OS/kernel: macOS-26.5.1-arm64-arm-64bit / 25.5.0
- Ollama: ollama version is 0.30.7

## Experiment Summary

- Total tests: 720
- Successful: 720
- Failed: 0
- Models: llama3.2:1b, llama3.2:3b, mistral:7b, qwen2.5:3b
- Prompt categories: basic_explanation, coding, command_explanation, debugging, linux_commands, local_assistant_tasks, planning, reasoning, safety_refusal, summarization

## Model Metrics

| Model | Runs | Success Rate | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |
|---|---:|---:|---:|---:|---:|---:|
| llama3.2:1b | 180 | 100.0% | 45.50 | 0.214 | 7.96 | 8.35 |
| llama3.2:3b | 180 | 100.0% | 23.64 | 0.247 | 17.60 | 8.00 |
| mistral:7b | 180 | 100.0% | 14.19 | 0.201 | 25.33 | 9.94 |
| qwen2.5:3b | 180 | 100.0% | 30.59 | 0.221 | 13.95 | 8.14 |

## Prompt Category Metrics

| Category | Runs | Success Rate | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |
|---|---:|---:|---:|---:|---:|---:|
| basic_explanation | 72 | 100.0% | 29.92 | 0.233 | 13.98 | 8.51 |
| coding | 72 | 100.0% | 29.08 | 0.218 | 15.18 | 8.74 |
| command_explanation | 72 | 100.0% | 28.15 | 0.219 | 16.39 | 8.46 |
| debugging | 72 | 100.0% | 28.57 | 0.219 | 22.16 | 8.69 |
| linux_commands | 72 | 100.0% | 28.72 | 0.219 | 14.81 | 8.67 |
| local_assistant_tasks | 72 | 100.0% | 27.51 | 0.226 | 17.28 | 8.49 |
| planning | 72 | 100.0% | 28.15 | 0.219 | 22.02 | 8.65 |
| reasoning | 72 | 100.0% | 29.23 | 0.220 | 16.70 | 8.67 |
| safety_refusal | 72 | 100.0% | 26.68 | 0.220 | 11.75 | 8.54 |
| summarization | 72 | 100.0% | 28.79 | 0.213 | 11.83 | 8.66 |

## Failure Table

No failures recorded.

## Top 5 Recommended Configurations

| Rank | Model | Context | Temperature | Top-p | Score |
|---:|---|---:|---:|---:|---:|
| 1 | llama3.2:1b | 1024 | 0.2 | 0.8 | 0.8064 |
| 2 | llama3.2:1b | 2048 | 0.7 | 0.95 | 0.8058 |
| 3 | qwen2.5:3b | 2048 | 0.2 | 0.8 | 0.7043 |
| 4 | qwen2.5:3b | 2048 | 0.2 | 0.95 | 0.6857 |
| 5 | llama3.2:3b | 2048 | 0.2 | 0.8 | 0.679 |

## Graphs

- [average_first_token_latency_by_model.png](graphs/hp001_balanced_top8_30prompts/average_first_token_latency_by_model.png)
- [average_peak_ram_by_model.png](graphs/hp001_balanced_top8_30prompts/average_peak_ram_by_model.png)
- [average_tokens_per_sec_by_model.png](graphs/hp001_balanced_top8_30prompts/average_tokens_per_sec_by_model.png)
- [average_total_response_time_by_model.png](graphs/hp001_balanced_top8_30prompts/average_total_response_time_by_model.png)
- [failure_rate_by_model.png](graphs/hp001_balanced_top8_30prompts/failure_rate_by_model.png)
- [model_performance_summary.png](graphs/hp001_balanced_top8_30prompts/model_performance_summary.png)
- [tokens_per_sec_by_context_length.png](graphs/hp001_balanced_top8_30prompts/tokens_per_sec_by_context_length.png)
- [total_response_time_by_context_length.png](graphs/hp001_balanced_top8_30prompts/total_response_time_by_context_length.png)

## Limitations

- Quality scores may be blank; recommendation scores are partial when so marked.
- Results are specific to one hardware profile and the Ollama backend.
- This dataset contains 30 distinct prompts.

## Reproducibility Checklist

- [x] Hardware profile preserved
- [x] Config and prompt files preserved
- [x] CSV, JSONL, failures, and raw outputs preserved
- [x] Runtime/model versions recorded where available
- [ ] Human quality scoring complete

## Next Step

Run the same fixed balanced top-eight and 30-prompt protocol on HP-002 (Ryzen 5 5500U, 8GB) and HP-003 (RTX 3090-class, 32GB) without changing the selected configurations.
