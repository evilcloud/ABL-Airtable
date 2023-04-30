import re


def create_gpu_summary(gpu_info):
    gpu_models = remove_nvidia_prefix(gpu_info["gpu_models"])
    unique_models = {}
    for model in gpu_models:
        unique_models[model] = unique_models.get(model, 0) + 1

    summary = ", ".join(f"{count} x {model}" for model, count in unique_models.items())
    return summary


def remove_nvidia_prefix(gpu_models):
    redundant_parts = ["NVIDIA", "GeForce", "RTX"]
    cleaned_models = []

    for model in gpu_models:
        cleaned = model
        for part in redundant_parts:
            cleaned = re.sub(rf"\s*{part}\s*", " ", cleaned)
        cleaned_models.append(cleaned.strip())

    return cleaned_models


def validate_data(data):
    if data["hashrate"] is None:
        return False
    if data["gpu_count"] == 0:
        return False
    if not data["gpu_summary"]:
        return False

    return True
