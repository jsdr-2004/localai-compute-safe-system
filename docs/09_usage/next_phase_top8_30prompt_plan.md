# Next Phase: Balanced Top-8 / 30-Prompt Validation

The original HP-001 partial-score ranking selected eight `llama3.2:1b` configurations because missing human quality scores caused speed and memory efficiency to dominate. That result is useful operationally but is not a research-valid basis for the expanded comparison.

The balanced phase therefore selects the best two measured configurations from each family: `llama3.2:1b`, `llama3.2:3b`, `qwen2.5:3b`, and `mistral:7b`. This preserves comparison across 1B, 3B, alternative 3B, and 7B model classes while human quality scoring remains pending. Selection uses the existing partial score, success rate, throughput, latency, RAM use, and feasibility.

The expanded phase uses 30 prompts across explanation, coding, Linux commands, debugging, summarization, reasoning, planning, safety refusal, local-assistant tasks, and command explanation. Each hardware run contains `8 configurations × 30 prompts × 3 repeats = 720` measured tests, plus one warmup per model family.

Planned hardware:

- HP-001: MacBook Air M4, 16GB unified memory
- HP-002: Ryzen 5 5500U, 8GB RAM
- HP-004: MSI Crosshair 16 HX AI, Intel Core Ultra 7 255HX, 32GB RAM, RTX 5060 Laptop GPU with 8GB VRAM
- HP-003: RTX 3090-class GPU PC, 32GB RAM

The remaining order is HP-002, HP-004, then HP-003. Do not run a pending config until its real hardware profile JSON exists and the required models are installed. The balanced choices originate from HP-001 and remain fixed across HP-002, HP-004, and HP-003 to support cross-hardware comparison.

The four-machine plan totals 3,360 measured tests: 1,200 completed on HP-001 and 2,160 pending.

```bash
python -m localai_system benchmark validate --config configs/benchmark_hp001_balanced_top8_30prompts.yaml
python -m localai_system benchmark dry-run --config configs/benchmark_hp001_balanced_top8_30prompts.yaml
python -m localai_system benchmark run --config configs/benchmark_hp001_balanced_top8_30prompts.yaml
```

HP-004 preparation only:

```bash
python -m localai_system benchmark validate --config configs/benchmark_hp004_balanced_top8_30prompts.yaml
python -m localai_system benchmark dry-run --config configs/benchmark_hp004_balanced_top8_30prompts.yaml
```
