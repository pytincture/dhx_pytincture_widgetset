#!/bin/bash

# Check if output file parameter is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 output_file"
    echo "Example: $0 all_inits.txt"
    exit 1
fi

OUTPUT_FILE="$1"

# Clear the output file if it already exists
> "$OUTPUT_FILE"

# Find all __init__.py files recursively and process them
find . -type f -name "__init__.py" | while read -r init_file; do
    # Add a header for each file to show where it came from
    echo -e "\n\n# ========== $init_file ==========\n" >> "$OUTPUT_FILE"
    
    # Append the file contents
    cat "$init_file" >> "$OUTPUT_FILE"
done

# Check if any __init__.py files were found
if [ $(wc -l < "$OUTPUT_FILE") -eq 0 ]; then
    echo "No __init__.py files found in the current directory tree."
    exit 0
else
    echo "Successfully collected all __init__.py files into $OUTPUT_FILE"
    echo "Found $(grep -c "# ========== " "$OUTPUT_FILE") __init__.py files."
fi
