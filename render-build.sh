#!/usr/bin/env bash

# Create directory for wkhtmltopdf binary
mkdir -p $HOME/.local/bin

# Download the correct precompiled binary for wkhtmltopdf (Linux, 64-bit)
curl -L https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.deb -o $HOME/.local/bin/wkhtmltopdf.deb

# Check if download was successful (by checking for deb file)
if [ ! -f "$HOME/.local/bin/wkhtmltopdf.deb" ]; then
  echo "Download failed, exiting."
  exit 1
fi

# Install the .deb package using dpkg (this works in many Linux distros)
dpkg -i $HOME/.local/bin/wkhtmltopdf.deb

# Ensure the binary is executable
chmod +x $HOME/.local/bin/wkhtmltopdf

# Verify installation
$HOME/.local/bin/wkhtmltopdf --version
