# Paper 1 Experiment Protocol

## Title

Compute-Aware Configuration Tuning for Local Large Language Models Across Consumer Hardware Classes

## Protocol

1. Record the hardware profile, OS, kernel, Python, runtime, models, git commit, and run ID.
2. Preserve config and prompt snapshots.
3. Hold hardware and runtime fixed while sweeping model settings.
4. Run a warmup before measured tests when configured.
5. Execute every matrix item with three repeats.
6. Record successes and failures without manual omission.
7. Preserve CSV, JSONL, raw outputs, graphs, and recommendations.
8. Perform human quality scoring with the documented 1-5 rubric.
9. Select top configurations using full scores when quality is available; otherwise label partial scores.
10. Repeat the expanded 30-prompt protocol on HP-001, HP-002, and HP-003.

## HP-001 Status

The first 480-test corrected run is complete and valid. It establishes the fixed-hardware baseline but is not the final multi-hardware study.
