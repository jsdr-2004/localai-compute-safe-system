# LocalAI Research Progress and Experimental Plan

## 1. Research Goal

The project studies compute-aware configuration tuning for local large language models and deterministic safety controls for local AI assistants.

## 2. Current Evidence Base

HP-001, a MacBook Air M4 with 16GB unified memory, has completed a 480-test full sweep and a 720-test balanced top-eight expanded run. All 1,200 measured runs succeeded.

## 3. Research Questions

- RQ1: How do model and runtime settings affect speed, latency, memory use, quality, and feasibility on fixed hardware?
- RQ2: Can hardware-aware recommendation rules reduce local LLM deployment trial-and-error?
- RQ3: How do recommendations change across low-memory CPU-based machines, Apple Silicon laptops, Windows laptop-GPU systems, and high-performance GPU workstations?
- RQ4: Can deterministic broker controls reduce risk in AI-assisted system administration?

## 4. Research Design

The study begins with fixed-hardware model-setting sweeps, then holds selected configurations constant across low-resource CPU systems, mainstream Apple Silicon consumer laptops, modern Windows laptop-GPU systems, and high-performance GPU workstation environments.

## 5. Hardware Profiles

| ID | Machine/Class | Key Resources | Status |
|---|---|---|---|
| HP-001 | MacBook Air M4 / Apple Silicon consumer laptop | 16GB unified memory | 1,200 tests completed |
| HP-002 | Ryzen 5 5500U / low-memory CPU-constrained system | 8GB RAM | Pending |
| HP-004 | MSI Crosshair 16 HX AI / modern Windows laptop GPU | Core Ultra 7 255HX, 32GB RAM, RTX 5060 Laptop GPU, 8GB VRAM | Newly added / pending |
| HP-003 | RTX 3090-class GPU PC / high-performance GPU workstation | 32GB RAM | Pending |

## 6. Models

The balanced phase fixes two configurations from each family: `llama3.2:1b`, `llama3.2:3b`, `qwen2.5:3b`, and `mistral:7b`.

## 7. Metrics

Metrics include first-token latency, total response time, estimated tokens/sec, peak RAM, peak VRAM where available, CPU/GPU use, success/failure, feasibility, and human quality scores when completed.

## 8. Reproducibility Controls

Each run preserves CSV, JSONL, raw outputs, hardware/config/prompt snapshots, environment metadata, graphs, recommendations, run ID, and git commit.

## 9. Balanced Configuration Rationale

The original partial-score top eight favored `llama3.2:1b` because quality scoring was blank. The balanced set preserves representation across 1B, 3B, alternative 3B, and 7B classes for research validity.

## 10. Four-Machine Research Plan

| Phase | Hardware | Configuration Set | Prompts | Repeats | Tests | Status |
|---|---|---|---:|---:|---:|---|
| A | HP-001 MacBook Air M4 | 32 configurations | 5 | 3 | 480 | Completed |
| B | HP-001 MacBook Air M4 | Balanced top 8 | 30 | 3 | 720 | Completed |
| C | HP-002 Ryzen 5 5500U | Balanced top 8 | 30 | 3 | 720 | Pending |
| D | HP-004 MSI Crosshair 16 HX AI RTX 5060 Laptop GPU | Balanced top 8 | 30 | 3 | 720 | Newly added / pending |
| E | HP-003 RTX 3090-class GPU PC | Balanced top 8 | 30 | 3 | 720 | Pending |
| **Total** | **Four hardware profiles** |  |  |  | **3,360** | **1,200 completed; 2,160 pending** |

## 11. Cross-Hardware Evaluation Strategy

The fixed balanced configurations enable direct comparison of low-memory CPU-constrained local AI deployment, Apple Silicon consumer laptop deployment, Windows laptop GPU deployment, and high-performance GPU workstation deployment.

## 12. HP-004 Research Role

HP-004 fills the gap between Apple Silicon consumer laptops and high-end workstation GPUs. Its dedicated RTX 5060 Laptop GPU and limited 8GB VRAM support realistic evaluation of Windows laptop GPU performance and VRAM-sensitive model recommendations.

## 13. Safety-System Track

The assistant safety track remains separate from benchmark execution: models propose commands, while deterministic broker policy, approval, audit, and rollback controls govern actions.

## 14. Current Research Status

HP-001 has 1,200 successful runs and zero failures. The fourth hardware profile has been added: MSI Crosshair 16 HX AI with Intel Core Ultra 7 255HX, 32GB RAM, and NVIDIA RTX 5060 Laptop GPU with 8GB VRAM. HP-002, HP-004, and HP-003 benchmarks remain pending.

## 15. Planned Research Outputs

- HP-002, HP-004, and HP-003 benchmark datasets and validation reports
- HP-004 performance graphs and recommendation report
- Apple Silicon versus Windows GPU laptop comparison
- Laptop GPU versus workstation GPU comparison
- VRAM-sensitive recommendation rules and cross-hardware decision maps

## 16. Paper 1 Direction

Paper 1 will evaluate four hardware classes: HP-001 MacBook Air M4 with 16GB unified memory; HP-002 Ryzen 5 5500U with 8GB RAM; HP-004 MSI Crosshair 16 HX AI with Intel Core Ultra 7 255HX, 32GB RAM, RTX 5060 Laptop GPU with 8GB VRAM, and Windows 11 Home; and HP-003 RTX 3090-class GPU workstation with 32GB RAM.

## 17. Paper Completion Roadmap

HP-001 supports controlled fixed-hardware conclusions. Broader cross-hardware claims must wait until HP-002, HP-004, and HP-003 are complete and human quality scoring is incorporated.

## 18. Data Integrity

Completed HP-001 measurements are immutable research artifacts. New hardware runs must use unique run IDs and resume behavior without overwriting prior datasets.

## 19. Research Limitations

- HP-002, HP-004, and HP-003 testing are still pending.
- Human quality scoring is pending.
- Ollama is the only evaluated backend.
- Laptop power, thermal, and GPU VRAM behavior require careful recording.

## 20. Next Steps

1. Run HP-002 Ryzen 5 5500U 8GB benchmark.
2. Create the real HP-004 profiler output and run the MSI Crosshair 16 HX AI RTX 5060 Laptop GPU benchmark.
3. Run HP-003 RTX 3090-class workstation benchmark.
4. Generate cross-hardware comparison reports and decision maps.

## 21. Conclusion

The four-machine plan now spans low-memory CPU hardware, Apple Silicon, a modern Windows NVIDIA laptop GPU, and a high-performance GPU workstation. The next major step is to run the same balanced top-eight 30-prompt benchmark on HP-002, HP-004, and HP-003.
