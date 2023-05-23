2#!/bin/bash

# Function to display usage information
function display_usage() {
    echo "Usage: $0 [-a|--alias_value <alias_value>] [-c|--command <command>] [-z|--zsh]"
    echo "Append an alias string to the user's profile."
    echo "Options:"
    echo "  -a, --alias_value   The value of the alias."
    echo "  -c, --::       The command associated with the alias."
    echo "  -z, --zsh           Set the alias in the ~/.zshrc file instead of ~/.bashrc."
}

# Check if help parameter is provided
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    display_usage
    exit 0
fi

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--alias_value)
            alias_value=$2
            shift 2
            ;;
        -c|--command)
            command=$2
            shift 2
            ;;
        -z|--zsh)
            zsh_profile=true
            shift
            ;;
        *)
            echo "Error: Invalid option: $1"
            display_usage
            exit 1
            ;;
    esac
done

# Check if both parameters are provided
if [[ -z $alias_value || -z $command ]]; then
    echo "Error: Insufficient or invalid parameters."
    display_usage
    exit 1
fi

# Determine the profile file
if [[ $zsh_profile ]]; then
    profile_file=~/.zshrc
else
    profile_file=~/.bashrc
fi

# Alias string to append
alias_string="alias $alias_value='$command'"

# Check if the alias already exists in the user's profile
if grep -q "$alias_string" "$profile_file"; then
  echo "The alias already exists in the profile."
else
  # Append the alias to the user's profile
  echo "$alias_string" >> "$profile_file"
  echo "Alias added to the profile: $profile_file"
fi

