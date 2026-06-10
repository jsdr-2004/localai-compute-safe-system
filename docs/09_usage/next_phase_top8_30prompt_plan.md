# Next Phase: Top-8 / 30-Prompt Validation

The HP-001 partial-score ranking selected all eight tested setting combinations for `llama3.2:1b`. This reflects its strong speed and memory efficiency on HP-001; human quality scoring is still pending, so these are provisional selections.

The expanded phase uses 30 prompts across explanation, coding, Linux commands, debugging, summarization, reasoning, planning, safety refusal, local-assistant tasks, and command explanation.

Planned hardware:

- HP-001: MacBook Air M4, 16GB unified memory
- HP-002: Ryzen 5 5500U, 8GB RAM
- HP-003: RTX 3090-class GPU PC, 32GB RAM

Each config produces `8 settings × 30 prompts × 3 repeats = 720` measured tests, plus one warmup per model. Do not run HP-002 or HP-003 configs until their hardware profile JSON exists and the required model is installed.

```bash
python -m localai_system benchmark validate --config configs/benchmark_hp001_top8_30prompts.yaml
python -m localai_system benchmark dry-run --config configs/benchmark_hp001_top8_30prompts.yaml
```
