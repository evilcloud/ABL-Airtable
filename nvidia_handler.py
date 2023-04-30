import subprocess
import re


def get_gpu_info():
    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=index,name,uuid,power.draw",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.strip().split("\n")
    gpu_info = []
    for line in lines:
        index, name, uuid, power_draw = line.split(", ")
        gpu_info.append(
            {
                "index": int(index),
                "name": name,
                "uuid": uuid,
                "power_draw": int(re.sub(r"\..*", "", power_draw)),
            }
        )

    return gpu_info


if __name__ == "__main__":
    print(get_gpu_info())
