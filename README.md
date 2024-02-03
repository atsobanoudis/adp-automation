# Google Calendar Event Extractor

This Python script allows you to extract events from your Google Calendar for the current day, including event color information.

## Setup Instructions

### Required Python Packages

- [google-auth](https://pypi.org/project/google-auth/)
- [google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)
- [google-auth-httplib2](https://pypi.org/project/google-auth-httplib2/)
- [google-api-python-client](https://pypi.org/project/google-api-python-client/)
- pytz
- pandas

### Step 1: Google Cloud Project and API Configuration

1. **Create a Google Cloud Project:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.

2. **Enable the Google Calendar API:**
   - In the navigation menu, go to `APIs & Services > Dashboard`.
   - Click `+ ENABLE APIS AND SERVICES`.
   - Search for `Google Calendar API` and enable it for your project.

3. **Configure OAuth Consent Screen:**
   - In the Google Cloud Console, go to `APIs & Services > OAuth consent screen`.
   - Set up the consent screen that will be shown to your users.

4. **Create Credentials:**
   - In the `Credentials` section, click `Create credentials` and select `OAuth client ID`.
   - Download the JSON file, which contains your client ID and secret.

### Step 2: Running the Script

1. **Place Your Credentials:**
   - Rename your downloaded JSON file to `credentials.json` and place it in the root directory of this project.

2. **Installation:**
   - Install the required Python packages by running `pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`.

3. **Running the Script:**
   - Execute `main.py` to start fetching events for the current day from your Google Calendar.

## Project Structure

- All functional scripts are stored under the `modules` folder in the root directory.
- Separate `.py` scripts for authentication and fetching events are included and imported into `main.py`.

Please follow these instructions carefully to ensure the script works correctly.