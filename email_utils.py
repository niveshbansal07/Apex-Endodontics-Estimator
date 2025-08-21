# email_utils.py
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

EMAIL_TO = "info@apexendopllc.com"
EMAIL_FROM = "your_email@gmail.com"  # Use Gmail or SMTP provider
EMAIL_PASSWORD = "your_app_password"  # Use app password (not your Gmail password)

def send_estimate_email(data, estimate_value):
    try:
        subject = "New Patient Estimate Submission"
        body = f"""Patient Name: {data.get('full_name')}
Email: {data.get('email')}
Phone: {data.get('phone')}
Treatment: {data.get('treatment')}
Tooth Type: {data.get('tooth')}
Estimated Price: ${estimate_value}
Submitted On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email sent.")
    except Exception as e:
        print(f"Email failed: {e}")
