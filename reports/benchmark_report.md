# Benchmark Report

- Date generated: 2026-06-10
- Run ID: legacy dataset
- Results: `data/results/benchmark_results.csv`

## Hardware Profile

- Profile: HP-001
- CPU: Apple M4
- Cores/threads: 10/10
- RAM: 16.0 GB
- GPU: Apple M4
- OS/kernel: macOS-26.5.1-arm64-arm-64bit / 25.5.0
- Ollama: ollama version is 0.30.7

## Experiment Summary

- Total tests: 480
- Successful: 480
- Failed: 0
- Models: llama3.2:1b, llama3.2:3b, mistral:7b, qwen2.5:3b
- Prompt categories: basic_explanation, coding, debugging, linux, safety

## Model Metrics

| Model | Runs | Success Rate | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |
|---|---:|---:|---:|---:|---:|---:|
| llama3.2:1b | 120 | 100.0% | 45.79 | 0.197 | 7.61 | 8.17 |
| llama3.2:3b | 120 | 100.0% | 29.73 | 0.299 | 9.12 | 8.35 |
| mistral:7b | 120 | 100.0% | 13.02 | 0.257 | 21.51 | 9.64 |
| qwen2.5:3b | 120 | 100.0% | 28.76 | 0.218 | 11.97 | 8.43 |

## Failure Table

No failures recorded.

## Top 5 Recommended Configurations

| Rank | Model | Context | Temperature | Top-p | Score |
|---:|---|---:|---:|---:|---:|
| 1 | llama3.2:1b | 2048 | 0.7 | 0.95 | 0.8314 |
| 2 | llama3.2:1b | 1024 | 0.2 | 0.8 | 0.8251 |
| 3 | llama3.2:1b | 2048 | 0.7 | 0.8 | 0.8219 |
| 4 | llama3.2:1b | 2048 | 0.2 | 0.95 | 0.7945 |
| 5 | llama3.2:1b | 2048 | 0.2 | 0.8 | 0.7713 |

## Graphs

- [average_first_token_latency_by_model.png](reports/graphs/hp001_macbook_air_m4/average_first_token_latency_by_model.png)
- [average_peak_ram_by_model.png](reports/graphs/hp001_macbook_air_m4/average_peak_ram_by_model.png)
- [average_tokens_per_sec_by_model.png](reports/graphs/hp001_macbook_air_m4/average_tokens_per_sec_by_model.png)
- [average_total_response_time_by_model.png](reports/graphs/hp001_macbook_air_m4/average_total_response_time_by_model.png)
- [failure_rate_by_model.png](reports/graphs/hp001_macbook_air_m4/failure_rate_by_model.png)
- [model_performance_summary.png](reports/graphs/hp001_macbook_air_m4/model_performance_summary.png)
- [tokens_per_sec_by_context_length.png](reports/graphs/hp001_macbook_air_m4/tokens_per_sec_by_context_length.png)
- [total_response_time_by_context_length.png](reports/graphs/hp001_macbook_air_m4/total_response_time_by_context_length.png)

## Limitations

- Quality scores may be blank; recommendation scores are partial when so marked.
- Results are specific to one hardware profile and the Ollama backend.
- The initial sweep uses five prompts.

## Reproducibility Checklist

- [x] Hardware profile preserved
- [x] Config and prompt files preserved
- [x] CSV, JSONL, failures, and raw outputs preserved
- [x] Runtime/model versions recorded where available
- [ ] Human quality scoring complete
