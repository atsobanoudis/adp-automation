import pandas as pd

def load_mappings(file_path):
    mappings = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 7:  # Ensure there are exactly 7 parts to unpack
                key, pay_code, customer, payroll_item, service_item, class_, billable = parts
                mappings[key] = {
                    'Pay Code': pay_code,
                    'Customer': customer,
                    'Payroll Item': payroll_item,
                    'Service Item': service_item,
                    'Class': class_,
                    'Billable': billable
                }
    return mappings

def load_subject_mappings(file_path):
    mappings = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:  # Ensure there are exactly 2 parts to unpack
                key, value = parts
                mappings[key] = value
    return mappings

def rename_columns(df):
    new_column_names = {
        'name': 'Customer',
        'subject': 'Service Item',
        'location': 'Class',
        'duration': 'Hours',
        'type': 'Pay Code',
    }
    
    # Rename columns using the mapping defined above
    df_renamed = df.rename(columns=new_column_names, inplace=False)
    
    return df_renamed

def map_pay_code(row, mappings):
    key = row['Pay Code']
    if key in mappings:
        return mappings[key]
    return {}

def apply_subject_mappings(df, mappings):
    def map_subject(service_item):
        service_item_str = str(service_item)  # Convert to string to safely use 'in'
        for key, value in mappings.items():
            if key in service_item_str:
                return value
        return service_item  # Return original service item if no mapping is found
    
    df['Service Item'] = df['Service Item'].apply(map_subject)
    return df

def apply_mappings(df):
    # Load mappings
    pay_code_mappings = load_mappings('adp_format_map.txt')  # Adjust path if necessary
    subject_mappings = load_subject_mappings('subject_code_map.txt')  # Adjust path if necessary

    df = rename_columns(df)

    for index, row in df.iterrows():
        updates = map_pay_code(row, pay_code_mappings)
        for column, value in updates.items():
            if value:  # Only update if value is not empty
                df.at[index, column] = value

    df = apply_subject_mappings(df, subject_mappings)
    df['Class'] = df['Class'].replace('HWY9', 'Hwy9') # Correct HWY9 capitalization
    return df