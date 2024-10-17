#!/usr/bin/env python3
#!/usr/bin/env python3
import os
import re
from collections import defaultdict

def find_terragrunt_files(root_dir):
    terragrunt_files = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == "terragrunt.hcl":
                terragrunt_files.append(os.path.join(subdir, file))
    return terragrunt_files

def extract_source(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        # Check for dependencies or non-empty inputs
        if 'dependency' in content or re.search(r'inputs\s*=\s*{[^}]*[^{}\s]+[^}]*}', content):
            return None
        match = re.search(r'source\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)
    return None

def get_service_name(source):
    # Split the source by '/' and take the last part
    return source.split('/')[-1]

def correlate_services_with_environments(root_dir):
    terragrunt_files = find_terragrunt_files(root_dir)
    service_to_environments = defaultdict(lambda: {'aws': set(), 'syseleven': set()})

    for terragrunt_file in terragrunt_files:
        source = extract_source(terragrunt_file)
        if source:
            service_name = get_service_name(source)
            path_parts = terragrunt_file.split(os.sep)
            if len(path_parts) >= 5:
                environment = os.path.join(path_parts[-4], path_parts[-3])
                # Check for 'environments/aws/SERVICE_NAME' or 'environments/syseleven/SERVICE_NAME'
                if path_parts[-5] == 'environments':
                    if path_parts[-4] == 'aws':
                        service_to_environments[service_name]['aws'].add(environment)
                    elif path_parts[-4] == 'syseleven':
                        service_to_environments[service_name]['syseleven'].add(environment)

    # Convert sets to lists for final output
    for service in service_to_environments:
        service_to_environments[service]['aws'] = list(service_to_environments[service]['aws'])
        service_to_environments[service]['syseleven'] = list(service_to_environments[service]['syseleven'])

    return service_to_environments

if __name__ == "__main__":
    root_directory = "/home/pantelis/Famly/famly-iac"  # Adjust this to your root directory
    service_env_map = correlate_services_with_environments(root_directory)
    for service, environments in service_env_map.items():
        aws_count = len(environments['aws'])
        syseleven_count = len(environments['syseleven'])
        total_count = aws_count + syseleven_count
        aws_envs = ', '.join(environments['aws'])
        syseleven_envs = ', '.join(environments['syseleven'])
        print(f"Service: {service} ({total_count} environments)")
        if aws_envs:
            print(f"  AWS Environments: {aws_envs}")
        if syseleven_envs:
            print(f"  SysEleven Environments: {syseleven_envs}")