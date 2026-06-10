# Model Recommendations

Scores are normalized for the supplied hardware profile. `partial_score_used=true` means human quality scores were blank and the score uses speed, memory efficiency, and feasibility only.

## Top 5 Configurations

| Rank | Model | Context | Temperature | Top-p | Tokens/sec | Latency | Peak RAM | Feasibility | Partial | Score |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---:|
| 1 | llama3.2:1b | 1024 | 0.2 | 0.8 | 45.4498 | 7.8764 | 8.313 | smooth | True | 0.8064 |
| 2 | llama3.2:1b | 2048 | 0.7 | 0.95 | 45.5576 | 8.0476 | 8.3879 | smooth | True | 0.8058 |
| 3 | qwen2.5:3b | 2048 | 0.2 | 0.8 | 29.9278 | 14.2177 | 7.3926 | smooth | True | 0.7043 |
| 4 | qwen2.5:3b | 2048 | 0.2 | 0.95 | 31.2503 | 13.6815 | 8.8887 | smooth | True | 0.6857 |
| 5 | llama3.2:3b | 2048 | 0.2 | 0.8 | 29.8801 | 12.4253 | 8.6861 | smooth | True | 0.679 |

## All Configurations

| Rank | Model | Configuration | Speed Rank | Memory Rank | Feasibility | Partial | Score |
|---:|---|---|---:|---:|---|---|---:|
| 1 | llama3.2:1b | ctx=1024, temp=0.2, top_p=0.8 | 2 | 3 | smooth | True | 0.8064 |
| 2 | llama3.2:1b | ctx=2048, temp=0.7, top_p=0.95 | 1 | 4 | smooth | True | 0.8058 |
| 3 | qwen2.5:3b | ctx=2048, temp=0.2, top_p=0.8 | 4 | 2 | smooth | True | 0.7043 |
| 4 | qwen2.5:3b | ctx=2048, temp=0.2, top_p=0.95 | 3 | 6 | smooth | True | 0.6857 |
| 5 | llama3.2:3b | ctx=2048, temp=0.2, top_p=0.8 | 5 | 5 | smooth | True | 0.679 |
| 6 | llama3.2:3b | ctx=2048, temp=0.7, top_p=0.8 | 6 | 1 | smooth | True | 0.5629 |
| 7 | mistral:7b | ctx=1024, temp=0.7, top_p=0.95 | 7 | 7 | smooth | True | 0.4907 |
| 8 | mistral:7b | ctx=2048, temp=0.7, top_p=0.95 | 8 | 8 | smooth | True | 0.4759 |

## Limitations

- Human quality scores are not yet populated for HP-001; all current recommendations are partial scores.
- Rankings are specific to the supplied hardware profile and Ollama runtime.

