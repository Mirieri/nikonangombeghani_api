from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory
load_dotenv()

class AppSettings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    app_env: str
    debug: bool
    api_url: str
    api_key: str

# Initialize AppSettings
settings = AppSettings()
