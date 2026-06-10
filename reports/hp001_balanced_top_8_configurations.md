# HP-001 Balanced Top 8 Configurations

The original top-eight recommendation consisted entirely of `llama3.2:1b` configurations because human quality scores are missing and partial scoring favors speed and memory efficiency. For research validity, this balanced set selects the two strongest measured configurations within each model family. It enables comparison across 1B, 3B, alternative 3B, and 7B model classes. Human quality scoring remains pending, so every score below is a partial score.

| Balanced rank | Model | Size | Context | Temp | Top-p | Avg tokens/sec | Avg first-token latency | Avg total time | Avg peak RAM | Success rate | Partial score | Reason |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | llama3.2:1b | 1B | 2048 | 0.7 | 0.95 | 54.057 | 0.1738 | 5.9204 | 8.1685 | 100.0% | 0.8314 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |
| 2 | llama3.2:1b | 1B | 1024 | 0.2 | 0.8 | 53.032 | 0.211 | 6.3996 | 8.1296 | 100.0% | 0.8251 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |
| 3 | llama3.2:3b | 3B | 2048 | 0.2 | 0.8 | 32.9581 | 0.3022 | 8.4813 | 8.1057 | 100.0% | 0.687 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |
| 4 | llama3.2:3b | 3B | 2048 | 0.7 | 0.8 | 31.4298 | 0.2052 | 8.8204 | 8.3232 | 100.0% | 0.6723 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |
| 5 | qwen2.5:3b | 3B | 2048 | 0.2 | 0.8 | 30.7126 | 0.2436 | 11.231 | 8.2079 | 100.0% | 0.6695 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |
| 6 | qwen2.5:3b | 3B | 2048 | 0.2 | 0.95 | 30.4348 | 0.1881 | 10.5945 | 8.3884 | 100.0% | 0.6641 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |
| 7 | mistral:7b | 7B | 2048 | 0.7 | 0.95 | 15.9022 | 0.1775 | 16.9625 | 9.6165 | 100.0% | 0.5402 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |
| 8 | mistral:7b | 7B | 1024 | 0.7 | 0.95 | 15.103 | 0.1653 | 15.993 | 9.4292 | 100.0% | 0.5383 | Top-two partial-score configuration within model family; 100% successful in HP-001 fixed-hardware sweep |

## Selection Rule

- Select two configurations per model family using partial/final score first, then success, throughput, latency, RAM, and feasibility.
- Preserve the selected configurations unchanged across HP-001, HP-002, and HP-003 for cross-hardware validity.
- Do not interpret partial-score rank as a quality rank until human quality scoring is complete.
