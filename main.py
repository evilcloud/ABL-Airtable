import json
from dotenv import load_dotenv
from nvidia_handler import get_gpu_info
from system_handler import get_system_data
from data_processor import process_gpu_data, process_system_data
from airtable_handler import get_airtable_instance, update_or_create_airtable_row


def main():
    # Load environment variables
    load_dotenv()

    # Collect data from NVIDIA and system
    gpu_data = get_gpu_data()
    system_data = get_system_data()

    # Process the data
    processed_gpu_data = process_gpu_data(gpu_data)
    processed_system_data = process_system_data(system_data)

    # Combine processed data into a single dictionary
    combined_data = {**processed_gpu_data, **processed_system_data}

    # Interact with Airtable
    airtable_instance = get_airtable_instance()
    hostname = combined_data["Name"]
    update_or_create_airtable_row(airtable_instance, hostname, combined_data)


if __name__ == "__main__":
    main()
