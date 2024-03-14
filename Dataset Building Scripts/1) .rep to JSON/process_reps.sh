#!/bin/bash

# Loop through all .rep files in the current folder
for rep_file in *.rep; do
    # Generate the corresponding JSON filename
    json_file="${rep_file%.rep}.json"
    
    # Run the command
    ./screp -cmds "$rep_file" > "$json_file"
    
    # Print a message indicating completion for each file
    echo "Processed: $rep_file -> $json_file"
done
