# v0.2 Repository Audit

## Implemented Requirements

- Cross-platform hardware profiler with Apple Silicon and NVIDIA detection.
- Resumable Ollama matrix runner with CSV, JSONL, raw outputs, failures, and timeouts.
- HP-001 fixed-hardware dataset with 480 successful runs.
- Partial-score recommendation engine and matplotlib reporting.
- Deterministic privilege broker, explicit approval, append-only audit logging, and file-level rollback.
- Assistant defaults to no-execute mode and routes every proposal through the broker.

## Partially Implemented Requirements

- GPU utilization capture currently uses `nvidia-smi`; Apple Metal utilization is not sampled.
- Quality scoring is supported but HP-001 human review is incomplete.
- High-risk backup requires an explicit file path; automatic shell-command target extraction is intentionally absent.
- The broker is a research prototype, not an OS-enforced sandbox.

## Missing Requirements

- Multi-hardware HP-002/HP-004/HP-003 results.
- Additional runtime backends such as llama.cpp.
- Full safety benchmark metrics and formal false-positive/false-negative study.
- Cryptographic audit-log integrity.

## Safety Gaps

- Deterministic rules cannot understand every command semantic.
- Unknown approved commands remain risky; execution uses `shell=False` but is not containerized.
- The assistant must never be run as root.

## Reproducibility Gaps

- The original HP-001 run predates self-contained `data/runs/<run_id>/` snapshots.
- Thermal and power-state metadata were not automatically captured.
- Exact Ollama model digests are available from the local runtime but not embedded in the legacy HP-001 CSV.

## README Command Issues

- The old README showed only two model pulls despite the four-model HP-001 matrix.
- The old report command lacked the hardware profile argument.
- The macOS Homebrew formula installed during HP-001 lacked `llama-server`; the Ollama app distribution worked.

## Prioritized v0.2 Fixes

1. Self-contained run directories and environment snapshots.
2. Complete HP-001 validation/reporting artifacts.
3. Global top-configuration ranking with partial-score labels.
4. Expanded deterministic forbidden-command policy and safety tests.
5. Verified commands and next-phase 30-prompt configs.
