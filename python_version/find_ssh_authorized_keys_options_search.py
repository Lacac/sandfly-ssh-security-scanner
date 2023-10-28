import os
import sys
import re

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
        with open(authorized_keys_path, 'r') as auth_keys_file:
            options_set = []

            for line in auth_keys_file:
                if re.search(r'^(command|environment|agent-forwarding|port-forwarding|user-rc|X11-forwarding|.*,\s*(command|environment|agent-forwarding|port-forwarding|user-rc|X11-forwarding))', line):
                    options_set.append(line.strip())

            if options_set:
                print(f"User with home directory {dir} has options set in their authorized_keys file:")
                print("\n".join(options_set))
