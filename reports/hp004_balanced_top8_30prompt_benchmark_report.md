# Benchmark Report

- Date generated: 2026-07-06
- Run ID: hp004_balanced_top8_30prompts_v1
- Results: `data\results\hp004_balanced_top8_30prompts_v1.csv`

## Hardware Profile

- Profile: HP-004
- CPU: Intel64 Family 6 Model 198 Stepping 2, GenuineIntel
- Cores/threads: 20/20
- RAM: 31.419 GB
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU
- OS/kernel: Windows 11 Home, platform string `Windows-10-10.0.26200-SP0` / 10
- Ollama: ollama version is 0.31.1
- llama.cpp: not detected; an earlier Windows PATH lookup resolved `C:\Windows\system32\main.CPL` and was removed as a false positive.

## Experiment Summary

- Total tests: 720
- Successful: 720
- Failed: 0
- Models: llama3.2:1b, llama3.2:3b, mistral:7b, qwen2.5:3b
- Prompt categories: basic_explanation, coding, command_explanation, debugging, linux_commands, local_assistant_tasks, planning, reasoning, safety_refusal, summarization

## Model Metrics

| Model | Runs | Success Rate | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |
|---|---:|---:|---:|---:|---:|---:|
| llama3.2:1b | 180 | 100.0% | 67.19 | 2.474 | 5.37 | 24.54 |
| llama3.2:3b | 180 | 100.0% | 47.62 | 2.477 | 7.16 | 26.95 |
| mistral:7b | 180 | 100.0% | 34.88 | 2.514 | 10.54 | 23.47 |
| qwen2.5:3b | 180 | 100.0% | 48.30 | 2.405 | 8.29 | 23.27 |

## Prompt Category Metrics

| Category | Runs | Success Rate | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |
|---|---:|---:|---:|---:|---:|---:|
| basic_explanation | 72 | 100.0% | 46.69 | 2.838 | 7.72 | 24.63 |
| coding | 72 | 100.0% | 51.56 | 2.401 | 7.66 | 24.76 |
| command_explanation | 72 | 100.0% | 51.68 | 2.405 | 8.04 | 24.89 |
| debugging | 72 | 100.0% | 56.45 | 2.400 | 9.60 | 24.64 |
| linux_commands | 72 | 100.0% | 48.53 | 2.385 | 7.97 | 24.63 |
| local_assistant_tasks | 72 | 100.0% | 52.08 | 2.374 | 7.58 | 24.36 |
| planning | 72 | 100.0% | 56.37 | 2.491 | 9.42 | 24.49 |
| reasoning | 72 | 100.0% | 52.67 | 2.496 | 8.06 | 24.35 |
| safety_refusal | 72 | 100.0% | 36.40 | 2.419 | 6.23 | 24.63 |
| summarization | 72 | 100.0% | 42.53 | 2.468 | 6.13 | 24.22 |

## Failure Table

No failures recorded.

## Top 5 Recommended Configurations

| Rank | Model | Context | Temperature | Top-p | Score |
|---:|---|---:|---:|---:|---:|
| 1 | llama3.2:1b | 1024 | 0.2 | 0.8 | 0.958 |
| 2 | llama3.2:1b | 2048 | 0.7 | 0.95 | 0.9473 |
| 3 | qwen2.5:3b | 2048 | 0.2 | 0.8 | 0.8648 |
| 4 | qwen2.5:3b | 2048 | 0.2 | 0.95 | 0.8545 |
| 5 | llama3.2:3b | 2048 | 0.2 | 0.8 | 0.8293 |

## Graphs

- [average_first_token_latency_by_model.png](graphs/hp004_balanced_top8_30prompts/average_first_token_latency_by_model.png)
- [average_peak_ram_by_model.png](graphs/hp004_balanced_top8_30prompts/average_peak_ram_by_model.png)
- [average_tokens_per_sec_by_model.png](graphs/hp004_balanced_top8_30prompts/average_tokens_per_sec_by_model.png)
- [average_total_response_time_by_model.png](graphs/hp004_balanced_top8_30prompts/average_total_response_time_by_model.png)
- [failure_rate_by_model.png](graphs/hp004_balanced_top8_30prompts/failure_rate_by_model.png)
- [model_performance_summary.png](graphs/hp004_balanced_top8_30prompts/model_performance_summary.png)
- [tokens_per_sec_by_context_length.png](graphs/hp004_balanced_top8_30prompts/tokens_per_sec_by_context_length.png)
- [total_response_time_by_context_length.png](graphs/hp004_balanced_top8_30prompts/total_response_time_by_context_length.png)

## Limitations

- Quality scores may be blank; recommendation scores are partial when so marked.
- Results are specific to one hardware profile and the Ollama backend.
- This dataset contains 30 distinct prompts.
- Python's platform string reports Windows 11 build 26200 using a Windows-10-style identifier; the display OS is recorded as Windows 11 Home.

## Reproducibility Checklist

- [x] Hardware profile preserved
- [x] Config and prompt files preserved
- [x] CSV, JSONL, failures, and raw outputs preserved
- [x] Runtime/model versions recorded where available
- [ ] Human quality scoring complete
