import os
import sys


# This script needs to be run as root to be able to read all user's .ssh directories
if os.geteuid() != 0:
    print("This script must be run as root.", file=sys.stderr)
    sys.exit(1)

# Get list of all home directories from /etc/passwd
with open('/etc/passwd', 'r') as passwd_file:
    home_dirs = [line.split(':')[5] for line in passwd_file]


for dir in home_dirs:
    # Check if the .ssh directory exists
    ssh_dir = os.path.join(dir, ".ssh")
    if os.path.exists(ssh_dir) and os.path.isdir(ssh_dir):
        # Find all files in the .ssh directory that contain the word "PRIVATE"
        private_files = []
        
        for root, _, files in os.walk(ssh_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    contents = file.read()
                    if "PRIVATE" in contents:
                        private_files.append(file_path)

        if private_files:
            print(f"User with home directory {dir} has files in their .ssh directory that are likely private keys:")
            for file in private_files:
                print(file)