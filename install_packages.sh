#!/bin/bash

# Loop through each line in requirements.txt and install it
while IFS= read -r package; do
    pip install --no-cache-dir "$package" || true
done < /root/requirements.txt

