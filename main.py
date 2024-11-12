print("WE ARE VENOM!!!!!!!")  # Print a message on startup to indicate the script is running

import os
import base64
from flask import Flask, request, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Set up Flask app
app = Flask(__name__)

# Define OAuth scopes and credentials file
SCOPES = ['https://www.googleapis.com/auth/gmail.send']  # Scope for sending email through Gmail API
CLIENT_SECRETS_FILE = "credentials.json"  # Path to the OAuth client secrets file

# Set up OAuth flow using client secrets
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="https://127.0.0.1:8080/oauth2callback"  # Redirect URI for OAuth callback (this should match your local address) it should be HTTPS
)

@app.route('/')
def index():
    """
    Home route that initiates the OAuth flow.
    Redirects the user to Google's OAuth consent screen to authorize the app.
    """
    # Generate the authorization URL and state
    authorization_url, state = flow.authorization_url(
        access_type='offline',  # Get a refresh token to use without re-authenticating
        include_granted_scopes='true',  # Include already-granted scopes
        login_hint="something@gmail.com"  # Hint to use a specific Google account
    )
    return redirect(authorization_url)  # Redirect user to Google's authorization page

@app.route('/oauth2callback')
def oauth2callback():
    """
    OAuth callback route that receives the authorization code after user consent.
    Exchanges the authorization code for an access token and saves it.
    Then, sends an email using the Gmail API.
    """
    # Complete the OAuth flow by exchanging the authorization code for an access token
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials  # Get the credentials object containing the access token

    # Save the credentials to a JSON file for future use
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    # Build the Gmail API service with the obtained credentials
    service = build('gmail', 'v1', credentials=creds)
    
    # Call the function to send an email
    send_email(service)
    return "Email sent successfully!"  # Confirm that the email was sent

def send_email(service):
    """
    Sends an email using the Gmail API.
    This function constructs an email message, encodes it, and sends it through the Gmail API.
    """
    to_email = "something@gmail.com"  # Recipient's email address
    subject = "Hello from the Gmail API"  # Subject line for the email
    body = "This is a test email sent using the Gmail API and Python."  # Body of the email

    # Create an email message in MIME format
    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()  # Encode message in base64

    # Send the email message using the Gmail API
    send_message = {'raw': encoded_message}
    service.users().messages().send(userId="me", body=send_message).execute()  # Send the email

if __name__ == "__main__":
    # Run the Flask app with SSL to ensure secure (HTTPS) communication
    app.run(ssl_context=('server.crt', 'server.key'), port=8080)

