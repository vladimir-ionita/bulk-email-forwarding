import imaplib

imap_host = "imap.gmail.com"
username = "email@gmail.com"
password = "password"
search_criteria = "ALL"

# Connect through IMAP
imap_client = imaplib.IMAP4_SSL(imap_host)
imap_client.login(username, password)

# Fetch messages' ID list
status, _ = imap_client.select("INBOX", readonly=True)
if status != "OK":
    raise Exception("Could not select connect to INBOX.")

status, data = imap_client.search(None, search_criteria)
if status != "OK":
    raise Exception("Could not search for emails.")

messages_id_list = data[0].decode("utf-8").split(' ')
