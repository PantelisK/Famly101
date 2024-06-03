import csv
import re

# List of known services and regions
known_services = [
    "Relational Database Service", "Elastic Compute Cloud", "Data Transfer",
    "OpenSearch Service", "Simple Storage Service", "CloudFront", "Elastic Transcoder",
    "Savings Plans for AWS Compute usage", "Simple Email Service", "Virtual Private Cloud",
    "Elastic Load Balancing", "ElastiCache", "DynamoDB", "CloudWatch", "Athena", "Config",
    "Lambda", "GuardDuty", "Simple Queue Service", "CloudTrail", "WAF",
    "Elastic Container Service for Kubernetes", "Key Management Service", "Elastic Container Service",
    "Route 53", "Simple Notification Service", "Registrar", "API Gateway", "QuickSight",
    "Lightsail", "Secrets Manager", "Cost Explorer", "EC2 Container Registry (ECR)",
    "Amazon Chime", "SageMaker", "Budgets", "CloudWatch Events", "CodeWhisperer",
    "Cognito", "Elastic File System", "Glue", "S3 Glacier Deep Archive", "Step Functions",
    "Systems Manager", "X-Ray"
]
known_regions = ["EU (Frankfurt)", "EU (Ireland)", "US East (N. Virginia)", "US West (Oregon)"]

def parse_text_to_data(text):
    data = []
    lines = text.split('\n')
    current_service = ''
    current_region = ''
    current_subservice = ''
    current_detail = ''
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line:
            if line in known_services:
                current_service = line
                current_region = ''
                current_subservice = ''
                current_detail = ''
                i += 1
                if i < len(lines) and lines[i].strip().startswith('USD'):
                    cost = float(lines[i].strip().replace('USD ', '').replace(',', ''))
                    if cost != 0.0:
                        data.append({
                            'Service': current_service,
                            'Region': '',
                            'Subservice': '',
                            'Detail': '',
                            'Cost': cost
                        })
            elif line in known_regions:
                current_region = line
                current_subservice = ''
                current_detail = ''
                i += 1
                if i < len(lines) and lines[i].strip().startswith('USD'):
                    cost = float(lines[i].strip().replace('USD ', '').replace(',', ''))
                    if cost != 0.0:
                        data.append({
                            'Service': current_service,
                            'Region': current_region,
                            'Subservice': '',
                            'Detail': '',
                            'Cost': cost
                        })
            elif re.match(r'^\$', line) or "instance used" in line or "Savings Plans" in line or "Instance Hour" in line:
                current_detail = line
                i += 1
                if i < len(lines) and lines[i].strip().startswith('USD'):
                    cost = float(lines[i].strip().replace('USD ', '').replace(',', ''))
                    if cost != 0.0:
                        data.append({
                            'Service': current_service,
                            'Region': current_region,
                            'Subservice': current_subservice,
                            'Detail': current_detail,
                            'Cost': cost
                        })
            else:
                current_subservice = line
                current_detail = ''
                i += 1
                if i < len(lines) and lines[i].strip().startswith('USD'):
                    cost = float(lines[i].strip().replace('USD ', '').replace(',', ''))
                    if cost != 0.0:
                        data.append({
                            'Service': current_service,
                            'Region': current_region,
                            'Subservice': current_subservice,
                            'Detail': '',
                            'Cost': cost
                        })
        i += 1
    return data
def align_and_compare(data1, data2):
    def create_lookup(data):
        lookup = {}
        for entry in data:
            key = (entry['Service'], entry['Region'], entry['Subservice'], entry['Detail'])
            lookup[key] = entry['Cost']
        return lookup
    
    lookup1 = create_lookup(data1)
    lookup2 = create_lookup(data2)
    # Create a dictionary to map services to their indices for sorting
    service_order = {service: idx for idx, service in enumerate(known_services)}
    
    all_keys = sorted(set(lookup1.keys()).union(set(lookup2.keys())), 
                      key=lambda k: (known_services.index(k[0]) if k[0] in known_services else float('inf'), k[1], k[2], k[3]))
    results = []
    
    for key in all_keys:
        cost1 = lookup1.get(key, 0)
        cost2 = lookup2.get(key, 0)
        difference = cost1 - cost2
        if cost1 != 0 or cost2 != 0:
            results.append({
                'Service': key[0],
                'Region': key[1],
                'Subservice': key[2],
                'Detail': key[3],
                'Cost_Month1': cost1,
                'Cost_Month2': cost2,
                'Difference': difference
            })
    
    return results

def output_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Service', 'Region', 'Subservice', 'Detail', 'Cost_Month1', 'Cost_Month2', 'Difference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def process_text(text):
    lines = text.split('\n')
    processed_lines = []
    block_line_count = 0

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            block_line_count += 1
            if block_line_count % 2 == 1 and stripped_line.startswith('USD'):
                processed_lines.append(line.replace('USD', '$USD', 1))
            else:
                processed_lines.append(line)
        else:
            processed_lines.append(line)
            block_line_count = 0  # Reset the block line count for new blocks

    return '\n'.join(processed_lines)

def main():
    # Read and process month1.txt
    with open('month1.txt', 'r') as file1:
        text1 = file1.read()
    processed_text1 = process_text(text1)
    with open('month1.txt', 'w') as file1:
        file1.write(processed_text1)

    # Read and process month2.txt
    with open('month2.txt', 'r') as file2:
        text2 = file2.read()
    processed_text2 = process_text(text2)
    with open('month2.txt', 'w') as file2:
        file2.write(processed_text2)

    # Continue with the rest of the script
    data1 = parse_text_to_data(processed_text1)
    data2 = parse_text_to_data(processed_text2)
    compared_data = align_and_compare(data1, data2)
    output_to_csv(compared_data, 'comparison.csv')

if __name__ == "__main__":
    main()
