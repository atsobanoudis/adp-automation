from modules.authenticate_google_calendar import authenticate_google_calendar
from modules.get_events_for_today import get_events_for_today

def main():
    creds = authenticate_google_calendar()
    get_events_for_today(creds)

if __name__ == '__main__':
    main()
