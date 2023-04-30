import subprocess
import re
import datetime


def get_mining_stats():
    cmd = 'systemctl status abel.service | grep " m " | tail -1'
    output = subprocess.check_output(cmd, shell=True, text=True)

    match = re.search(r"abelminer (\d+):(\d+).*?([\d.]+) (Mh|Kh|h)", output)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        value = float(match.group(3))
        unit = match.group(4)

        if unit == "Kh":
            value *= 1000
        elif unit == "h":
            value *= 1_000_000

        return {"hashrate": value}
    else:
        return {"hashrate": None}


def get_uptime():
    # Run the uptime command to get the system reboot time
    cmd = "uptime -s"
    output = subprocess.check_output(cmd, shell=True, text=True).strip()

    # Parse the reboot time as a datetime object
    reboot_time = datetime.datetime.strptime(output, "%Y-%m-%d %H:%M:%S")

    # Calculate the time since the last reboot
    time_since_reboot = datetime.datetime.now() - reboot_time

    return time_since_reboot


def get_gpu_info():
    # Run the nvidia-smi command to get the list of GPUs and their information
    cmd = "nvidia-smi -L"
    output = subprocess.check_output(cmd, shell=True, text=True)

    # Split the output into individual GPU lines
    gpu_lines = output.strip().split("\n")

    # Calculate the GPU count
    gpu_count = len(gpu_lines)

    # Extract GPU models from each line
    gpu_models = []
    for line in gpu_lines:
        match = re.search(r": (.*?) \(UUID", line)
        if match:
            gpu_models.append(match.group(1))

    # Return the GPU count and the list of GPU models
    return {"gpu_count": gpu_count, "gpu_models": gpu_models}
