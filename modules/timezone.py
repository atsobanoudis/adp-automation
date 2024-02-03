import pytz

def get_user_timezone():
    """Prompt the user for their timezone and save it."""
    while True:
        user_timezone = input("Please enter your timezone (e.g., 'America/New_York'): ")
        if user_timezone in pytz.all_timezones:
            with open('user_timezone.txt', 'w') as f:
                f.write(user_timezone)
            return user_timezone
        else:
            print("Invalid timezone. Please try again.")

def load_timezone():
    """Load the user's timezone from file, or prompt if not found."""
    try:
        with open('user_timezone.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return get_user_timezone()