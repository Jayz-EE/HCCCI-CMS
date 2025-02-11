#!/usr/bin/env bash

# Create a directory for wkhtmltopdf
mkdir -p $HOME/.local/bin

# Download the prebuilt binary directly
curl -L -o $HOME/.local/bin/wkhtmltopdf https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6_linux-generic-amd64.tar.xz

# Extract the binary
tar -xJf $HOME/.local/bin/wkhtmltopdf -C $HOME/.local/bin/

# Ensure it's executable
chmod +x $HOME/.local/bin/wkhtmltopdf

# Verify installation
$HOME/.local/bin/wkhtmltopdf --version
