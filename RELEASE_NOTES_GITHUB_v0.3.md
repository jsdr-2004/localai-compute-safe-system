# v0.3 HP-001 Balanced Top-8 30-Prompt Benchmark

## Summary

This release contains the completed HP-001 MacBook Air M4 16GB benchmark artifacts:

- 480-test full configuration sweep completed: 480 successes, 0 failures.
- 720-test balanced top-eight expanded run completed: 720 successes, 0 failures.
- 1,200 successful HP-001 benchmark measurements total, with 0 failures.
- Four model families tested: `llama3.2:1b`, `llama3.2:3b`, `qwen2.5:3b`, and `mistral:7b`.

## Artifacts

- Benchmark CSV and JSONL datasets
- Raw model outputs
- Hardware profiles and environment metadata
- Configuration and prompt snapshots
- Matplotlib graphs
- Recommendation and validation reports
- Paper 1 templates
- Reproducible dataset archive and SHA256 checksum

## Limitations

- Human quality scoring is pending; current recommendation scores are partial.
- HP-002, newly added HP-004, and HP-003 cross-hardware validation is pending.
- Ollama is the only evaluated inference backend so far.
- Results currently represent the MacBook Air M4 16GB hardware class only.

## Updated Four-Hardware Plan

HP-004 adds a realistic Windows NVIDIA laptop-GPU environment: MSI Crosshair 16 HX AI, Intel Core Ultra 7 255HX, 32GB RAM, and RTX 5060 Laptop GPU with 8GB VRAM. The remaining recommended order is HP-002, HP-004, then HP-003. Total planned measurements are 3,360: 1,200 completed and 2,160 pending.
