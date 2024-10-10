#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define directories
SRC_DIR="src"
BUILD_DIR="build"
ZIP_FILE="lambda_function.zip"

# Remove existing build directory if it exists
if [ -d "$BUILD_DIR" ]; then
    echo "Removing existing build directory..."
    rm -rf "$BUILD_DIR"
fi

# Remove existing zip file if it exists
if [ -f "$ZIP_FILE" ]; then
    echo "Removing existing zip file..."
    rm "$ZIP_FILE"
fi

# Create the build directory
mkdir -p "$BUILD_DIR"

# Copy your source code from the 'src' directory to the build directory
echo "Copying Lambda function code from src/ to build directory..."
cp -r "$SRC_DIR/"* "$BUILD_DIR/"

# Install dependencies into the build directory
echo "Installing dependencies into build directory..."
pip install -r requirements.txt -t "$BUILD_DIR"

# Navigate to the build directory and create the zip file
cd "$BUILD_DIR"
echo "Creating zip file for the Lambda function..."
zip -r "../$ZIP_FILE" .

# Go back to the root directory
cd ..

# Optionally, remove the build directory after zipping
rm -rf "$BUILD_DIR"

echo "Packaging process completed successfully. Zip file created: $ZIP_FILE"
