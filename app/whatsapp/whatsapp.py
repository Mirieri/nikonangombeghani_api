import requests
from app.config.whatsapp_settings import AppSettings

# Initialize AppSettings
app_settings = AppSettings()

class WhatsAppAPI:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def send_message(self, to: str, message: str):
        response = requests.post(
            f"{self.api_url}/send",
            json={"to": to, "message": message},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()

# Create an instance of WhatsAppAPI using settings from AppSettings
whatsapp_api = WhatsAppAPI(api_url=app_settings.api_url, api_key=app_settings.api_key)
