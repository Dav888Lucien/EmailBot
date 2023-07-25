import imaplib
import json
import smtplib
from email.parser import BytesParser
from email.utils import parseaddr
import dateparser
import re

import spacy
from spacy import Language

# Define client credentials get from our database
client_credentials = {
    'highstrokepiston@gmail.com': {
        'userAccount': 'highstrokepiston@gmail.com',
        'userPassword': 'Test@123321'
        # pass these information to json file for automation login
    },
    'linluxiang2000@gmail.com': {
        'username': 'luxiang lin',
        'userPassword': 'Test'
    },
    'ramyasri2063@gmail.com': {
        'userAccount': 'bc2023test@grr.la',
        'userPassword': 'canada10'
    },
    # Add more client credentials as needed
}

# set system email
IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_ADDRESS = 'ramyasri2063@gmail.com'
PASSWORD = 'higncgwgbzjvcnog'

# connect IMAP service
imap_server = imaplib.IMAP4_SSL(IMAP_SERVER)
imap_server.login(EMAIL_ADDRESS, PASSWORD)
imap_server.select('INBOX')

#  connect SMTP service
# smtp_server = smtplib.SMTP(SMTP_SERVER)
# smtp_server.starttls()
# smtp_server.login(EMAIL_ADDRESS, PASSWORD)

# load spaCy English Model
nlp: Language = spacy.load('en_core_web_sm')

# get unread list
response, email_ids = imap_server.search(None, 'UNSEEN')
email_ids = email_ids[0].split()

# Iterate over each unread email
for email_id in email_ids:
    response, email_data = imap_server.fetch(email_id, '(RFC822)')
    msg = BytesParser().parsebytes(email_data[0][1])
    # extract sender email
    sender_name, sender_email = parseaddr(msg['From'])

    # print("Sender Email:", sender_email) test sender email

    # Verify if the sender's email exists in the client credentials dictionary
    if sender_email in client_credentials:
        client = client_credentials[sender_email]
        email_json = {
            'Subject': msg['Subject'],
            'From': sender_email,
            'To': msg['To'],
            'Date': msg['Date'],
            'Body': '',
            'Nouns': [],
            'Verbs': [],
            'ClientCredentials': client  # Include client credentials in the JSON data
        }

        # Extract email body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_json['Body'] = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            email_json['Body'] = msg.get_payload(decode=True).decode('utf-8')

        # Perform POS tagging and extract nouns and verbs
        doc = nlp(email_json['Body'])
        for token in doc:
            if token.pos_ == 'NOUN':
                email_json['Nouns'].append(token.text)
            elif token.pos_ == 'VERB':
                email_json['Verbs'].append(token.text)

        # Extract month and year from email body using regular expressions
        month_regex = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
        year_regex = r'\b\d{4}\b'
        # Extract the email date using regular expressions

        date_regex = r'\b(\d{1,2})\s(?:st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b'
        # Extracted month
        month_matches = re.findall(month_regex,  email_json['Body'], re.IGNORECASE)

        # Extracted year
        year_matches = re.findall(year_regex,  email_json['Body'], re.IGNORECASE)

        #Extracted date
        date_match = re.search(r'on\s+(\d+)(?:st|nd|rd|th)\s+(\w+)\s+(\d+)', email_json['Body'])
        day = int(date_match.group(1))

        data = {
            "Month": month_matches,
            "Year": year_matches,
            "Date": day
        }

        email_json['Document Request Date'] = data

        # Convert to JSON format
        json_data = json.dumps(email_json, indent=4, ensure_ascii=False)
        json_filename = f'email_{email_id}.json'
        with open(json_filename, 'w') as json_file:
            json_file.write(json_data)

        print(f'Email {email_id} converted to {json_filename}')
    else:
        print(f'Email {email_id} is not from a recognized client')

    # Mark email as read
    imap_server.store(email_id, '+FLAGS', '\\Seen')

# close connection
imap_server.close()
imap_server.logout()
# smtp_server.quit()
