import os
from datasets import load_from_disk
import subprocess 

dataset_dict = load_from_disk('/home/grenders95/710/710_project/data/training/hf_datasets/newreqs_clearedfields')

# Access the test dataset
test_dataset = dataset_dict['test']

# Define the root directory where you want to create the subdirectories and clone the repos
root_dir = '/scratch/grenders95/test_repos'
log_file_path = os.path.join(root_dir, 'clone_failures.txt')

# Ensure the root directory exists
os.makedirs(root_dir, exist_ok=True)

# Function to log failures
def log_failure(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

# Iterate through each row in the test dataset
for item in test_dataset:
    org_repo_name = item['org_repo_name']
    # Splitting the org_repo_name at the first underscore to separate orgname and reponame
    split_name = org_repo_name.split('_', 1)
    if len(split_name) == 2:
        orgname, reponame = split_name
        subdir_name = f"{orgname}_{reponame}"
        subdir_path = os.path.join(root_dir, subdir_name)
        repo_url = f"https://github.com/{orgname}/{reponame}.git"
        
        # Create the subdirectory
        os.makedirs(subdir_path, exist_ok=True)
        
        # Attempt to clone the repo into the subdirectory
        try:
            result = subprocess.run(['git', 'clone', repo_url, subdir_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Successfully cloned {repo_url} into {subdir_path}")
        except subprocess.CalledProcessError as e:
            error_message = f"Failed to clone {repo_url} into {subdir_path}: {e.stderr}"
            print(error_message)
            log_failure(error_message)
