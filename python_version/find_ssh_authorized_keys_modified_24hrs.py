import os
import sys
import time

# 24 hours in seconds. Adjust to suit.
SECONDS_LIMIT = 86400  # 24 hours in seconds

# This script needs to be run as root to be able to read all user's .ssh directories
if os.geteuid() != 0:
    print("This script must be run as root.", file=sys.stderr)
    sys.exit(1)

# Get list of all home directories from /etc/passwd
with open('/etc/passwd', 'r') as passwd_file:
    home_dirs = [line.split(':')[5] for line in passwd_file]


# Get the current time in seconds since the epoch
now = int(time.time())

for dir in home_dirs:
    authorized_keys_path = os.path.join(dir, ".ssh", "authorized_keys")
    if os.path.exists(authorized_keys_path) and os.path.isfile(authorized_keys_path):
        # Get the last modification time of the file
        mtime = int(os.path.getmtime(authorized_keys_path))

        # Calculate the difference in seconds between now and the file's mtime
        diff = now - mtime

        # If the file was modified in the last 24 hours (86400 seconds)
        if diff <= SECONDS_LIMIT:
            print(f"User with home directory {dir} has modified their authorized_keys file in the last 24 hours.")