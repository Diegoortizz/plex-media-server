from __future__ import print_function
import base64
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime
import re
import time
from datetime import datetime

# Import the extract_pdf_paths function from the script that processes files
from get_pdf_not_sended import extract_pdf_paths

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Define the OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://mail.google.com/']

# Paths to the credentials and token files
credentials_path = '/home/diego/htpc-download-box/sendMails/credentials.json'
token_path = '/home/diego/htpc-download-box/sendMails/token.json'

# Initialize credentials
creds = None

# Load existing token if available
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

# Check if credentials are valid; refresh or authenticate if needed
if not creds or not creds.valid:
    try:
        # Attempt to refresh the token if possible
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Authenticate again if no valid credentials are found
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
    except Exception as e:
        print(f"{timestamp()} - Error refreshing or obtaining credentials: {e}")
        # Optionally guide the user through re-authentication if a serious error occurs

    # Save the new credentials for future use
    with open(token_path, 'w') as token:
        token.write(creds.to_json())


service_gmail = build('gmail', 'v1', credentials=creds)
service_drive = build('drive', 'v3', credentials=creds)


# French to English month translation dictionary
french_to_english_months = {
    'Janvier': 'January', 'Février': 'February', 'Mars': 'March',
    'Avril': 'April', 'Mai': 'May', 'Juin': 'June', 'Juillet': 'July',
    'Août': 'August', 'Septembre': 'September', 'Octobre': 'October',
    'Novembre': 'November', 'Décembre': 'December'
}

# Function to extract and convert date from filename
def extract_date(filename):
    # Define regex patterns for date extraction
    date_patterns = [
        r'(\d{1,2}) (\w+) (\d{4})',   # Format: 18 Juillet 2024
        r'(\d{1,2})\.(\d{1,2})\.(\d{4})'  # Format: 25.07.2024
    ]
    
    # Attempt to match and parse the date
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            try:
                if pattern == date_patterns[0]:  # Format with month name
                    day, month_str, year = match.groups()
                    # Translate the French month name to English
                    month = french_to_english_months[month_str.capitalize()]
                    date_str = f'{day} {month} {year}'
                    return datetime.strptime(date_str, '%d %B %Y')
                else:  # Format DD.MM.YYYY
                    day, month, year = match.groups()
                    date_str = f'{day}.{month}.{year}'
                    return datetime.strptime(date_str, '%d.%m.%Y')
            except ValueError:
                print(f"{timestamp()} - Error parsing date for file: {filename}")
    # If no valid date is found, return a max date to sort these last
    return datetime.max

# Function to extract dates
def extract_dates(strings):
    dates = []
    date_pattern = r"\b(\d{2}(?:-\d{2})?\.\d{2}\.\d{4})\b"
    for s in strings:
        match = re.search(date_pattern, s)
        if match:
            dates.append(match.group(1))
    if len(dates) == 0:
        return datetime.now().strftime("%d/%m/%Y")
    elif len(dates) == 1:
        return str(dates[0])
    elif len(dates) == 2:
        return " et ".join(dates)
    else:
        return ", ".join(dates[:-1]) + " et " + dates[-1]

def upload_to_drive(file_path):
    # Folder ID for the "LeMonde" folder
    folder_id = '1bZsuYXpjyStgDHVZ-j_9U6SnijzpQh8A'
    
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]  # Specify the folder ID as the parent
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')
    
    # Upload the file
    file = service_drive.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    
    return (file.get('webViewLink'), file_metadata['name'])

def create_message_with_links(sender, to, subject, message_text, file_links):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    links_text = "\n".join([f"{file_name.replace('.pdf', '')} ici : {link}" for (link, file_name) in file_links])
    full_message_text = f"{message_text}\n\n{links_text}"
    msg = MIMEText(full_message_text)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode()).decode()
    return {'raw': raw_message}

def create_message_with_attachments(sender, to, subject, message_text, file_paths):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    for file_path in file_paths:
        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        with open(file_path, 'rb') as file:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(file.read())
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(timestamp(), ' - Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(error)

current_date = datetime.now().strftime("%d/%m/%Y")

body = f"""🌞 Bonjour !

J'espère que vous allez bien aujourd'hui ! Vous trouverez ci-dessous la dernière édition du jour du journal Le Monde. 

Bonne lecture et bonne journée ! 📈📰

Cordialement,

🗂️ Archives des articles : Pour retrouver les numéros précédents et consulter les articles que vous auriez pu manquer, rendez-vous ici : https://drive.google.com/drive/folders/1bZsuYXpjyStgDHVZ-j_9U6SnijzpQh8A?usp=sharing. 🗞️📦
"""

# Choose whether to attach files or use Google Drive links
USE_GDRIVE_LINKS = True  # Set to False to attach files

mail_to = "pascal.ortiz@gmail.com"
# mail_to = "ortiz.diego81@gmail.com"
# mail_to = "facebookdu81@gmail.com"

# Get the list of new file paths
new_file_paths = extract_pdf_paths()

# Sort the files based on extracted dates
sorted_files = sorted(new_file_paths, key=extract_date)


if new_file_paths:
    print(f"{timestamp()} - {len(new_file_paths)} new files found : {[f.split('/')[-1] for f in new_file_paths]} ")
    header = f"Le Monde - {extract_dates([f.split('/')[-1] for f in new_file_paths])}".replace(".", "/")

    if USE_GDRIVE_LINKS:
        file_links = [upload_to_drive(path) for path in new_file_paths]
        message = create_message_with_links('me', mail_to, header, body, file_links)
    else:
        message = create_message_with_attachments('me', mail_to, header, body, new_file_paths)

    message = create_message_with_links('me', mail_to, header, body, file_links)
    send_message(service_gmail, 'me', message)
else:
    print(f"{timestamp()} - No new files found, no email sent.")