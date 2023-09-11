import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
def mail(json_data):
    # Replace these variables with your Gmail credentials and the recipient's email address
    gmail_user = 'shubhamsatyam54@gmail.com'
    gmail_password = 'laffbhokuwuouufv'
    recipient_email = 'boyn139@gmail.com'

    # Create the email message
    subject = f'Data From API - Request ID : {json_data["request_id"]} - Page - {json_data["current_page"]}'
    body = 'Please find the attachment '

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))
    json_string = json.dumps(json_data)
    json_attachment = MIMEApplication(json_string.encode('utf-8'), 'json')
    json_attachment.add_header('Content-Disposition', 'attachment', filename='data.json')
    msg.attach(json_attachment)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)

        # Send the email
        server.sendmail(gmail_user, recipient_email, msg.as_string())
        print('Email sent successfully!')

    except Exception as e:
        print(f'Error: {str(e)}')

    finally:
        # Quit the server
        server.quit()
