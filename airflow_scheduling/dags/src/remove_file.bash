#!/bin/bash

# Check if the file exists before removing
if [ -f "$FILE_PATH" ]; then
    rm "$FILE_PATH" && echo "Successfully removed $FILE_PATH" || echo "Failed to remove $FILE_PATH"
else
    echo "File $FILE_PATH does not exist. Skipping removal."
fi
