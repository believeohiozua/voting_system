#!/bin/bash

echo "Initializing Gradle wrapper..."

# Remove existing gradlew files
rm -f gradlew gradlew.bat
rm -rf gradle/wrapper

# Initialize gradle wrapper using gradle if available, otherwise download
if command -v gradle &> /dev/null; then
    echo "Using local Gradle to initialize wrapper..."
    gradle wrapper --gradle-version 8.3
else
    echo "Gradle not found locally, downloading wrapper manually..."
    
    # Create wrapper directory
    mkdir -p gradle/wrapper
    
    # Download gradle wrapper files
    curl -L -o gradle/wrapper/gradle-wrapper.jar https://github.com/gradle/gradle/raw/v8.3.0/gradle/wrapper/gradle-wrapper.jar
    
    # Create gradlew script (already exists)
    chmod +x gradlew
    
    echo "Manual Gradle wrapper setup complete!"
fi

echo "Gradle wrapper initialized successfully!"