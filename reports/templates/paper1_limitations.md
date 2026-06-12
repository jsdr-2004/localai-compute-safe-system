# Paper 1 Limitations

- HP-001 is one hardware profile and cannot establish cross-hardware generality.
- Human quality scoring is incomplete, so current recommendation scores are partial.
- Ollama is the only evaluated runtime backend.
- The initial sweep contains five prompts; broader task coverage is planned.
- System-wide RAM and CPU peaks may include background processes.
- Apple unified memory makes direct system RAM versus VRAM separation difficult.
- Estimated token throughput relies on runtime-provided counts and timing.
- Thermal and power-state effects were not fully controlled automatically.
- HP-002, HP-004, and HP-003 validation is pending.
- HP-004 laptop-GPU performance may be sensitive to Windows power mode, NVIDIA driver/runtime versions, thermal limits, and its 8GB VRAM ceiling.
