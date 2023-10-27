import os
import sys

# Set to your limit for excessive keys.
MAX_KEY = 10

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

        count_key = 0
        # Count the number of key (line)
        with open(authorized_keys_path, 'r') as auth_keys_file:
            for line in auth_keys_file:
                if (line.strip() != ""):
                    count_key += 1
        
        if (count_key > MAX_KEY):
            print(f"User with home directory {dir} has {count_key} keys in the authorized_keys file")
        else: 
            print(f"User with home directory {dir} has {count_key} keys")