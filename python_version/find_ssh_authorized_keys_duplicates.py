import os
import sys
from collections import defaultdict 

# This script needs to be run as root to be able to read all user's .ssh directories
if os.geteuid() != 0:
    print("This script must be run as root.", file=sys.stderr)
    sys.exit(1)

# Get list of all home directories from /etc/passwd
with open('/etc/passwd', 'r') as passwd_file:
    home_dirs = [line.split(':')[5] for line in passwd_file]


for dir in home_dirs:
    authorized_keys_path = os.path.join(dir, '.ssh', 'authorized_keys')

    if os.path.isfile(authorized_keys_path):
        print(f"Processing {authorized_keys_path}.")

        # Read the authorized_keys file, sort, and count duplicates
        keys = defaultdict(int)
        with open(authorized_keys_path, 'r') as auth_keys_file:
            for line in auth_keys_file:
                if (line.strip() != ""):
                    keys[line] += 1

        # Print duplicate keys and their counts
        for key, count in keys.items():
            if count > 1:
                print(f"{key.strip()} is duplicated {count} times")
            # if count == 1:
            #     print(f"{key.strip()} is not duplicated")