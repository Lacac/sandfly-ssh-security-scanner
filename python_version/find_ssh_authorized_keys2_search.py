import os
import sys

# This script needs to be run as root to be able to read all user's .ssh directories
if os.geteuid() != 0:
    print("This script must be run as root.", file=sys.stderr)
    sys.exit(1)

# Get list of all home directories from /etc/passwd
with open('/etc/passwd', 'r') as passwd_file:
    home_dirs = [line.split(':')[5] for line in passwd_file]

found = False

for dir in home_dirs:
    authorized_keys2_path = os.path.join(dir, '.ssh', 'authorized_keys2')
    
    if os.path.isfile(authorized_keys2_path):
        print(f'An authorized_keys2 file was found at: {authorized_keys2_path}.')
        found = True

# if not found:
#     print('No authorized_keys2 files found.')