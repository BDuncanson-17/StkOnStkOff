#!/bin/bash

# Help function to display usage instructions
display_help() {
    echo "Usage: generate_pem.sh [input] [output]"
    echo "Generate a .pem file from input and save it as output."
}

# Check if help option is passed
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    display_help
    exit 0
fi

# Check if two arguments are provided
if [[ $# -ne 2 ]]; then
    echo "Error: Invalid number of arguments."
    display_help
    exit 1
fi

input="$1"
output="$2"

# Generate .pem file
openssl rsa -pubout -in "$input" -out "$output"

is_package_installed() {
    dpkg -s "$1" >/dev/null 2>&1
}

# Get the array of packages from command-line arguments
packages=("$@")

# Check if any packages were provided
if [[ ${#packages[@]} -eq 0 ]]; then
    echo "No packages provided. Exiting."
    exit 1
