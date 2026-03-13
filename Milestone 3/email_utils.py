import os
import threading
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_async_email(message):
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
        print("Background email sent successfully!")
    except Exception as e:
        print(f"Background email failed: {e}")

def send_otp_email(to_email, otp, subject="FitPlan AI - Login Verification"):
    """Helper function to format and send the OTP email."""
    message = Mail(
        from_email=os.environ.get('EMAIL_FROM'),
        to_emails=to_email,
        subject=subject,
        html_content=f'''
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>FitPlan AI Security</h2>
            <p>Your login verification code is:</p>
            <h1 style="color: #0ea5e9; font-size: 36px; letter-spacing: 2px;">{otp}</h1>
            <p>If you did not request this, please ignore this email.</p>
        </div>
        '''
    )
    # Send in a background thread
    threading.Thread(target=send_async_email, args=(message,)).start()
