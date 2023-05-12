import subprocess
import re
import socket


# convert to the single hashrate
def get_hashrates():
    # Implement a function to fetch GPU hashrates using the provided command
    result = subprocess.run(
        ["systemctl", "status", "abel.service"],
        capture_output=True,
        text=True,
    )
    hashrates_line = re.search(r"(\d+(?:\.\d+)?)[ ]?([mMkK]?)[hH].*- cu", result.stdout)
    if hashrates_line:
        hashrates_str = hashrates_line.group()
        hashrate_tuples = re.findall(r"(\d+(?:\.\d+)?)[ ]?([mMkK]?)[hH]", hashrates_str)
        hashrates = [convert_to_mh(value, unit) for value, unit in hashrate_tuples]
    else:
        hashrates = []

    return hashrates


# a single hashrate harvest
def get_hashrate():
    result = subprocess.run(
        ["systemctl", "status", "abel.service"],
        capture_output=True,
        text = True,
    )
    hashrate_line = re.search(r"(\d+(?:\.\d+)?)[ ]?([mMkK]?)[hH].*- cu", result.stdout)
    if hashrate_line:
        hashrate_str = hashrate_line.group()
        hashrate_tuple = re.findall(r"(\d+(?:\.\d+)?)[ ]?([mMkK]?)[hH]"), hashrate_str)
        value, unit, _ = hashrate_tuple if len(hashrate_tuple) > 1 else []
        hashrate = convert_to_mh(value, unit)
    else:
        0
    
    return hashrate

def convert_to_mh(value, unit):
    try:
        value = float(value)
    except ValueError:
        value = 0
    if unit.lower() == "k":
        value /= 1000
    elif unit.lower() == "h":
        value /= 1_000_000
    else:
        value = 0
    return value


def get_hostname():
    hostname = socket.gethostname()
    return hostname


def get_time_since_last_boot():
    # Get the system uptime in seconds
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds


def get_system_data():
    hostname = get_hostname()
    hashrate = get_hashrates()
    reboot_seconds = get_time_since_last_boot()


if __name__ == "__main__":
    print("Hashrates (Mh):", get_hashrates())
    print("Hostname:", get_hostname())
    print("Time since last boot (seconds):", get_time_since_last_boot())
