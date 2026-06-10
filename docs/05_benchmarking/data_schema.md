# Benchmark Data Schema

## CSV Columns

| Column | Description |
|---|---|
| run_id | Unique benchmark run identifier |
| test_id | Unique benchmark test ID |
| date | Timestamp |
| hardware_profile_id | Hardware profile reference |
| runtime | Runtime backend |
| model_name | Model identifier |
| model_size | Parameter size |
| quantization | Quantization level |
| context_length | Context window |
| temperature | Sampling temperature |
| top_p | Top-p value |
| prompt_id | Prompt identifier |
| prompt_category | Task category |
| repeat_id | Repeat number |
| status | success or failed |
| first_token_latency_sec | Time to first token |
| tokens_per_sec_estimate | Estimated generation speed |
| total_response_time_sec | Total response time |
| peak_ram_gb | Peak system RAM usage |
| peak_vram_gb | Peak VRAM usage |
| peak_cpu_usage_percent | Peak CPU usage |
| peak_gpu_usage_percent | Peak GPU usage |
| quality_score | Human quality score |
| safety_score | Safety score |
| feasibility_status | smooth, slow, unusable, failed |
| final_score | Weighted ranking score |
| raw_output_path | Path to separately preserved model output |
| error | Error message |

## Feasibility Labels

| Label | Meaning |
|---|---|
| smooth | Usable for local assistant |
| slow | Works but poor experience |
| unusable | Too slow or memory-heavy |
| failed | Crashed or could not complete |
