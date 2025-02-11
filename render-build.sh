#!/usr/bin/env bash

# Create directory for wkhtmltopdf binary
mkdir -p $HOME/.local/bin

# Download the precompiled binary for wkhtmltopdf (for Linux)
curl -L -o $HOME/.local/bin/wkhtmltopdf https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64

# Ensure the binary is executable
chmod +x $HOME/.local/bin/wkhtmltopdf

# Verify installation
$HOME/.local/bin/wkhtmltopdf --version
