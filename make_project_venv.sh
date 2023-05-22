#!/bin/bash

function find_python_cmd {
  # Try to find python3
  if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
  # If python3 is not found, try to find python
  elif command -v python &>/dev/null; then
    PYTHON_CMD=python
  else
    echo "Python could not be found. Please install Python."
    exit 1
  fi
}

function update_gitignore {
  # Check if .gitignore exists
  if [ -f ".gitignore" ]; then
    # Check if .venv is already in .gitignore
    if ! grep -q ".venv" ".gitignore"; then
      # Add .venv to .gitignore
      echo ".venv" >> .gitignore
    fi
  else
    # If .gitignore does not exist, create it and add .venv
    echo ".venv" > .gitignore
  fi
}

function print_help {
  echo "Usage: $0 [-m | --make | -d | --delete | -h | --help]"
  echo ""
  echo "Options:"
  echo "-m, --make     Creates a new Python virtual environment in the '.venv' directory and adds '.venv' to the '.gitignore' file."
  echo "-d, --delete   Deletes the Python virtual environment in the '.venv' directory."
  echo "-h, --help     Prints this help message."
}

find_python_cmd

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -m|--make)
      # Create the virtual environment
      $PYTHON_CMD -m venv .venv
      source .venv/bin/activate
      update_gitignore
      pip install .
      exit 0
      ;;
    -d|--delete)
      # Delete the virtual environment
      if [ -d ".venv" ]; then
        rm -rf .venv
        echo "Virtual environment '.venv' deleted."
      else
        echo "Virtual environment '.venv' not found."
      fi
      exit 0
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Invalid option: $key"
      print_help
      exit 1
      ;;
  esac

  shift
done

echo "No valid option provided. Please use either -m or -d."
print_help
exit 1
