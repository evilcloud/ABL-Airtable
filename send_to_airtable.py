import os
import sys
import socket
from airtable import Airtable
from mining_stats import get_mining_stats, get_gpu_info, get_uptime
from process_data import create_gpu_summary, validate_data

# Get the Airtable API Key
airtable_api_key = os.environ.get("AIRTABLE_API_KEY")
if not airtable_api_key:
    print("Please set the AIRTABLE_API_KEY environment variable.")
    sys.exit(1)

# Get the Airtable Base ID
airtable_base_id = os.environ.get("AIRTABLE_BASE_ID")
if not airtable_base_id:
    print("Please set the AIRTABLE_BASE_ID environment variable.")
    sys.exit(1)

# Get the table name from the environment variable
table_name = os.environ.get("AIRTABLE_TABLE_NAME")
if not table_name:
    print("Please set the AIRTABLE_TABLE_NAME environment variable.")
    sys.exit(1)

# Initialize the Airtable connection
airtable = Airtable(airtable_base_id, table_name, api_key=airtable_api_key)

# Get the mining statistics and GPU information
mining_stats = get_mining_stats()
gpu_info = get_gpu_info()

# Get the time since the last reboot
uptime = get_uptime()

# Create a summary of the GPU models
gpu_summary = create_gpu_summary(gpu_info)

# Prepare the data to send to Airtable
data = {
    "Hashrate": mining_stats["hashrate"],
    "gpu_count": gpu_info["gpu_count"],
    "gpu_summary": gpu_summary,
    "Reboot": int(uptime.total_seconds()),
}

# Check if the data is valid
if validate_data(data):
    # Get the hostname or use "Unknown" if it's not set
    hostname = socket.gethostname()

    # Update the Airtable row with the gathered data
    airtable.update_by_field("Name", hostname, data)
    print(f"Updated Airtable row for {hostname} with data: {data}")
else:
    print(f"Invalid data: {data}")
