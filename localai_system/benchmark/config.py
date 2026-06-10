from __future__ import annotations

from pathlib import Path
from typing import Any

from localai_system.common.io import load_json, load_yaml


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    config = load_yaml(config_path)
    prompts_path = Path(config.get("prompts_file", ""))
    if not prompts_path.is_absolute():
        prompts_path = config_path.parent / prompts_path
    config["_config_path"] = str(config_path)
    config["_prompts_path"] = str(prompts_path)
    return config


def validate_config(config: dict[str, Any]) -> list[str]:
    errors = []
    for key in ("hardware_profile_id", "runtime", "repeat_each_test", "output_csv"):
        if key not in config:
            errors.append(f"Missing required field: {key}")
    if config.get("runtime") != "ollama":
        errors.append("Only the ollama runtime is supported in this prototype")
    configurations = config.get("configurations")
    if configurations is not None:
        if not isinstance(configurations, list) or not configurations:
            errors.append("configurations must be a non-empty list")
        for index, configuration in enumerate(configurations or [], start=1):
            for key in ("model_name", "model_size", "quantization", "context_length", "temperature", "top_p"):
                if key not in configuration:
                    errors.append(f"Configuration {index} missing required field: {key}")
            if "context_length" in configuration and int(configuration["context_length"]) < 1:
                errors.append(f"Configuration {index} context_length must be positive")
            for key in ("temperature", "top_p"):
                if key in configuration:
                    try:
                        value = float(configuration[key])
                        if value < 0 or (key == "top_p" and value > 1):
                            errors.append(f"Configuration {index} {key} is invalid")
                    except (TypeError, ValueError):
                        errors.append(f"Configuration {index} {key} must be numeric")
    else:
        if not isinstance(config.get("models"), list) or not config.get("models"):
            errors.append("models must be a non-empty list when configurations is not provided")
        for model in config.get("models", []):
            for key in ("name", "size", "quantization"):
                if key not in model:
                    errors.append(f"Model missing required field: {key}")
        settings = config.get("settings", {})
        for key in ("context_lengths", "temperatures", "top_p"):
            if not isinstance(settings.get(key), list) or not settings.get(key):
                errors.append(f"settings.{key} must be a non-empty list")
    if int(config.get("repeat_each_test", 0) or 0) < 1:
        errors.append("repeat_each_test must be at least 1")
    for key in ("warmup_runs", "cooldown_seconds_between_tests", "max_output_tokens", "per_test_timeout_seconds"):
        if key in config:
            try:
                value = float(config[key])
                if value < 0 or (key == "per_test_timeout_seconds" and value == 0):
                    errors.append(f"{key} must be positive" if value == 0 else f"{key} must not be negative")
            except (TypeError, ValueError):
                errors.append(f"{key} must be numeric")
    for key in ("save_raw_outputs", "save_environment_metadata", "resume"):
        if key in config and not isinstance(config[key], bool):
            errors.append(f"{key} must be true or false")
    if "run_id" in config and (not isinstance(config["run_id"], str) or not config["run_id"].strip()):
        errors.append("run_id must be a non-empty string")
    prompts_path = config.get("_prompts_path")
    if not prompts_path or not Path(prompts_path).exists():
        errors.append(f"Prompts file not found: {prompts_path}")
    else:
        prompts = load_json(prompts_path)
        if not isinstance(prompts, list) or not prompts:
            errors.append("Prompts file must contain a non-empty JSON list")
    return errors
