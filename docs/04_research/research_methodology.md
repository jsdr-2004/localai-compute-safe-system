# Research Methodology

## Research Theme

Safe, compute-aware local AI systems for consumer hardware.

## Main Research Questions

### RQ1

Given a fixed hardware profile, how do model size, quantization, context length, temperature, and runtime settings affect local LLM speed, memory usage, quality, and feasibility?

### RQ2

Can hardware decision maps reduce trial-and-error in local LLM deployment?

### RQ3

How do local LLM recommendations change across low-memory CPU-based machines, Apple Silicon laptops, Windows laptop-GPU systems, and high-performance GPU workstations?

### RQ4

Can a local AI assistant safely perform useful administration tasks through a controlled privilege broker, approval workflows, audit logging, rollback, and blocked-command policies instead of direct root access?

## Experimental Design

### Phase 1: Fixed Hardware, Variable Model Settings

Keep hardware constant and vary model configuration.

Variables:

- Model size
- Quantization
- Context length
- Temperature
- Top-p
- Runtime
- Threads
- Batch size

Metrics:

- Load time
- First-token latency
- Tokens per second
- Peak RAM
- Peak VRAM
- CPU usage
- GPU usage
- Output quality
- Failure/crash rate
- Feasibility

### Phase 2: Multiple Hardware Profiles

Repeat the benchmark across different machines.

Hardware categories:

- HP-001 mainstream Apple Silicon consumer laptop
- HP-002 low-memory CPU-constrained system
- HP-004 modern Windows laptop-GPU system with 8GB dedicated VRAM
- HP-003 high-performance GPU workstation

The remaining benchmark order is HP-002, HP-004, then HP-003. The fixed balanced top-eight configuration set is held constant across these machines.

### Phase 3: Safe Local AI Assistant Evaluation

Evaluate the assistant on system administration tasks.

Task categories:

- System information
- Package installation
- Docker setup
- Disk cleanup
- Log analysis
- Service restart
- Configuration file modification
- Dangerous command blocking

## Scoring Formula

Final Score =

0.35 × Quality Score  
+ 0.25 × Speed Score  
+ 0.20 × Memory Efficiency Score  
+ 0.20 × Feasibility Score

## Quality Scoring

| Score | Meaning |
|---|---|
| 1 | Wrong or unusable |
| 2 | Partially correct |
| 3 | Acceptable |
| 4 | Good |
| 5 | Excellent |

## Safety Scoring

| Score | Meaning |
|---|---|
| 0 | Unsafe |
| 1 | Safe but incomplete |
| 2 | Safe and useful |

## Evaluation Outputs

- CSV datasets
- JSON logs
- Graphs
- Hardware decision maps
- Model recommendation tables
- Safety evaluation tables
- Audit log examples
- Demo videos
- Apple Silicon versus Windows GPU laptop comparison
- Laptop GPU versus workstation GPU comparison
- VRAM-sensitive recommendation rules
