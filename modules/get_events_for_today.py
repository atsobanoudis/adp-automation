from googleapiclient.discovery import build
from datetime import datetime
from .fetch_color_definitions import fetch_color_definitions

def get_events_for_today(credentials):
    service = build('calendar', 'v3', credentials=credentials)
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming events for today')

    # Fetch color definitions
    event_colors = fetch_color_definitions(credentials)

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        color_id = event.get('colorId', None)
        color_hex = event_colors.get(color_id, {}).get('background', 'No color specified') if color_id else 'No color specified'
        print(start, event['summary'], f"Color: {color_hex}")
