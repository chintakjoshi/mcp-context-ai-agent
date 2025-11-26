import os
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarServer:
    def __init__(self):
        self.creds = None
        self.service = None
        self.logger = logging.getLogger(__name__)
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API."""
        token_path = os.path.join('config', 'token.json')
        creds_path = os.path.join('config', 'credentials.json')
        
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(
                        "Please download credentials.json from Google Cloud Console "
                        "and place it in the config directory."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    async def get_upcoming_events(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get upcoming events from Google Calendar."""
        try:
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'id': event.get('id', ''),
                    'summary': event.get('summary', 'No title'),
                    'description': event.get('description', ''),
                    'start': event.get('start', {}),
                    'end': event.get('end', {}),
                    'attendees': event.get('attendees', []),
                    'hangoutLink': event.get('hangoutLink', ''),
                    'status': event.get('status', '')
                })
            
            return formatted_events
        except HttpError as error:
            self.logger.error(f'An error occurred: {error}')
            return []

    async def get_events_for_today(self) -> List[Dict[str, Any]]:
        """Get all events for today."""
        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            time_min = today_start.isoformat() + 'Z'
            time_max = today_end.isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            
            return events
        except HttpError as error:
            self.logger.error(f'An error occurred: {error}')
            return []

# Simple test function
async def test_calendar():
    server = GoogleCalendarServer()
    events = await server.get_upcoming_events(5)
    print("Upcoming events:")
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        print(f"- {event['summary']} at {start_time}")

if __name__ == '__main__':
    asyncio.run(test_calendar())