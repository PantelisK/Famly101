import re

def parse_cost_data(file_path):
    """Parses the cost data from the given file, retaining order."""
    cost_data = []
    with open(file_path, 'r') as f:
        current_service = None
        current_region = None
        for line in f:
            line = line.strip()
            if line:
                if "USD" in line:  # Cost line
                    cost_match = re.search(r'USD\s*([\d,.]+)', line)
                    cost = float(cost_match.group(1).replace(',', '')) if cost_match else None
                    cost_data.append((current_service, current_region, line, cost))
                else:  # Service or region line
                    if current_service is None or not line.startswith('$'):  # New service
                        current_service = line
                        current_region = None
                    else:  # Region line
                        current_region = line
                        cost_data.append((current_service, current_region, None, None))
    return cost_data

def compare_costs(file1, file2):
    """Compares the cost data and prints in CSV format, excluding zero-cost subservices."""
    data1 = parse_cost_data(file1)
    data2 = parse_cost_data(file2)

    print("Service,Region,Subservice,Detail,Cost_Month1,Cost_Month2,Difference")

    i = 0
    j = 0
    while i < len(data1) or j < len(data2):
        if i < len(data1) and j < len(data2):
            service1, region1, line1, cost1 = data1[i]
            service2, region2, line2, cost2 = data2[j]

            if service1 == service2 and region1 == region2:
                if line1 == line2:
                    if cost1 != 0.0 or cost2 != 0.0:
                        cost1_str = f"{cost1:.2f}" if cost1 is not None else ""
                        cost2_str = f"{cost2:.2f}" if cost2 is not None else ""
                        diff_str = f"{cost2 - cost1:.2f}" if cost1 is not None and cost2 is not None else ""
                        print(f'"{service1}","{region1 if region1 else ""}","{line1.replace("USD ", "") if line1 else ""}","",{cost1_str},{cost2_str},{diff_str}')
                    i += 1
                    j += 1
                else:
                    if line1 and cost1 != 0.0:
                        print(f'"{service1}","{region1 if region1 else ""}","{line1.replace("USD ", "") if line1 else ""}","",{cost1:.2f if cost1 else ""}","","')
                    if line2 and cost2 != 0.0:
                        print(f'"{service2}","{region2 if region2 else ""}","{line2.replace("USD ", "") if line2 else ""}","",,"{cost2:.2f if cost2 else ""}","')
                    i += 1
                    j += 1
            # The following block was modified to include service1 and region1
            elif service1 < service2 or (service1 == service2 and region1 < region2):
                if cost1 != 0.0:
                    print(f'"{service1}","{region1 if region1 else ""}","{line1.replace("USD ", "") if line1 else ""}","",{cost1:.2f if cost1 else ""}","","')
                i += 1
            else:
                if cost2 != 0.0:
                    print(f'"{service2}","{region2 if region2 else ""}","{line2.replace("USD ", "") if line2 else ""}","",,"{cost2:.2f if cost2 else ""}","')
                j += 1
        elif i < len(data1):
            service1, region1, line1, cost1 = data1[i]
            if cost1 != 0.0:
                print(f'"{service1}","{region1 if region1 else ""}","{line1.replace("USD ", "") if line1 else ""}","",{cost1:.2f if cost1 else ""}","","')
            i += 1
        else:
            service2, region2, line2, cost2 = data2[j]
            if cost2 != 0.0:  # Exclude if cost2 is 0
                print(f'"{service2}",{region2 if region2 else ""},"{line2.replace("USD ", "") if line2 else ""}","",,"{cost2:.2f if cost2 else ""}","')
            j += 1


# Example usage:
file1 = 'month1.txt'
file2 = 'month2.txt'
compare_costs(file1, file2)