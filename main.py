print("WE ARE VENOUMM!");
import os
import base64
from flask import Flask, request, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# Set up Flask app
app = Flask(__name__)

# Set up OAuth credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRETS_FILE = "credentials.json"

# OAuth flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="https://127.0.0.1:8080/oauth2callback"  # Make sure this uses https
)

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def schedule_in(time_string, service, bcc_list):
    """
    Schedules an email based on a human-readable time string like '5 min' or '1 hr'.
    Accepts time in minutes, hours, or days.
    """
    try:
        amount, unit = time_string.split()
        amount = int(amount)
    except ValueError:
        raise ValueError("Invalid time format. Use format like '5 min', '1 hr', or '2 days'.")

    # Calculate the target time based on the unit
    if unit in ["min", "minutes"]:
        schedule_time = datetime.now() + timedelta(minutes=amount)
    elif unit in ["hr", "hour", "hours"]:
        schedule_time = datetime.now() + timedelta(hours=amount)
    elif unit in ["day", "days"]:
        schedule_time = datetime.now() + timedelta(days=amount)
    else:
        raise ValueError("Invalid time unit. Use 'min', 'hr', or 'day'.")

    # Schedule the email at the calculated time
    scheduler.add_job(scheduled_email_task, 'date', run_date=schedule_time, args=[service, bcc_list])
    print(f"Email scheduled for {schedule_time}.")

def scheduled_email_task(service, bcc_list):
    """
    Task to send an email using the Gmail API.
    """
    subject = "Hello from the Gmail API"
    body = "This is a test email sent using the Gmail API and Python."

    # Create the email
    message = MIMEText(body)
    message['bcc'] = ', '.join(bcc_list)  # Set BCC recipients
    message['subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email
    send_message = {'raw': encoded_message}
    service.users().messages().send(userId="me", body=send_message).execute()

def get_bcc_list(file_path):
    """
    Reads email addresses from a text file and returns them as a list.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, 'r') as file:
        emails = file.readlines()

    # Clean up any extra whitespace or newline characters
    return [email.strip() for email in emails if email.strip()]

@app.route('/')
def index():
    # Redirect the user to the OAuth consent screen
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        login_hint="example@something"  # Specify the account to use
    )
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Exchange authorization code for access token
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials

    # Save the credentials for future use
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    # Build the Gmail API service with the obtained credentials
    service = build('gmail', 'v1', credentials=creds)

    # Load BCC list from file
    bcc_list = get_bcc_list('emails.txt')  # File with email addresses
    if not bcc_list:
        return "No BCC recipients found."

    # Schedule an email based on user-defined input (for testing)
    schedule_in("5 min", service, bcc_list)  # Example to schedule an email 5 minutes from now

    return "Email scheduling initiated!"

if __name__ == "__main__":
    # Run the Flask app with SSL (HTTPS)
    app.run(ssl_context=('server.crt', 'server.key'), port=8080)

