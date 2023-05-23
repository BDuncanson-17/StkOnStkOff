#!/bin/bash
if debian
# Debian
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
 sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg

# Add the 1Password Apt repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --print-architecture) stable main" | \
 sudo tee /etc/apt/sources.list.d/1password.list

# Add the debsig-verify policy
sudo mkdir -p /etc/debsig/policies/AC2D62742012EA22/
curl -sS https://downloads.1password.com/linux/debian/debsig/1password.pol | \
 sudo tee /etc/debsig/policies/AC2D62742012EA22/1password.pol
sudo mkdir -p /usr/share/debsig/keyrings/AC2D62742012EA22
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
 sudo gpg --dearmor --output /usr/share/debsig/keyrings/AC2D62742012EA22/debsig.gpg

# Install 1Password CLI
sudo apt update && sudo apt install 1password-cli

# Check that 1Password CLI was installed successfully

if yum

sudo rpm --import https://downloads.1password.com/linux/keys/1password.asc

# Configure the repository information
sudo sh -c 'echo -e "[1password]\nname=1Password Stable Channel\nbaseurl=https://downloads.1password.com/linux/rpm/stable/\$basearch\nenabled=1\ngpgcheck=1\nrepo_gpgcheck=1\ngpgkey=\"https://downloads.1password.com/linux/keys/1password.asc\"" > /etc/yum.repos.d/1password.repo'

# Install 1Password CLI
sudo dnf check-update -y 1password-cli && sudo dnf install 1password-cli

# Check that 1Password CLI was installed successfully
op --version


------ if yum

sudo rpm --import https://downloads.1password.com/linux/keys/1password.asc
sudo sh -c 'echo -e "[1password]\nname=1Password Stable Channel\nbaseurl=https://downloads.1password.com/linux/rpm/stable/\$basearch\nenabled=1\ngpgcheck=1\nrepo_gpgcheck=1\ngpgkey=\"https://downloads.1password.com/linux/keys/1password.asc\"" > /etc/yum.repos.d/1password.repo'
sudo dnf check-update -y 1password-cli && sudo dnf install 1password-cli
op --version