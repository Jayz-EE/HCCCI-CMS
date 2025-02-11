#!/usr/bin/env bash

# Create directory for wkhtmltopdf
mkdir -p $HOME/.local/bin

# Download the correct prebuilt binary for Linux
curl -L -o $HOME/.local/bin/wkhtmltopdf https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.deb

# Install the downloaded .deb file
dpkg -i $HOME/.local/bin/wkhtmltopdf

# Ensure it's executable
chmod +x $HOME/.local/bin/wkhtmltopdf

# Verify installation
$HOME/.local/bin/wkhtmltopdf --version
