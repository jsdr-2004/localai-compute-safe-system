# Model Recommendations

Scores are normalized for the supplied hardware profile. `partial_score_used=true` means human quality scores were blank and the score uses speed, memory efficiency, and feasibility only.

## Top 5 Configurations

| Rank | Model | Context | Temperature | Top-p | Tokens/sec | Latency | Peak RAM | Feasibility | Partial | Score |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|---:|
| 1 | llama3.2:1b | 1024 | 0.2 | 0.8 | 67.6885 | 5.3133 | 24.3051 | smooth | True | 0.689 |
| 2 | llama3.2:1b | 2048 | 0.7 | 0.95 | 66.6893 | 5.4258 | 24.7717 | smooth | True | 0.6798 |
| 3 | qwen2.5:3b | 2048 | 0.2 | 0.8 | 49.9517 | 8.1693 | 23.631 | smooth | True | 0.6139 |
| 4 | qwen2.5:3b | 2048 | 0.2 | 0.95 | 46.6416 | 8.4117 | 22.9189 | smooth | True | 0.6057 |
| 5 | llama3.2:3b | 2048 | 0.2 | 0.8 | 48.5559 | 7.1021 | 26.2852 | smooth | True | 0.5815 |

## All Configurations

| Rank | Model | Configuration | Speed Rank | Memory Rank | Feasibility | Partial | Score |
|---:|---|---|---:|---:|---|---|---:|
| 1 | llama3.2:1b | ctx=1024, temp=0.2, top_p=0.8 | 1 | 4 | smooth | True | 0.689 |
| 2 | llama3.2:1b | ctx=2048, temp=0.7, top_p=0.95 | 2 | 5 | smooth | True | 0.6798 |
| 3 | qwen2.5:3b | ctx=2048, temp=0.2, top_p=0.8 | 3 | 3 | smooth | True | 0.6139 |
| 4 | qwen2.5:3b | ctx=2048, temp=0.2, top_p=0.95 | 6 | 2 | smooth | True | 0.6057 |
| 5 | llama3.2:3b | ctx=2048, temp=0.2, top_p=0.8 | 4 | 7 | smooth | True | 0.5815 |
| 6 | mistral:7b | ctx=1024, temp=0.7, top_p=0.95 | 7 | 1 | smooth | True | 0.5794 |
| 7 | llama3.2:3b | ctx=2048, temp=0.7, top_p=0.8 | 5 | 8 | smooth | True | 0.5598 |
| 8 | mistral:7b | ctx=2048, temp=0.7, top_p=0.95 | 8 | 6 | smooth | True | 0.5094 |

## Limitations

- Human quality scores are not yet populated for HP-001; all current recommendations are partial scores.
- Rankings are specific to the supplied hardware profile and Ollama runtime.

