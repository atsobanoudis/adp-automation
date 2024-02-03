import pandas as pd
import numpy as np

def load_ignore_events(filepath='ignore_events.txt'):
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File {filepath} not found. No events will be ignored.")
        return []

def remove_cancelled_events(df):
    return df[df['type'] != 'cancel']

def verify_dates(df, user_date):
    if not all(df['date'] == user_date.strftime("%Y-%m-%d")):
        raise ValueError("All events must be for the user's inputted date.")

# Handle break entries
def consolidate_breaks(df):
    df.loc[(df['type'] == 'break') & (df['duration'] < 0.5), 'duration'] = 0.17
    break_rows = df[df['type'] == 'break']
    if not break_rows.empty:
        note_val = 'break' if len(break_rows) == 1 else 'breaks'
        consolidated_duration = break_rows['duration'].sum()
        new_row = pd.DataFrame({'duration': [consolidated_duration], 'note': [note_val], 'type': ['break']})
        df = pd.concat([df[df['type'] != 'break'], new_row], ignore_index=True)
    return df

# Handle admin entries
def consolidate_admin(df):
    # Separate 'Admin' events for 'solve + emails'
    admin_solve_emails = df[(df['type'] == 'admin') & (df['event'] == 'Admin')]
    solve_duration = admin_solve_emails['duration'].sum() if not admin_solve_emails.empty else 0

    # Handle other 'admin' events
    other_admins = df[(df['type'] == 'admin') & (df['event'] != 'Admin')]
    if not other_admins.empty:
        other_admins['note'] = other_admins['event']
        other_duration = other_admins['duration'].sum()
        other_notes = ' + '.join(other_admins['note'].unique())
    else:
        other_duration = 0
        other_notes = ''

    # Consolidate all 'admin' events
    total_duration = solve_duration + other_duration
    notes = 'solve + emails' + (' + ' + other_notes if other_notes else '')

    # Remove old 'admin' rows and append consolidated info
    df = df[df['type'] != 'admin']
    consolidated_admin_row = pd.DataFrame({
        'duration': [total_duration], 
        'note': [notes], 
        'type': ['admin']
    })
    df = pd.concat([df, consolidated_admin_row], ignore_index=True)
    
    return df

# Handle tutor entries
def parse_tutor_info(df):
    for index, row in df[df['type'] == 'tutor'].iterrows():
        event_parts = row['event'].split(' - ')
        if len(event_parts) == 2:
            name_part, subject_location_part = event_parts
            # Split name part and handle cases with different numbers of names
            names = name_part.split()
            if len(names) >= 2:
                first_name, last_name = names[0], ' '.join(names[1:])  # Handles multiple last names
            else:
                # Default or placeholder values if format is unexpected
                first_name, last_name = name_part, "Unknown"

            subject_location = subject_location_part.strip().rstrip(')').split(' (')
            if len(subject_location) == 2:
                subject, location = subject_location
            else:
                subject, location = "Unknown", "Unknown"

            df.at[index, 'name'] = f"{last_name} {first_name}"
            df.at[index, 'subject'] = subject
            df.at[index, 'location'] = location
    return df
def add_tutor_note_info(df, tutor_name):
    for index, row in df[df['type'] == 'tutor'].iterrows():
        df.at[index, 'note'] = tutor_name
    return df

def print_total_hours(df):
    # Group by 'type' and sum 'duration' for each group
    total_hours = df.groupby('type')['duration'].sum()

    print("\nTotal hours")
    for type_, hours in total_hours.items():
        print(f"{type_}: {hours:.2f}")

def data_wrangler(df, user_date, tutor_name):
    ignored_events = load_ignore_events()
    df = df[~df['event'].isin(ignored_events)]
    
    verify_dates(df, user_date)

    # Remove specified columns
    df.drop(['date', 'start', 'end'], axis=1, inplace=True)

    # Insert 'note' column
    df.insert(len(df.columns), 'note', np.nan)

    df = remove_cancelled_events(df)
    df = consolidate_breaks(df)
    df = consolidate_admin(df)
    df = parse_tutor_info(df)
    df = add_tutor_note_info(df, tutor_name)

    print_total_hours(df)

    return df
