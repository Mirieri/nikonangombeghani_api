# app/utils/whatsapp/whatsapp.py

from twilio.rest import Client
from app.config.appsettings import AppSettings

# Initialize AppSettings
app_settings = AppSettings()

class WhatsAppAPI:
    def __init__(self):
        # Load API credentials from app settings
        self.client = Client(app_settings.twilio_account_sid, app_settings.twilio_auth_token)
        self.whatsapp_number = app_settings.whatsapp_number # Your Twilio WhatsApp number

    def send_message(self, to: str, message: str):
        # Use Twilio API to send WhatsApp messages
        response = self.client.messages.create(
            from_=self.whatsapp_number,
            body=message,
            to=f'whatsapp:{to}'
        )
        return {
            "sid": response.sid,  # Message SID (useful for tracking)
            "status": response.status  # Message status (e.g., 'queued', 'sent')
        }

# Usage
whatsapp_api = WhatsAppAPI()
