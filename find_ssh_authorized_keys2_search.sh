#!/bin/bash
#
# This script searches for any SSH authorized_keys2 files in any user's home directory.
#
# (c) 2023 Sandfly Security
# https://www.sandflysecurity.com
#
# MIT Licensed

# This script needs to be run as root to be able to read all user's .ssh directories
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root." 1>&2
   exit 1
fi

# Get list of all home directories
home_dirs=$(awk -F':' '{ print $6 }' /etc/passwd)


found=false
for dir in $home_dirs; do
    # Check if the authorized_keys2 file exists
    if [ -f $dir/.ssh/authorized_keys2 ]; then
        echo "An authorized_keys2 file was found at: $dir/.ssh/authorized_keys2."
        found=true
    fi
done

if [ "$found" = false ]; then
   echo "No authorized_keys2 files found "
fi
