from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import gspread
import datetime

# 1. Set up the Gmail API and Sheets API
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Authenticate using the service account file
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Gmail API setup
gmail_service = build('gmail', 'v1', credentials=credentials)

# Google Sheets API setup
gsheets_client = gspread.authorize(credentials)
sheet = gsheets_client.open("Gmail Data").sheet1  # Replace "Gmail Data" with your sheet name

# 2. Fetch Gmail messages
def fetch_gmail_messages():
    results = gmail_service.users().messages().list(userId='me', maxResults=25).execute()
    messages = results.get('messages', [])
    
    email_data = []

    for msg in messages:
        msg_id = msg['id']
        message = gmail_service.users().messages().get(userId='me', id=msg_id).execute()
        
        headers = message['payload']['headers']
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
        sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
        timestamp = datetime.datetime.fromtimestamp(int(message['internalDate']) / 1000)
        snippet = message.get('snippet', 'No Snippet')

        email_data.append([msg_id, subject, sender, timestamp, snippet])
    
    return email_data

# 3. Write data to Google Sheets
def write_to_google_sheets(data):
    # Clear existing data
    sheet.clear()

    # Add headers
    headers = ["Message ID", "Subject", "Sender", "Timestamp", "Snippet"]
    sheet.append_row(headers)

    # Add email data
    for row in data:
        sheet.append_row(row)

# 4. Main function
if __name__ == '__main__':
    print("Fetching Gmail messages...")
    emails = fetch_gmail_messages()
    print(f"Fetched {len(emails)} messages.")

    print("Writing data to Google Sheets...")
    write_to_google_sheets(emails)
    print("Data written successfully!")
