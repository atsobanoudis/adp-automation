import pandas as pd
from googleapiclient.discovery import build
from modules.authenticate_google_calendar import authenticate_google_calendar
from modules.get_events_for_today import get_events_for_today
from modules.timezone import load_timezone

def main():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    timezone = load_timezone()
    df_events_today = get_events_for_today(service, timezone)
    print(df_events_today)

if __name__ == '__main__':
    main()
