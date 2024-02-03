import pandas as pd
from googleapiclient.discovery import build
from modules.authenticate_google_calendar import authenticate_google_calendar
from modules.get_events_for_today import get_events_for_today
from modules.timezone import load_timezone

def main():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    timezone = load_timezone()
    events = get_events_for_today(service, timezone)

    df = pd.DataFrame(events)
    # Convert start and end times to datetime, then calculate duration in hours
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    df['duration'] = (df['end'] - df['start']).dt.total_seconds() / 3600  # Duration in decimal hours
    
    print(df)

if __name__ == '__main__':
    main()
