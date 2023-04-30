from airtable import Airtable
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")


def get_airtable_instance():
    return Airtable(BASE_ID, TABLE_NAME, api_key=API_KEY)


def update_or_create_airtable_row(airtable_instance, hostname, data):
    # Check if a row with the matching hostname exists
    existing_rows = airtable_instance.search("Name", hostname)

    if existing_rows:
        # Update the existing row
        row_id = existing_rows[0]["id"]
        airtable_instance.update(row_id, data)
    else:
        # Create a new row
        airtable_instance.insert(data)


if __name__ == "__main__":
    airtable_instance = get_airtable_instance()

    # Example usage of update_or_create_airtable_row()
    hostname = "example_hostname"
    data = {
        "Name": hostname,
        "Hashrate": 456,
        "Content": "3 x 3080 Ti, 2 x 3060",
        "Reboot": 7200,
        "Power draw": 850,
    }
    update_or_create_airtable_row(airtable_instance, hostname, data)
