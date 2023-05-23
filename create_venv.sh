#!/bin/bash

usage() {
  echo "Usage: $0 [-m|--make] [-d|--delete] [-h|--help]"
  echo
  echo "Options:"
  echo "  -m, --make      Create and activate a Python virtual environment."
  echo "  -d, --delete    Delete the Python virtual environment if it exists."
  echo "  -h, --help      Display help."
  exit 1
}

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -m|--make)
      # Create the virtual environment
      if which python > /dev/null; then
        python -m venv .venv
      elif which python3 > /dev/null; then
        python3 -m venv .venv
      else
        echo "No suitable Python version found."
        exit 1
      fi
      source .venv/bin/activate
      echo "Virtual environment created and activated."
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
      usage
      ;;
    *)
      echo "Invalid option: $key"
      usage
      ;;
  esac

  shift
done

echo "No valid option provided."
usage
