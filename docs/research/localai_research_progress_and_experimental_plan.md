# LocalAI Research Progress and Experimental Plan

## Research Goal

The project studies compute-aware configuration tuning for local large language models and a deterministic safety architecture for local AI assistants. It measures speed, latency, memory use, feasibility, and eventually human-reviewed quality across consumer hardware classes.

## Completed HP-001 Work

HP-001 is a MacBook Air M4 with 16GB unified memory running Ollama.

| Experiment | Tests | Successes | Failures |
|---|---:|---:|---:|
| Full four-model configuration sweep | 480 | 480 | 0 |
| Balanced top-eight, 30-prompt expanded run | 720 | 720 | 0 |
| Total | 1,200 | 1,200 | 0 |

The full sweep tested `llama3.2:1b`, `llama3.2:3b`, `qwen2.5:3b`, and `mistral:7b`. Because partial scoring favored the fastest model while quality scoring remained blank, the expanded phase selected two configurations per model family to preserve research validity.

## Current Interpretation

HP-001 demonstrates that all four tested model families are feasible on a 16GB Apple Silicon consumer laptop under the measured Ollama configuration. Performance rankings remain partial because human quality scoring has not been completed. Results must not be generalized to other hardware classes yet.

## Next Experimental Phase

1. Run the fixed balanced top-eight 30-prompt protocol on HP-002, a Ryzen 5 5500U system with 8GB RAM.
2. Run the same protocol on HP-003, an RTX 3090-class GPU system with 32GB RAM.
3. Complete human quality and safety scoring using a documented rubric.
4. Compare cross-hardware feasibility, latency, throughput, memory use, and recommendation stability.
5. Expand the prompt suite and evaluate additional local inference backends.

## Reproducibility

Each v0.3 run preserves CSV and JSONL results, raw outputs, hardware/config/prompt snapshots, environment metadata, graphs, and recommendation reports. See the [reproducibility checklist](../09_usage/reproducibility_checklist.md) and [next-phase plan](../09_usage/next_phase_top8_30prompt_plan.md).

## Limitations

- HP-001 is the only completed hardware profile.
- Human quality scoring is pending.
- Ollama is the only evaluated backend.
- The prompt suites are bounded research samples.
- The safety broker is a research prototype, not a production privilege boundary.
