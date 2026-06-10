# Model Recommendations

Scores are normalized for the supplied hardware profile. `partial_score_used=true` means human quality scores were blank and the score uses speed, memory efficiency, and feasibility only.

## Top 5 Configurations

| Rank | Model | Context | Temperature | Top-p | Tokens/sec | Latency | Peak RAM | Feasibility | Partial | Score |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---:|
| 1 | llama3.2:1b | 2048 | 0.7 | 0.95 | 54.057 | 5.9204 | 8.1685 | smooth | True | 0.8314 |
| 2 | llama3.2:1b | 1024 | 0.2 | 0.8 | 53.032 | 6.3996 | 8.1296 | smooth | True | 0.8251 |
| 3 | llama3.2:1b | 2048 | 0.7 | 0.8 | 52.6843 | 6.7857 | 8.1693 | smooth | True | 0.8219 |
| 4 | llama3.2:1b | 2048 | 0.2 | 0.95 | 48.654 | 6.7569 | 8.1512 | smooth | True | 0.7945 |
| 5 | llama3.2:1b | 2048 | 0.2 | 0.8 | 45.0423 | 7.3976 | 8.0607 | smooth | True | 0.7713 |

## All Configurations

| Rank | Model | Configuration | Speed Rank | Memory Rank | Feasibility | Partial | Score |
|---:|---|---|---:|---:|---|---|---:|
| 1 | llama3.2:1b | ctx=2048, temp=0.7, top_p=0.95 | 1 | 6 | smooth | True | 0.8314 |
| 2 | llama3.2:1b | ctx=1024, temp=0.2, top_p=0.8 | 2 | 4 | smooth | True | 0.8251 |
| 3 | llama3.2:1b | ctx=2048, temp=0.7, top_p=0.8 | 3 | 7 | smooth | True | 0.8219 |
| 4 | llama3.2:1b | ctx=2048, temp=0.2, top_p=0.95 | 4 | 5 | smooth | True | 0.7945 |
| 5 | llama3.2:1b | ctx=2048, temp=0.2, top_p=0.8 | 5 | 1 | smooth | True | 0.7713 |
| 6 | llama3.2:1b | ctx=1024, temp=0.2, top_p=0.95 | 6 | 10 | smooth | True | 0.7505 |
| 7 | llama3.2:1b | ctx=1024, temp=0.7, top_p=0.8 | 7 | 12 | smooth | True | 0.7027 |
| 8 | llama3.2:1b | ctx=1024, temp=0.7, top_p=0.95 | 8 | 11 | smooth | True | 0.6976 |
| 9 | llama3.2:3b | ctx=2048, temp=0.2, top_p=0.8 | 9 | 3 | smooth | True | 0.687 |
| 10 | llama3.2:3b | ctx=2048, temp=0.7, top_p=0.8 | 10 | 17 | smooth | True | 0.6723 |
| 11 | qwen2.5:3b | ctx=2048, temp=0.2, top_p=0.8 | 11 | 9 | smooth | True | 0.6695 |
| 12 | llama3.2:3b | ctx=2048, temp=0.2, top_p=0.95 | 13 | 13 | smooth | True | 0.6676 |
| 13 | llama3.2:3b | ctx=1024, temp=0.7, top_p=0.95 | 12 | 16 | smooth | True | 0.6667 |
| 14 | qwen2.5:3b | ctx=2048, temp=0.2, top_p=0.95 | 14 | 18 | smooth | True | 0.6641 |
| 15 | qwen2.5:3b | ctx=1024, temp=0.7, top_p=0.95 | 15 | 14 | smooth | True | 0.6633 |
| 16 | qwen2.5:3b | ctx=1024, temp=0.7, top_p=0.8 | 17 | 8 | smooth | True | 0.6601 |
| 17 | qwen2.5:3b | ctx=1024, temp=0.2, top_p=0.95 | 20 | 15 | smooth | True | 0.6568 |
| 18 | llama3.2:3b | ctx=2048, temp=0.7, top_p=0.95 | 16 | 21 | smooth | True | 0.6546 |
| 19 | qwen2.5:3b | ctx=2048, temp=0.7, top_p=0.8 | 18 | 19 | smooth | True | 0.6546 |
| 20 | llama3.2:3b | ctx=1024, temp=0.7, top_p=0.8 | 23 | 2 | smooth | True | 0.6485 |
| 21 | llama3.2:3b | ctx=1024, temp=0.2, top_p=0.95 | 21 | 20 | smooth | True | 0.6442 |
| 22 | qwen2.5:3b | ctx=1024, temp=0.2, top_p=0.8 | 19 | 24 | smooth | True | 0.6432 |
| 23 | llama3.2:3b | ctx=1024, temp=0.2, top_p=0.8 | 22 | 23 | smooth | True | 0.6395 |
| 24 | qwen2.5:3b | ctx=2048, temp=0.7, top_p=0.95 | 24 | 22 | smooth | True | 0.6032 |
| 25 | mistral:7b | ctx=2048, temp=0.7, top_p=0.95 | 27 | 28 | smooth | True | 0.5402 |
| 26 | mistral:7b | ctx=1024, temp=0.7, top_p=0.95 | 28 | 25 | smooth | True | 0.5383 |
| 27 | mistral:7b | ctx=2048, temp=0.2, top_p=0.95 | 25 | 32 | smooth | True | 0.5382 |
| 28 | mistral:7b | ctx=2048, temp=0.7, top_p=0.8 | 26 | 31 | smooth | True | 0.5283 |
| 29 | mistral:7b | ctx=2048, temp=0.2, top_p=0.8 | 29 | 29 | smooth | True | 0.5158 |
| 30 | mistral:7b | ctx=1024, temp=0.7, top_p=0.8 | 30 | 27 | smooth | True | 0.4608 |
| 31 | mistral:7b | ctx=1024, temp=0.2, top_p=0.8 | 31 | 30 | slow | True | 0.4053 |
| 32 | mistral:7b | ctx=1024, temp=0.2, top_p=0.95 | 32 | 26 | slow | True | 0.3962 |

## Limitations

- Human quality scores are not yet populated for HP-001; all current recommendations are partial scores.
- Rankings are specific to the supplied hardware profile and Ollama runtime.

