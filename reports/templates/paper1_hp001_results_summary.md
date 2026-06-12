# Paper 1 HP-001 Results Summary

HP-001 completed all 480 corrected benchmark cases successfully. The invalid earlier all-HTTP-500 runtime attempt was discarded and is not part of the research dataset.

| Model | Runs | Avg Tokens/sec | Avg First-token Latency | Avg Total Time | Avg Peak RAM |
|---|---:|---:|---:|---:|---:|
| llama3.2:1b | 120 | 45.79 | 0.197s | 7.61s | 8.17GB |
| llama3.2:3b | 120 | 29.73 | 0.299s | 9.12s | 8.35GB |
| qwen2.5:3b | 120 | 28.76 | 0.218s | 11.98s | 8.43GB |
| mistral:7b | 120 | 13.02 | 0.257s | 21.51s | 9.64GB |

The 1B model leads the current partial-score ranking because it provides the highest throughput and strong memory efficiency. This is not a final quality-aware conclusion; human output review is pending.

HP-001 remains the completed Apple Silicon baseline in the four-hardware plan. Cross-hardware claims wait for HP-002 low-memory CPU hardware, HP-004 modern Windows RTX 5060 laptop-GPU hardware with 8GB VRAM, and HP-003 RTX 3090-class workstation hardware.
