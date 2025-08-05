#!/bin/bash
SSD="/mnt/ssd"
PROJECT="create-groups"

# Run the program
filename="${SSD}/GitHub/python/src/${PROJECT}.py"
if [ ! -f ${filename} ]; then
  echo "ERROR: File not found - ${filename}"
  exit 3
fi

python3.12 ${filename} "$@"

#EOF
