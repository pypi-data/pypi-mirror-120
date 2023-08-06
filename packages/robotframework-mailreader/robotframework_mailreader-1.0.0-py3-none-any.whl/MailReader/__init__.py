from robot.api.deco import keyword, library
import smtplib
from email.message import EmailMessage
import email
from email.header import decode_header
import imaplib

@library
class MailReader(object):
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'

    @keyword('Read The Last Email')
    def read_last_email(self, username, password):

        def clean(text):
            # clean text for creating a folder
            return "".join(c if c.isalnum() else "_" for c in text)

        # number of top emails to fetch
        N = 1

        # create an IMAP4 class with SSL, use your email provider's IMAP server
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        imap.login(username, password)

        # select a mailbox (in this case, the inbox mailbox)
        # use imap.list() to get the list of mailboxes
        status, messages = imap.select("INBOX")

        # total number of emails
        messages = int(messages[0])

        for i in range(messages, messages-N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):

                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):

                        subject = subject.decode(encoding)

                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    print("Subject:", subject)
                    print("From:", From)

                    # if the email message is multipart
                    if msg.is_multipart():

                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print(body)
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            print(body)

        imap.close()
        imap.logout()

    @keyword('Send Email')
    def send_email(self, message, subject, email_address, recipient, smtp_server, port, password):
        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = recipient
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(email_address, password)
        server.send_message(msg)
        server.close()
