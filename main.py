import imaplib

imap_host = "imap.gmail.com"
username = "email@gmail.com"
password = "password"

# Connect through IMAP
imap_client = imaplib.IMAP4_SSL(imap_host)
imap_client.login(username, password)
