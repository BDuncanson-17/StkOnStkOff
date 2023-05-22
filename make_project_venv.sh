#!/bin/bash

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -m|--make)
      # Create the virtual environment
      python -m venv .venv
      source .venv/bin/activate
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
    *)
      echo "Invalid option: $key"
      exit 1
      ;;
  esac

  shift
done

echo "No valid option provided. Please use either -m or -d."
exit 1



