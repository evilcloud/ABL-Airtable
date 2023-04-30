from collections import Counter
from datetime import timedelta


def process_gpu_data(gpu_data):
    gpu_names = []
    power_draws = 0
    redundant_substrings = ["NVIDIA", "GeForce", "RTX"]

    for gpu in gpu_data:
        # Simplify the GPU name by removing redundant substrings
        simplified_name = gpu["name"]
        for substring in redundant_substrings:
            simplified_name = simplified_name.replace(substring, "").strip()

        gpu_names.append(simplified_name)
        power_draws += gpu["power_draw"]

    # Count the occurrences of each GPU model
    gpu_counts = Counter(gpu_names)

    # Create the content string with counts and UUIDs
    content = ", ".join(f"{count} x {model}" for model, count in gpu_counts.items())

    return {"Content": content, "Power draw": power_draws}


def process_system_data(system_data):
    hashrate = system_data["hashrate"]
    reboot = system_data["reboot"]

    # Convert time since last reboot to seconds
    reboot_seconds = reboot.days * 86400 + reboot.seconds

    return {
        "Name": system_data["hostname"],
        "Hashrate": hashrate,
        "Reboot": reboot_seconds,
    }


if __name__ == "__main__":
    # Example GPU data
    example_gpu_data = [
        {
            "name": "NVIDIA GeForce RTX 3080 Ti",
            "uuid": "GPU-12345678",
            "power_draw": 300,
        },
        {
            "name": "NVIDIA GeForce RTX 3080 Ti",
            "uuid": "GPU-23456789",
            "power_draw": 300,
        },
        {"name": "NVIDIA GeForce RTX 3060", "uuid": "GPU-34567890", "power_draw": 150},
    ]

    # Example system data
    example_system_data = {
        "hostname": "example_hostname",
        "hashrate": 456,
        "reboot": timedelta(seconds=7200),
    }

    # Process the example data
    processed_gpu_data = process_gpu_data(example_gpu_data)
    processed_system_data = process_system_data(example_system_data)

    # Print the results
    print("Processed GPU data:", processed_gpu_data)
    print("Processed system data:", processed_system_data)
