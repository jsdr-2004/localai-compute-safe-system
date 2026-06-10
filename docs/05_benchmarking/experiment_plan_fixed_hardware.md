# Experiment Plan: Fixed Hardware Model Setting Tuning

## Goal

Run all tests on one fixed computer while changing only model settings.

## Hypothesis

Local LLM performance and feasibility change significantly based on model size, quantization, context length, and sampling settings even when hardware remains constant.

## Fixed Variables

- Device
- CPU
- RAM
- GPU
- VRAM
- OS
- Runtime backend
- Power mode
- Thermal condition
- Prompt set

## Independent Variables

- Model name
- Model size
- Quantization
- Context length
- Temperature
- Top-p
- Threads
- Batch size

## Dependent Variables

- First-token latency
- Total response time
- Tokens per second
- Peak RAM
- Peak VRAM
- CPU usage
- GPU usage
- Output quality score
- Feasibility status
- Failure rate

## Initial Test Matrix

| Model Size | Quantization | Context Length | Temperature | Top-p |
|---|---|---:|---:|---:|
| 1B | default/INT4 | 1024 | 0.2 | 0.8 |
| 1B | default/INT4 | 2048 | 0.7 | 0.95 |
| 3B | default/INT4 | 1024 | 0.2 | 0.8 |
| 3B | default/INT4 | 2048 | 0.7 | 0.95 |
| 7B | default/INT4 | 1024 | 0.2 | 0.8 |
| 7B | default/INT4 | 2048 | 0.7 | 0.95 |

## Prompt Categories

- Basic explanation
- Coding
- Linux command help
- Debugging
- Safety refusal
- Summarization
- Reasoning
- Planning

## Run Rules

1. Use the same prompt set for all models.
2. Run each test at least 3 times.
3. Record all failures.
4. Do not manually skip poor results.
5. Save raw outputs.
6. Record hardware and software versions.
7. Do not change power mode during runs.
8. Restart runtime between major model groups if needed.

## Research Output

- Benchmark CSV
- Model comparison graph
- Context length impact graph
- RAM usage graph
- Speed vs quality graph
- Best configuration recommendation
