#!/usr/bin/env bash

# Create directory for wkhtmltopdf binary
mkdir -p $HOME/.local/bin

# Download the correct prebuilt binary for wkhtmltopdf (for Linux)
curl -L -o $HOME/.local/bin/wkhtmltopdf https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.deb

# Extract the binary from the .deb package
ar x $HOME/.local/bin/wkhtmltopdf

# Extract the contents from the tarball inside the .deb
tar -xvf data.tar.xz -C $HOME/.local/bin/

# Clean up unnecessary files
rm wkhtmltopdf data.tar.xz control.tar.gz debian-binary

# Ensure it's executable
chmod +x $HOME/.local/bin/usr/local/bin/wkhtmltopdf

# Verify installation
$HOME/.local/bin/usr/local/bin/wkhtmltopdf --version
