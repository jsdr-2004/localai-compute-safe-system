# Paper 1 Methodology

## Study Design

The study begins with a fixed-hardware configuration sweep, then validates selected configurations across four hardware classes. HP-001 is the first controlled experiment.

## HP-001 Initial Sweep

- Hardware: MacBook Air M4, 16GB unified memory
- Runtime: Ollama
- Models: llama3.2:1b, llama3.2:3b, qwen2.5:3b, mistral:7b
- Settings: context lengths 1024/2048, temperatures 0.2/0.7, top-p 0.8/0.95
- Prompt suite: five prompts
- Repeats: three
- Total measured tests: 480

The runner preserved CSV, JSONL, and raw outputs and recorded every success or failure. Metrics include first-token latency, total response time, estimated tokens/sec, peak system RAM, peak CPU, and feasibility.

## Recommendation Method

The documented score weights quality, speed, memory efficiency, and feasibility. Because HP-001 human quality scores are blank, current rankings are explicitly labeled partial scores and normalize the remaining speed, memory, and feasibility weights.

## Four-Hardware Validation Stage

The balanced top-eight configurations are evaluated with a 30-prompt suite in this order:

1. HP-001 Apple Silicon consumer laptop: completed.
2. HP-002 low-memory CPU-constrained system: pending.
3. HP-004 modern Windows laptop-GPU system with RTX 5060 Laptop GPU and 8GB VRAM: newly added / pending.
4. HP-003 high-performance RTX 3090-class GPU workstation: pending.

The same configurations and prompts remain fixed so the study can compare Apple Silicon, CPU-only constraints, limited laptop VRAM, and workstation GPU capacity.
