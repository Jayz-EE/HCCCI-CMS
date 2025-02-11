#!/usr/bin/env bash

# Download wkhtmltopdf prebuilt binary
curl -L -o wkhtmltopdf.tar.xz https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox-0.12.6-1.bionic_amd64.deb

# Extract and install
dpkg-deb -x wkhtmltopdf.tar.xz $HOME/.local/
mv $HOME/.local/usr/local/bin/wkhtmltopdf $HOME/.local/bin/

# Clean up
rm wkhtmltopdf.tar.xz