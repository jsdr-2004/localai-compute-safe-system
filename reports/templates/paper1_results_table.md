# Paper 1 Results Table

| Hardware Profile | Model | Context | Temperature | Top-p | Avg Tokens/sec | Avg Latency | Avg Peak RAM | Success Rate | Partial Score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HP-001 | llama3.2:1b | 2048 | 0.7 | 0.95 | 54.057 | 5.920s | 8.169GB | 100% | 0.8314 |
| HP-001 | llama3.2:1b | 1024 | 0.2 | 0.8 | 53.032 | 6.400s | 8.130GB | 100% | 0.8251 |
| HP-001 | llama3.2:1b | 2048 | 0.7 | 0.8 | 52.684 | 6.786s | 8.169GB | 100% | 0.8219 |

Full configuration results are stored in `reports/recommendations.csv`. Scores are partial because HP-001 quality scoring is pending.

## Pending Cross-Hardware Rows

The final table will add the same balanced configurations for HP-002, HP-004, and HP-003. HP-004 adds the modern Windows laptop-GPU class and enables analysis of 8GB-VRAM-sensitive recommendations. No pending-hardware measurements should be inserted before their benchmark runs complete.
