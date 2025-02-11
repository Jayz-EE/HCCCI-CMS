#!/usr/bin/env bash

# Create directory for wkhtmltopdf binary
mkdir -p $HOME/.local/bin

# Download the tarball for wkhtmltopdf (Linux, 64-bit)
curl -L https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.tar.xz -o $HOME/.local/bin/wkhtmltopdf.tar.xz

# Extract the tarball to the appropriate directory
tar -xvJf $HOME/.local/bin/wkhtmltopdf.tar.xz -C $HOME/.local/bin/

# The extracted directory should be located in $HOME/.local/bin/wkhtmltox/
# Ensure the binary is executable and located correctly
chmod +x $HOME/.local/bin/wkhtmltox/bin/wkhtmltopdf

# Verify installation
$HOME/.local/bin/wkhtmltox/bin/wkhtmltopdf --version
