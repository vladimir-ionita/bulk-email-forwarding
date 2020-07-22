import imaplib

IMAP_HOST = "imap.gmail.com"
USERNAME = "email@gmail.com"
PASSWORD = "password"
SEARCH_CRITERIA = "ALL"
VERBOSE = True

# Connect through IMAP
imap_client = imaplib.IMAP4_SSL(IMAP_HOST)
imap_client.login(USERNAME, PASSWORD)

# Fetch messages' ID list
status, _ = imap_client.select("INBOX", readonly=True)
if status != "OK":
    raise Exception("Could not select connect to INBOX.")

status, data = imap_client.search(None, SEARCH_CRITERIA)
if status != "OK":
    raise Exception("Could not search for emails.")

messages_id_list = data[0].decode("utf-8").split(' ')
if VERBOSE:
    print("{} messages were found. Forwarding will start immediately.".format(len(messages_id_list)))
    print("Messages ids: {}".format(messages_id_list))
    print()

