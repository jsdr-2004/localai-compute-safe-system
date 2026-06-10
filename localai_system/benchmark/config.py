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
    for key in ("hardware_profile_id", "runtime", "models", "settings", "repeat_each_test", "output_csv"):
        if key not in config:
            errors.append(f"Missing required field: {key}")
    if config.get("runtime") != "ollama":
        errors.append("Only the ollama runtime is supported in this prototype")
    if not isinstance(config.get("models"), list) or not config.get("models"):
        errors.append("models must be a non-empty list")
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
    prompts_path = config.get("_prompts_path")
    if not prompts_path or not Path(prompts_path).exists():
        errors.append(f"Prompts file not found: {prompts_path}")
    else:
        prompts = load_json(prompts_path)
        if not isinstance(prompts, list) or not prompts:
            errors.append("Prompts file must contain a non-empty JSON list")
    return errors
