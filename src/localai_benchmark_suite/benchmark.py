import requests
import time
import json
import csv
import os
import psutil
import yaml
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_system_usage():
    ram = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=None)
    return {
        "cpu_usage_percent": cpu_percent,
        "ram_used_gb": round(ram.used / (1024 ** 3), 3),
        "ram_percent": ram.percent
    }

def run_ollama_test(model_name, prompt, context_length, temperature, top_p):
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_ctx": context_length,
            "temperature": temperature,
            "top_p": top_p
        }
    }

    start_time = time.time()
    first_token_time = None
    output_text = ""
    token_count_estimate = 0

    before_usage = get_system_usage()
    peak_ram_gb = before_usage["ram_used_gb"]
    peak_cpu = before_usage["cpu_usage_percent"]

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=300
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            now = time.time()
            data = json.loads(line.decode("utf-8"))

            if "response" in data:
                chunk = data["response"]

                if chunk and first_token_time is None:
                    first_token_time = now

                output_text += chunk
                token_count_estimate += max(1, len(chunk.split()))

                usage = get_system_usage()
                peak_ram_gb = max(peak_ram_gb, usage["ram_used_gb"])
                peak_cpu = max(peak_cpu, usage["cpu_usage_percent"])

            if data.get("done") is True:
                break

        end_time = time.time()
        total_response_time = end_time - start_time
        first_token_latency = first_token_time - start_time if first_token_time else None
        tokens_per_sec = token_count_estimate / total_response_time if total_response_time > 0 else 0

        return {
            "status": "success",
            "first_token_latency_sec": round(first_token_latency, 4) if first_token_latency else None,
            "total_response_time_sec": round(total_response_time, 4),
            "tokens_per_sec_estimate": round(tokens_per_sec, 4),
            "peak_ram_gb": peak_ram_gb,
            "peak_cpu_usage_percent": peak_cpu,
            "output_text": output_text,
            "error": ""
        }

    except Exception as e:
        return {
            "status": "failed",
            "first_token_latency_sec": None,
            "total_response_time_sec": None,
            "tokens_per_sec_estimate": None,
            "peak_ram_gb": peak_ram_gb,
            "peak_cpu_usage_percent": peak_cpu,
            "output_text": "",
            "error": str(e)
        }

def write_result(csv_path, row):
    file_exists = os.path.isfile(csv_path)
    ensure_dir(os.path.dirname(csv_path))

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_yaml(os.path.join(current_dir, "config.yaml"))
    prompts = load_json(os.path.join(current_dir, "prompts.json"))

    output_csv = os.path.normpath(os.path.join(current_dir, config["output_csv"]))
    test_counter = 1

    for model in config["models"]:
        for context_length in config["settings"]["context_lengths"]:
            for temperature in config["settings"]["temperatures"]:
                for top_p in config["settings"]["top_p"]:
                    for prompt_item in prompts:
                        for repeat_id in range(1, config["repeat_each_test"] + 1):
                            test_id = f"T{test_counter:05d}"
                            test_counter += 1

                            print(
                                f"Running {test_id}: {model['name']} | "
                                f"ctx={context_length} | temp={temperature} | "
                                f"top_p={top_p} | {prompt_item['prompt_id']} | repeat={repeat_id}"
                            )

                            result = run_ollama_test(
                                model_name=model["name"],
                                prompt=prompt_item["prompt"],
                                context_length=context_length,
                                temperature=temperature,
                                top_p=top_p
                            )

                            row = {
                                "test_id": test_id,
                                "date": datetime.now().isoformat(),
                                "hardware_profile_id": config["hardware_profile_id"],
                                "runtime": config["runtime"],
                                "model_name": model["name"],
                                "model_size": model["size"],
                                "quantization": model["quantization"],
                                "context_length": context_length,
                                "temperature": temperature,
                                "top_p": top_p,
                                "prompt_id": prompt_item["prompt_id"],
                                "prompt_category": prompt_item["category"],
                                "repeat_id": repeat_id,
                                "status": result["status"],
                                "first_token_latency_sec": result["first_token_latency_sec"],
                                "tokens_per_sec_estimate": result["tokens_per_sec_estimate"],
                                "total_response_time_sec": result["total_response_time_sec"],
                                "peak_ram_gb": result["peak_ram_gb"],
                                "peak_cpu_usage_percent": result["peak_cpu_usage_percent"],
                                "quality_score": "",
                                "safety_score": "",
                                "feasibility_status": "",
                                "final_score": "",
                                "output_text": result["output_text"],
                                "error": result["error"]
                            }

                            write_result(output_csv, row)

    print(f"Benchmark complete. Results saved to {output_csv}")

if __name__ == "__main__":
    main()
