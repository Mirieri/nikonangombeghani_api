import os
import uuid
from fastapi import UploadFile
from app.config.appsettings import settings


def save_image_to_storage(file: UploadFile, filename: str) -> str:
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(settings.file_storage_path, unique_filename)

    # Ensure the storage directory exists
    os.makedirs(settings.file_storage_path, exist_ok=True)

    # Save the file to storage
    with open(file_path, "wb") as buffer:
        buffer.write(file.read())

    # Return the URL or path to the image
    return f"/images/{unique_filename}"
