from datetime import datetime, timedelta
from .fetch_color_definitions import fetch_color_definitions
import pytz
import pandas as pd

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
    else:
        # Prepare data for dataframe
        data = []

        for event in events:
            start_iso = event['start'].get('dateTime', event['start'].get('date'))
            end_iso = event['end'].get('dateTime', event['end'].get('date'))

            summary = event.get('summary', 'No Title')

            color_id = event.get('colorId', None)
            color_hex = event_colors.get(color_id, {}).get('background', 'default')

            # Convert ISO format to datetime
            start_dt = datetime.fromisoformat(start_iso)
            end_dt = datetime.fromisoformat(end_iso)

            # Check if start and end are on the same day
            date = start_dt.strftime("%Y-%m-%d") if start_dt.date() == end_dt.date() else ""

            # Calculate duration in hours only if date is present
            duration = (end_dt - start_dt).seconds / 3600 if date else None

            data.append({
                'date': date,
                'start': start_dt.strftime("%H:%M"),
                'end': end_dt.strftime("%H:%M"),
                'duration': round(duration, 2) if duration else "",
                'event': summary,
                'color': color_hex
            })

            print(f"{start_dt} to {end_dt}, {event['summary']}, Color: {color_hex}")

        
        df = pd.DataFrame(data, columns=['date', 'start', 'end', 'duration', 'event', 'color'])
        return df

            