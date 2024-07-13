from __future__ import print_function
import base64
import os.path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from get_most_recent_article import extract_pdf_path

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

def create_message_with_attachment(sender, to, subject, message_text, file_path):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    # Attach the file
    with open(file_path, 'rb') as f:
        part = MIMEApplication(f.read(), _subtype='pdf')
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(error)

header = "Your Daily New York Times Update - 13/07/2024"

body = """Dear Pascal,

Good morning!

Attached to this email, you will find today's edition of The New York Times. Start your day with the latest news, insights, and in-depth coverage from around the world."""

path_to_file = extract_pdf_path()

message = create_message_with_attachment('me', 'ortiz.diego81@gmail.com', header, body, path_to_file)

send_message(service, 'me', message)
