import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

results_path = Path("../../data/templates/benchmark_results.csv")
out_dir = Path("../../reports/graphs")
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(results_path)

success = df[df["status"] == "success"].copy()

if success.empty:
    print("No successful benchmark rows found.")
    raise SystemExit

plt.figure()
success.groupby("model_name")["tokens_per_sec_estimate"].mean().sort_values().plot(kind="bar")
plt.ylabel("Average Estimated Tokens/sec")
plt.title("Average Speed by Model")
plt.tight_layout()
plt.savefig(out_dir / "avg_tokens_per_sec_by_model.png")

plt.figure()
success.groupby("model_name")["peak_ram_gb"].mean().sort_values().plot(kind="bar")
plt.ylabel("Average Peak RAM GB")
plt.title("Average Peak RAM by Model")
plt.tight_layout()
plt.savefig(out_dir / "avg_peak_ram_by_model.png")

plt.figure()
success.groupby("context_length")["total_response_time_sec"].mean().plot(kind="bar")
plt.ylabel("Average Total Response Time sec")
plt.title("Response Time by Context Length")
plt.tight_layout()
plt.savefig(out_dir / "response_time_by_context_length.png")

print(f"Graphs saved to {out_dir}")
