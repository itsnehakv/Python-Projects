from twilio.rest import Client
import os
from dotenv import load_dotenv
import smtplib
load_dotenv()

class NotificationManager:
    def __init__(self):
        self._twilio_sid=os.environ["TWILIO_ACCOUNT_SID"]
        self._twilio_auth_token=os.environ["TWILIO_AUTH_TOKEN"]
        self._twilio_number=os.environ["TWILIO_NUMBER"]
        self._user_number=os.environ["USER_NUMBER"]
        self._sender_email=os.environ["SENDER_EMAIL"]
        self._sender_password=os.environ["SENDER_PASSWORD"]
        self.connection = smtplib.SMTP(os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"])


    def send_message(self, message):
        client = Client(self._twilio_sid, self._twilio_auth_token)

        message = client.messages.create(
            from_=f"whatsapp:{self._twilio_number}",
            to=f"whatsapp:{self._user_number}",
            body=message
        )
        print(message.status)

    def send_email(self, email_list, message_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(user=self._sender_email, password=self._sender_password)
            for email in email_list:
                self.connection.sendmail(from_addr=self._sender_email, to_addrs=email,
                                         msg=f"Subjec: Low Flights Alert \n\n")


