import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configuration for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Fallback to default if not set
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Ensure it's an integer
