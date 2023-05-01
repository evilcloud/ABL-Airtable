#!/bin/bash

# Update package lists
sudo apt-get update

# Install required packages
sudo apt-get install -y python3 python3-pip git

# Install Python packages
pip3 install airtable-python-wrapper python-dotenv

# Define the repository directory
REPO_DIR="ABL-Airtable"

# Clone the repository or update it if it already exists
if [ -d "$REPO_DIR" ]; then
    cd "$REPO_DIR"
    git pull
else
    git clone https://github.com/evilcloud/ABL-Airtable.git
    cd "$REPO_DIR"
fi

# Make main.py executable
chmod +x main.py
