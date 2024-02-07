import pytz
import platform
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from modules.authenticate_google_calendar import authenticate_google_calendar
from modules.get_events import get_events
from modules.color_map import update_df_with_color_mapping
from modules.timezone import load_timezone
from modules.data_wrangler import data_wrangler
from modules.adp_format_data import apply_mappings
from modules.adp_automation import adp_automation

# Prompt tutor name for ADP notes
def prompt_for_tutor_name(filepath='tutor_name.txt'):
    try:
        with open(filepath, 'r') as file:
            tutor_name = file.read().strip()
    except FileNotFoundError:
        tutor_name = input("Enter your first and last name: ").strip()
        with open(filepath, 'w') as file:
            file.write(tutor_name)
    return tutor_name

# Prompt for desired date
def prompt_for_date():
    system = platform.system()
    if system == 'Windows':
        import msvcrt
        while True:
            print("Do you want to use today's date? (Y/N): ", end='', flush=True)
            key = msvcrt.getch()
            if key in [b'y', b'Y']:
                print("Y")
                return datetime.now()
            elif key in [b'n', b'N']:
                print("N")
                # Directly proceed to input for Windows, as the issue does not affect this OS
                date_input = input("Enter a specific date (M/D): ").strip()
                try:
                    month, day = map(int, date_input.split('/'))
                    year = datetime.now().year  # Assumes current year if not specified
                    return datetime(year, month, day)
                except ValueError:
                    print("Invalid date format. Please enter in M/D format (e.g., 2/1).")
            else:
                print("\nInvalid input. Please enter 'Y' or 'N'.")
    else:
        import termios, sys, tty
        while True:
            print("Do you want to use today's date? (Y/N): ", end='', flush=True)
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            if key in ['y', 'Y']:
                print("Y")
                return datetime.now()
            elif key in ['n', 'N']:
                print("N")
                # Ensure terminal settings are restored before calling input()
                date_input = input("Enter a specific date (M/D): ").strip()
                try:
                    month, day = map(int, date_input.split('/'))
                    year = datetime.now().year
                    return datetime(year, month, day)
                except ValueError:
                    print("Invalid date format. Please enter in M/D format (e.g., 2/1).")
            else:
                print("\nInvalid input. Please enter 'Y' or 'N'.")

def main():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)
    
    # Load timezone
    timezone = load_timezone()
    tz = pytz.timezone(timezone)

    # Prompt user for date choice and adjust time parameters
    tutor_name = prompt_for_tutor_name()
    user_date = prompt_for_date()
    start_of_day = tz.localize(datetime.combine(user_date.date(), datetime.min.time())).isoformat()
    end_of_day = tz.localize(datetime.combine(user_date.date(), datetime.max.time())).isoformat()
    
    df_events_today = get_events(service, timezone, start_of_day, end_of_day)

    # Apply the color-to-type mapping
    try:
        df_events_today = update_df_with_color_mapping(df_events_today)
        print(df_events_today)
    except Exception as e:
        print(f"Failed to apply color mapping: {e}")

    # Manipulate the DataFrame based on additional criteria
    df_processed = data_wrangler(df_events_today, user_date, tutor_name)

    # Format DataFrame 
    df_adp_format = apply_mappings(df_processed)
    print(df_adp_format)

    # Run the ADP filler script
    adp_automation(user_date, df_adp_format)
    
    

if __name__ == '__main__':
    main()