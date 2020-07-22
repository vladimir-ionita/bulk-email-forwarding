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

FROM_ADDRESS = "email@gmail.com"
TO_ADDRESS = "email@gmail.com"

FORWARD_TIME_DELAY = 5
EXCEPTION_TIME_DELAY = 60
VERBOSE = True



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
messages_sent = []
while len(messages_sent) < len(messages_id_list):
    msg_id = messages_id_list[len(messages_sent)]

    status, msg_data = imap_client.fetch(msg_id, '(RFC822)')
    if status != "OK":
        raise Exception("Could not fetch email with id {}".format(msg_id))

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            # Change FROM and TO header of the message
            msg.replace_header("From", FROM_ADDRESS)
            msg.replace_header("To", TO_ADDRESS)

            try:
                # Open SMTP connection
                smtp_client = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
                smtp_client.starttls()
                smtp_client.ehlo()
                smtp_client.login(USERNAME, PASSWORD)

                # Send message
                smtp_client.sendmail(FROM_ADDRESS, TO_ADDRESS, msg.as_bytes())
                messages_sent.append(msg_id)
                if VERBOSE:
                    print("Message {} was sent. {} emails from {} emails were forwarded.".format(msg_id,
                                                                                                 len(messages_sent),
                                                                                                 len(messages_id_list)))

                # Close SMTP connection
                smtp_client.close()

                # Time delay until next command
                time.sleep(FORWARD_TIME_DELAY)
            except smtplib.SMTPSenderRefused as exception:
                if VERBOSE:
                    print("Encountered an error! Error: {}".format(exception))
                    print("Messages sent until now:")
                    print(messages_sent)
                    print("Time to take a break. Will start again in {} seconds.".format(EXCEPTION_TIME_DELAY))
                time.sleep(EXCEPTION_TIME_DELAY)
            except smtplib.SMTPServerDisconnected as exception:
                if VERBOSE:
                    print("Server disconnected: {}".format(exception))
            except smtplib.SMTPNotSupportedError as exception:
                if VERBOSE:
                    print("Connection failed: {}".format(exception))
                    print("Messages sent until now:")
                    print(messages_sent)
                    print("Time to take a break. Will start again in {} seconds.".format(EXCEPTION_TIME_DELAY))
                time.sleep(EXCEPTION_TIME_DELAY)
            except smtplib.SMTPDataError:
                raise Exception("Daily user sending quota exceeded.")

if VERBOSE:
    print("Job done. Enjoy your day!")

# Logout
imap_client.close()
imap_client.logout()
