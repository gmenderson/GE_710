import os
import subprocess
import sys

root_dir = '/scratch/grenders95/test_repos'

# Path for the log file
log_file_path = os.path.join(root_dir, 'venv_install_failures.txt')

# Function to log failures
def log_failure(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

# Iterate over each subdirectory in the root directory
for subdir_name in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir_name)
    if os.path.isdir(subdir_path):
        # Define the path for the virtual environment
        venv_path = os.path.join(subdir_path, 'venv')
        requirements_path = os.path.join(subdir_path, 'requirements.txt')
        
        try:
            # Create the virtual environment
            subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            activate_script = 'bin/activate' if os.name != 'nt' else 'Scripts\\activate'
            activate_path = os.path.join(venv_path, activate_script)
            
            # Check if requirements.txt exists
            if os.path.exists(requirements_path):
                # Install dependencies from requirements.txt
                subprocess.run([f"source {activate_path} && pip install -r {requirements_path}"], shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
            else:
                print(f"No requirements.txt found in {subdir_path}, skipping dependency installation.")
            
        except subprocess.CalledProcessError as e:
            error_message = f"{subdir_name}: failed to install venv or dependencies\n{e.stderr}"
            log_failure(error_message)
