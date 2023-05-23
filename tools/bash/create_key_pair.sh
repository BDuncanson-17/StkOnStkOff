#!/bin/bash

# Help function to display usage instructions
display_help() {
    echo "Usage: generate_pem.sh [input] [output]"
    echo "Generate a .pem file from input and save it as output."
}


#!/bin/bash

# Check if openssl command is available
if ! command -v openssl >/dev/null 2>&1; then
  echo "openssl command not found. Installing openssl..."

  # Check if apt package manager is available
  if command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y openssl
  # Check if yum package manager is available
  elif command -v yum >/dev/null 2>&1; then
    sudo yum update
    sudo yum install -y openssl
  else
    echo "Error: Could not find a supported package manager (apt or yum) to install openssl."
    exit 1
  fi
fi

# Output file paths
private_key_file="private_key.pem"
public_key_file="public_key.pem"

# Key size (in bits)
key_size=2048

# Check if private key file already exists
if [ -f "$private_key_file" ]; then
  echo "Private key file already exists: $private_key_file"
  exit 1
fi

# Generate the key pair
openssl genpkey -algorithm RSA -out "$private_key_file" -pkeyopt rsa_keygen_bits:"$key_size"
openssl rsa -pubout -in "$private_key_file" -out "$public_key_file"

# Set appropriate permissions on private key file
chmod 600 "$private_key_file"

echo "Public-private key pair generated:"
echo "Private key: $private_key_file"
echo "Public key: $public_key_file"