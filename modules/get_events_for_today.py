from datetime import datetime, timedelta
from .fetch_color_definitions import fetch_color_definitions
import pytz

def get_events_for_today(service, timezone_str):
    tz = pytz.timezone(timezone_str)
    
    now = datetime.now(tz)
    start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=tz).isoformat()
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=tz).isoformat()

    # Fetch color definitions
    event_colors = fetch_color_definitions(service)

    print('Getting all events for today')
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print('No events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        color_id = event.get('colorId', None)
        color_hex = event_colors.get(color_id, {}).get('background', 'No color specified') if color_id else 'No color specified'
        print(start, event['summary'], f"Color: {color_hex}")
