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

# Create build directory
mkdir "$BUILD_DIR"

# Copy source code into build directory
echo "Copying source code to build directory..."
cp -r "$SRC_DIR/"* "$BUILD_DIR/"

# Install dependencies into build directory
echo "Installing dependencies..."
pip install -r requirements.txt --target "$BUILD_DIR/"

# Navigate to build directory and create the zip file
cd "$BUILD_DIR"
echo "Creating zip file..."
zip -r "../$ZIP_FILE" .

# Go back to the root directory
cd ..

# Optionally, remove the build directory after zipping
rm -rf "$BUILD_DIR"

echo "Build process completed successfully. Zip file created: $ZIP_FILE"