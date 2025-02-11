#!/usr/bin/env bash

# Create directory for wkhtmltopdf binary
mkdir -p $HOME/.local/bin

# Download the correct precompiled binary for wkhtmltopdf (Linux)
curl -L -o $HOME/.local/bin/wkhtmltopdf https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64

# Check if download was successful
if file $HOME/.local/bin/wkhtmltopdf | grep -q "binary"; then
    echo "Downloaded binary is valid."
else
    echo "Downloaded file is not a valid binary."
    exit 1
fi

# Ensure the binary is executable
chmod +x $HOME/.local/bin/wkhtmltopdf

# Verify installation
$HOME/.local/bin/wkhtmltopdf --version
