import imaplib
import email
import smtplib
import time

IMAP_HOST = "imap.gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "email@gmail.com"
PASSWORD = "password"
SEARCH_CRITERIA = "ALL"
VERBOSE = True
FROM_ADDRESS = "email@gmail.com"
TO_ADDRESS = "email@gmail.com"
TIME_DELAY = 5

# Open IMAP connection
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

# Fetch each message data
for msg_id in messages_id_list:
    status, msg_data = imap_client.fetch(msg_id, '(RFC822)')
    if status != "OK":
        raise Exception("Could not fetch email with id {}".format(msg_id))

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            # Change FROM and TO header of the message
            msg.replace_header("From", FROM_ADDRESS)
            msg.replace_header("To", TO_ADDRESS)

            # Open SMTP connection
            smtp_client = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            smtp_client.starttls()
            smtp_client.ehlo()
            smtp_client.login(USERNAME, PASSWORD)

            # Send message
            smtp_client.sendmail(FROM_ADDRESS, TO_ADDRESS, msg.as_bytes())

            # Close SMTP connection
            smtp_client.close()

            # Time delay until next command
            time.sleep(TIME_DELAY)

# Logout
imap_client.close()
imap_client.logout()
