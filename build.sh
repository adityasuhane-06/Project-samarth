#!/usr/bin/env bash
# Render build script

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r src/requirements.txt

echo "Build completed successfully!"
