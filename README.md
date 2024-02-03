# AJ/ADP Automation

AJ/ADP Automation is a Python-based tool designed to automate the process of fetching, filtering, and processing event data from Google Calendar. It allows users to dynamically select dates for event retrieval, apply custom color mappings to event types, and perform various data wrangling tasks such as consolidating event durations and categorizing events based on custom criteria.

## Features

- Fetch events from Google Calendar for specific or current dates.
- Apply custom color mappings to events for easy categorization.
- Filter out specified events and cancellations.
- Consolidate event durations and notes based on type.
- Automatically handle tutor-specific event formatting and notes.
- Summarize total hours spent per event type.

## Installation

### Clone the Repository

Clone the repository to your local machine and navigate into the project directory.

### Set Up a Virtual Environment

Create and activate a virtual environment for the project.

### Install Dependencies

Install the necessary Python dependencies:
- pandas
- pytz
- google-api-python-client
- google-httplib2
- google-oauthlib

These can be installed using pip.

### Google Calendar API Credentials

Enable the Google Calendar API and download your `credentials.json` file to the project root, following Google's Python Quickstart guide.

## Usage

1. Configuration: Ensure `credentials.json` is in the project root. Customize `color_mapping.txt` and `ignore_events.txt` as needed.
2. Running the Script: Execute the script and follow the on-screen prompts to select the desired date and input the tutor's name.
3. View Processed Events: The script outputs the processed events directly to the terminal.

## Project Structure

- `main.py`: Entry point, handling user inputs and coordinating the processing.
- `modules/`: Contains all modular scripts used in the project, including authentication, event fetching, color mapping, and data processing.
- `color_mapping.txt`: Defines custom mappings from event colors to types.
- `ignore_events.txt`: Lists event titles to be excluded from processing.