# Gmail API Email Scheduler

This project allows you to send emails using the Gmail API and schedule them based on user-defined time intervals. The emails are sent with BCC recipients read from a text file. The project uses Flask for the web application and Google OAuth for authentication.

## Features
- OAuth 2.0 authentication with Gmail API.
- Sends emails to multiple recipients using BCC.
- Schedule emails based on a human-readable time format (e.g., "5 min", "1 hr").
- Local Flask server running with HTTPS support.

## Project Structure

Your directory structure should look like this:

```
project-directory/
│
├── credentials.json      # OAuth credentials downloaded from Google Cloud
├── server.crt            # SSL certificate for HTTPS
├── server.key            # SSL key for HTTPS
├── token.json            # (Generated after OAuth authorization)
├── app.py                # Main Python script
└── requirements.txt      # Package dependencies
```

## Prerequisites

Before you can run this project, ensure that you have the following set up:

### 1. **Set Up Google Cloud Console**

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Select **Create Project** (or select an existing project if you have one).

2. **Enable the Gmail API**:
   - Go to **[APIs & Services > Library](https://console.cloud.google.com/apis/library)** in the Cloud Console.
   - Search for "Gmail API" and click **Enable**.

3. **Create OAuth 2.0 Credentials**:
   - Go to **[APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)**.
   - Click **Create Credentials** > **OAuth client ID**.
   - Set up the **OAuth consent screen** (you’ll need to enter some basic information).
   - Under **Application type**, select **Web application**.
   - In **Authorized redirect URIs**, add:
     - `https://127.0.0.1:8080/oauth2callback` (this URI should match the redirect URI in your code).
   - After creation, download the `credentials.json` file and save it in your project directory.

4. **Set Up Test Users** (if app is in "Testing" mode):
   - Go to the **[OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)**.
   - Add your Google account (and others you want to test with) under **Test users**.

### 2. **Set Up Local Environment**

#### Install Required Python Packages

To handle dependencies, create a `modules.txt` file with the following content:

```plaintext
Flask
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
APScheduler
```

Then install the packages with:

```bash
pip install -r modules.txt
```

#### Generate SSL Certificates for HTTPS

For HTTPS support, you’ll need SSL certificates:

1. Run this command to generate an SSL certificate (`server.crt`) and key (`server.key`):

   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
   ```

2. Save `server.crt` and `server.key` in your project folder.

### 3. **Create Project File Structure**

Ensure that your project has the following file structure:

```
project-directory/
│
├── credentials.json      # OAuth credentials downloaded from Google Cloud
├── server.crt            # SSL certificate for HTTPS
├── server.key            # SSL key for HTTPS
├── token.json            # (Generated after OAuth authorization)
├── app.py                # Main Python script
└── requirements.txt      # Package dependencies
```

### 4. **Code Setup in `app.py`**

Your main Python script (`app.py`) includes functionality to:

- Handle OAuth 2.0 authorization with Google.
- Read BCC recipients from a file (`emails.txt`).
- Send emails using Gmail API.
- Schedule emails at a user-defined time.

### 5. **Run the Flask App**

To start the app with HTTPS support, open your terminal, navigate to your project directory, and run:

```bash
python app.py
```

The app will start on `https://127.0.0.1:8080`.

### 6. **Authorize the App**

When you visit the local host website, you'll be redirected to Google’s OAuth consent screen. Once authorized, the app will be able to send emails via the Gmail API.

### 7. **Files to Include in GitHub Repository**

Ensure you include the following files in your GitHub repository:

- **main.py**: Your main Flask and Gmail API code.
- **modules.txt**: Python package dependencies.
- **README.md**: A description of the project setup, including links to required resources.

### 8. **Sensitive Files to Exclude from GitHub**

Make sure to exclude the following files from your GitHub repository:

- `credentials.json`
- `server.crt` and `server.key`
- `token.json`

Add these entries to your `.gitignore` file:

```plaintext
credentials.json
server.crt
server.key
token.json
```

For more information about using `.gitignore`, visit the [GitHub Documentation on Ignoring Files](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files).

---

### 9. **Notes**

- The email addresses to be added in the BCC field are read from a text file (`emails.txt`), which should have one email address per line.
- The email sending can be scheduled in intervals (e.g., "5 min", "1 hr", or "2 days") using the Flask server and the APScheduler library.
