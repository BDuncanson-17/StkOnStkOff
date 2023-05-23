#!/bin/bash

check_installed_packages() {
  declare -a packages=("${!1}")  # Retrieve the array of packages from the first argument

  declare -a not_installed=()   # Initialize an empty array to store the not installed packages

  for package in "${packages[@]}"; do
    if ! command -v "$package" >/dev/null 2>&1; then
      not_installed+=("$package")   # Add the package to the not installed array
    fi
  done

  echo "${not_installed[@]}"   # Print the not installed packages
}

# Function to display help message
display_help() {
  echo "Usage: ./check_packages.sh [OPTIONS] package1 package2 package3 ..."
  echo "Check if packages are installed on the system."
  echo ""
  echo "Options:"
  echo "  -h, --help   Display this help message and exit."
}

# Check if -h or --help option is provided
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  display_help
  exit 0
fi

# Check if packages array is provided as command-line arguments
if [ $# -eq 0 ]; then
  echo "Error: No packages specified. Usage: ./check_packages.sh package1 package2 package3 ..."
  exit 1
fi

# Convert command-line arguments to an array
declare -a packages=("$@")

not_installed_packages=($(check_installed_packages packages[@]))

sudo apt update && sudo apt upgrade -y

sudo apt install -y packages[@]

