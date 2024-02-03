import pandas as pd
from googleapiclient.discovery import build
from modules.authenticate_google_calendar import authenticate_google_calendar
from modules.get_events_for_today import get_events_for_today

def main():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    get_events_for_today(service)

if __name__ == '__main__':
    main()
