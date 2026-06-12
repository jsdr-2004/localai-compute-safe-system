# Hardware Profile Template

## Hardware Profile ID

HP-XXX

## Device

Device Name:

Manufacturer:

Model:

## CPU

CPU Model:

Cores:

Threads:

Base Clock:

## Memory

RAM:

RAM Type:

## GPU

GPU Model:

VRAM:

Driver Version:

## Storage

Storage Type:

Available Storage:

## Operating System

OS:

Version:

Kernel:

## Runtime Environment

Python Version:

Ollama Version:

llama.cpp Version:

CUDA Version:

Docker Version:

## Power/Thermal Conditions

Plugged In: Yes/No

Power Mode:

Room Temperature:

Thermal Notes:

## Date Recorded

Date:

## Planned Hardware Profiles

| Profile | Class | Status |
|---|---|---|
| HP-001 | Apple Silicon consumer laptop | Completed |
| HP-002 | Low-memory CPU-constrained system | Pending |
| HP-004 | Modern Windows laptop GPU with RTX 5060 Laptop GPU and 8GB VRAM | Template added / pending |
| HP-003 | High-performance GPU workstation | Pending |

HP-004 must record Windows version, NVIDIA driver, CUDA/runtime details, dedicated VRAM, secondary integrated GPU, power mode, and thermal conditions. Use `data/hardware_profiles/HP-004.template.json` only as a planning template; generate `HP-004.json` with the profiler on the actual machine before benchmarking.
