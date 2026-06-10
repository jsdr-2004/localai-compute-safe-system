# HP-001 MacBook Air M4 Local LLM Benchmark Report

## Purpose

This is the first controlled fixed-hardware configuration sweep for compute-aware local LLM selection. It establishes an HP-001 baseline without claiming cross-hardware generality.

## Hardware Summary

- CPU/GPU: Apple M4 / Apple M4
- CPU cores/threads: 10/10
- Unified memory: 16.0 GB
- OS/kernel: macOS-26.5.1-arm64-arm-64bit / 25.5.0
- Ollama: ollama version is 0.30.7

## Model Matrix

- Models: llama3.2:1b, llama3.2:3b, mistral:7b, qwen2.5:3b
- Context lengths: 1024, 2048
- Temperatures: 0.2, 0.7
- Top-p: 0.8, 0.95
- Prompts: 5
- Repeats: 3

## Experimental Design

4 models × 2 context lengths × 2 temperatures × 2 top-p values × 5 prompts × 3 repeats = **480 tests**.

## Metrics

- First-token latency
- Total response time
- Estimated tokens/sec
- Peak system RAM
- Peak CPU usage
- Success/failure status
- Derived feasibility

## Results Summary

- Successful runs: 480/480
- Fastest average model: **llama3.2:1b**
- Lowest average peak RAM model: **llama3.2:1b**
- Lowest average first-token latency model: **llama3.2:1b**
- Highest partial-score configuration: **llama3.2:1b**, context 2048, temperature 0.7, top-p 0.95.

## Top 8 Configurations

| Rank | Model | Size | Context | Temp | Top-p | Avg tokens/sec | Avg latency | Avg peak RAM | Feasibility | Partial score |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | llama3.2:1b | 1B | 2048 | 0.7 | 0.95 | 54.057 | 5.9204 | 8.1685 | smooth | 0.8314 |
| 2 | llama3.2:1b | 1B | 1024 | 0.2 | 0.8 | 53.032 | 6.3996 | 8.1296 | smooth | 0.8251 |
| 3 | llama3.2:1b | 1B | 2048 | 0.7 | 0.8 | 52.6843 | 6.7857 | 8.1693 | smooth | 0.8219 |
| 4 | llama3.2:1b | 1B | 2048 | 0.2 | 0.95 | 48.654 | 6.7569 | 8.1512 | smooth | 0.7945 |
| 5 | llama3.2:1b | 1B | 2048 | 0.2 | 0.8 | 45.0423 | 7.3976 | 8.0607 | smooth | 0.7713 |
| 6 | llama3.2:1b | 1B | 1024 | 0.2 | 0.95 | 42.4488 | 8.6446 | 8.2118 | smooth | 0.7505 |
| 7 | llama3.2:1b | 1B | 1024 | 0.7 | 0.8 | 35.5937 | 9.0212 | 8.2343 | smooth | 0.7027 |
| 8 | llama3.2:1b | 1B | 1024 | 0.7 | 0.95 | 34.8304 | 9.9184 | 8.2254 | smooth | 0.6976 |

## Failure Analysis

No corrected-run failures were recorded. The earlier all-HTTP-500 run was invalid runtime output and was discarded before this dataset.

## Graphs

- [average_first_token_latency_by_model.png](reports/graphs/hp001_macbook_air_m4/average_first_token_latency_by_model.png)
- [average_peak_ram_by_model.png](reports/graphs/hp001_macbook_air_m4/average_peak_ram_by_model.png)
- [average_tokens_per_sec_by_model.png](reports/graphs/hp001_macbook_air_m4/average_tokens_per_sec_by_model.png)
- [average_total_response_time_by_model.png](reports/graphs/hp001_macbook_air_m4/average_total_response_time_by_model.png)
- [failure_rate_by_model.png](reports/graphs/hp001_macbook_air_m4/failure_rate_by_model.png)
- [model_performance_summary.png](reports/graphs/hp001_macbook_air_m4/model_performance_summary.png)
- [tokens_per_sec_by_context_length.png](reports/graphs/hp001_macbook_air_m4/tokens_per_sec_by_context_length.png)
- [total_response_time_by_context_length.png](reports/graphs/hp001_macbook_air_m4/total_response_time_by_context_length.png)

## Research Interpretation

On this 16 GB Apple Silicon laptop, the 1B model provides the strongest throughput and memory-efficient interactive baseline. The 3B models trade speed for potentially greater capability, while Mistral 7B remains feasible but has materially lower throughput and longer responses. Human quality review is required before treating the partial-score ranking as a final recommendation.

## Limitations

- One hardware profile only so far.
- Human quality scoring is not yet completed.
- Ollama is the only tested backend.
- The initial sweep uses five prompts.
- Cross-hardware validation is pending.

## Next Step

Use the selected top eight configurations for a 30-prompt expanded test on HP-001 MacBook Air M4 16GB, HP-002 Ryzen 5 5500U 8GB, and HP-003 RTX 3090-class GPU PC 32GB.
