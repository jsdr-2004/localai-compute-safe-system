# Software Requirements Specification

## 1. Introduction

This document defines the functional and non-functional requirements for the LocalAI Compute-Aware Safe System.

## 2. System Components

1. Hardware Profiler
2. Benchmark Runner
3. Model Recommendation Engine
4. Local AI Assistant CLI
5. Command Risk Classifier
6. Privilege Broker
7. Audit Logging System
8. Rollback/Backup Engine
9. Reporting and Visualization Module

## 3. Functional Requirements

### FR-001 Hardware Profiling

The system shall detect CPU model, CPU cores, RAM, GPU availability, VRAM, operating system, storage, and runtime environment.

### FR-002 Model Configuration Input

The system shall accept model name, model size, quantization level, context length, temperature, top-p, threads, and runtime backend.

### FR-003 Prompt Execution

The benchmark runner shall execute the same prompt set across all selected model configurations.

### FR-004 Performance Measurement

The system shall measure first-token latency, total response time, estimated tokens per second, peak RAM, CPU usage, and optional GPU/VRAM usage.

### FR-005 Result Export

The system shall export benchmark results to CSV and JSON.

### FR-006 Recommendation Score

The system shall calculate a final score using quality, speed, memory efficiency, and feasibility.

### FR-007 Local AI Assistant

The assistant shall accept user requests through a CLI interface and generate a proposed action plan.

### FR-008 Command Preview

The assistant shall show commands before execution.

### FR-009 Risk Classification

The risk classifier shall categorize actions as low, medium, high, critical, or forbidden.

### FR-010 Human Approval

The system shall require explicit user approval before executing medium, high, or critical actions.

### FR-011 Forbidden Action Blocking

The system shall block forbidden actions such as credential theft, security disabling, disk wiping, unauthorized persistence, destructive file deletion, and data exfiltration.

### FR-012 Audit Logging

The system shall log command proposals, risk levels, approval decisions, execution status, timestamps, and rollback metadata.

### FR-013 Rollback/Backup

The system shall create a backup or rollback point before high-risk operations when technically feasible.

## 4. Non-Functional Requirements

### NFR-001 Safety

The system must never provide uncontrolled root access to the AI assistant.

### NFR-002 Transparency

The user must be able to see what the assistant plans to do before execution.

### NFR-003 Reproducibility

Benchmark results must include hardware profile, software versions, model versions, runtime settings, and timestamps.

### NFR-004 Portability

The benchmark suite should run on Linux first, with later support for macOS and Windows.

### NFR-005 Extensibility

The system should support additional runtimes such as Ollama, llama.cpp, ONNX Runtime, and LocalAI.

### NFR-006 Security

The privilege broker must be isolated from the model and must enforce policy independently.

### NFR-007 Performance

The benchmark runner should be able to run unattended for long test matrices.

## 5. Assumptions

- The first benchmark backend is Ollama.
- The first operating system target is Ubuntu/Debian Linux.
- The first user interface is CLI.
- Human quality scoring is acceptable for early research phases.
- Exact token counting may be added later.

## 6. Constraints

- No uncontrolled root execution.
- No hidden command execution.
- No destructive operations without explicit confirmation.
- No claims of generality without multi-hardware validation.
