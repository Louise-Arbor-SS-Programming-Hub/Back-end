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

---

### 2. **Set Up Local Environment**

#### Install Required Python Packages

To handle dependencies, create a `modules.txt` file with the following content:

```plaintext
Flask
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
```

Then install the packages with:

```bash
pip install -r requirements.txt
```

To learn more about these packages:
   - [Flask](https://flask.palletsprojects.com/) – for building web applications in Python.
   - [google-auth](https://google-auth.readthedocs.io/) – for Google’s OAuth 2.0 authorization.
   - [google-auth-oauthlib](https://google-auth-oauthlib.readthedocs.io/) – to simplify OAuth 2.0 with Google APIs.
   - [google-auth-httplib2](https://google-auth.readthedocs.io/en/stable/httplib2.html) – HTTP libraries used with Google Auth.
   - [google-api-python-client](https://developers.google.com/api-client-library/python) – Google API client for Python.

#### Generate SSL Certificates for HTTPS

For HTTPS support, you’ll need SSL certificates:

1. Run this command to generate an SSL certificate (`server.crt`) and key (`server.key`):

   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
   ```

   Learn more about generating SSL certificates here: [OpenSSL Documentation](https://www.openssl.org/docs/).

   Download SSL here: [SSL](https://slproweb.com/products/Win32OpenSSL.html)

2. Save `server.crt` and `server.key` in your project folder.

---

### 3. **Create Project File Structure**

Your directory structure should look like this:

```plaintext
project-directory/
│
├── credentials.json      # OAuth credentials downloaded from Google Cloud
├── server.crt            # SSL certificate for HTTPS
├── server.key            # SSL key for HTTPS
├── token.json            # (Generated after OAuth authorization)
├── app.py                # Main Python script
└── requirements.txt      # Package dependencies
```

### 4. **Code Setup in `app.py` or `main.py`**

You already have the code with comments explaining each section.

---

### 5. **Run the Flask App**

To start the app with HTTPS support, open your terminal, navigate to your project directory, and run:

```bash
python main.py
```

Access the app in your browser at whatever your local host link is.

### 6. **Authorizing the App**

When you go to the local host website, you should be directed to Google’s OAuth consent screen to authorize the app. Once authorized, the app will be able to send an email through the Gmail API.

---

### 7. **Files for GitHub**

Ensure you include the following files in your GitHub repository:

- **app.py**: Your main Flask and Gmail API code.
- **requirements.txt**: Python package dependencies.
- **README.md**: A description of the project setup, including links to required resources.

# Sensitive files to exclude from GitHub:

- `credentials.json`
- `server.crt` and `server.key`
- `token.json`

Add these entries in your `.gitignore` file:

```plaintext
credentials.json
server.crt
server.key
token.json
```

You can learn more about GitHub’s `.gitignore` here: [GitHub Documentation on Ignoring Files](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files).
