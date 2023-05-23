#!/bin/bash

# Function to check if a command is available

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check if curl is installed
if ! command_exists curl; then
  echo "curl is not installed. Do you want to install it? (y/n)"
  read -r install_curl

  if [[ "$install_curl" =~ ^[Yy]$ ]]; then
    # Install curl
    if command_exists apt; then
      sudo apt update
      sudo apt install -y curl
    elif command_exists yum; then
      sudo yum update
      sudo yum install -y curl
    else
      echo "Error: Could not find a supported package manager (apt or yum) to install curl."
      exit 1
    fi
  else
    echo "curl is required to run this script. Please install curl and run the script again."
    exit 1
  fi
fi

# Check if URL parameter is provided
if [ -z "$4" ]; then
  echo "Error: Missing URL parameter. Usage: upload_ssh.sh -f <file_path> -u <url>"
  exit 1
fi

# Check if file exists
if [ ! -f "$2" ]; then
  echo "Error: File not found: $2"
  exit 1
fi

# Assign parameter values to variables
file_path="$2"
url="$4"

# Send file to the specified URL using curl
curl -X POST -F "file=@$file_path" "$url"