#!/bin/bash
SSD="/mnt/ssd"
PROJECT="groups"

# Run the program
filename="${SSD}/GitHub/python/src/${PROJECT}.py"
if [ ! -f ${filename} ]; then
  echo "ERROR: File not found - ${filename}"
  exit 3
fi
echo ${filename} 

python3.12 ${filename} "$@"

#EOF
