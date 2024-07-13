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

# Import the extract_pdf_paths function from the script that processes files
from get_pdf_not_sended import extract_pdf_paths

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://mail.google.com/']

credentials_path = '/home/diego/htpc-download-box/sendMails/credentials.json'
token_path = '/home/diego/htpc-download-box/sendMails/token.json'


creds = None
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

service_gmail = build('gmail', 'v1', credentials=creds)
service_drive = build('drive', 'v3', credentials=creds)

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

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(error)

current_date = datetime.now().strftime("%d/%m/%Y")

header = f"Votre mise à jour quotidienne du journal Le Monde - {current_date}"

body = f"""🌞 Bonjour !

J'espère que vous allez bien aujourd'hui ! Vous trouverez ci-dessous la dernière édition du jour du journal Le Monde. 📰✨ Ici, chaque article est soigneusement sélectionné pour vous offrir les meilleures perspectives sur les événements mondiaux.

Détente assurée ! 📚🗞️ Découvrez les nouvelles, recevez les informations les plus récentes et explorez les analyses les plus intéressantes.

Bonne lecture et bonne journée ! 📈📰

Cordialement,
Votre équipe de nouvelles quotidiennes

P.S. Vous êtes invité à explorer toutes les dernières publications et à apprécier les moments captivants que chaque numéro apporte.

🗂️ **Archives des articles** : Pour retrouver les numéros précédents et consulter les articles que vous auriez pu manquer, rendez-vous ici : [Archives Le Monde](https://drive.google.com/drive/folders/1bZsuYXpjyStgDHVZ-j_9U6SnijzpQh8A?usp=sharing). Vous y trouverez toutes les éditions passées, prêtes à être découvertes ! 🗞️📦
"""

# Get the list of new file paths
new_file_paths = extract_pdf_paths()

if new_file_paths:
    print(f"{len(new_file_paths)} new files found : {[f.split('/')[-1] for f in new_file_paths]} ")
    file_links = [upload_to_drive(path) for path in new_file_paths]
    message = create_message_with_links('me', 'ortiz.diego81@gmail.com', header, body, file_links)
    # message = create_message_with_links('me', 'pascal.ortiz@gmail.comd', header, body, file_links)
    send_message(service_gmail, 'me', message)


else:
    print("No new files found, no email sent.")
