import smtplib
import sys
sys.path.insert(0, "..")
from config import Config  # noqa: E402


def send_email(email, video_id):
    SUBJECT = 'EC500 HW4 - Your video is ready!'
    TEXT = f"""
    Video ID: {video_id}

    Thank you for using my API!
    """

    # Gmail Sign In
    gmail_sender = Config.GMAIL_EMAIL
    gmail_passwd = Config.GMAIL_PASSWORD
    print(gmail_sender, gmail_passwd)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join([f'To: {email}',
                        f'From: {gmail_sender}',
                        f'Subject: {SUBJECT}',
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [email], BODY)
        print('email sent')
    except Exception as e:
        print('error sending mail:', e)

    server.quit()


if __name__ == '__main__':
    send_email("rjewing@bu.edu", "Test_ID")
