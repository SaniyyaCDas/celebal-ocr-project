### Folder: main_function
# File: __init__.py

import logging
import os
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from azure.ai.vision import VisionClient
from azure.ai.vision.models import (ImageAnalysisOptions, ImageSource, ImageAnalysisResultReason)
import smtplib
from email.message import EmailMessage

# Load environment variables from local.settings.json or Azure Function config
COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")
COMPUTER_VISION_KEY = os.getenv("COMPUTER_VISION_KEY")
OUTPUT_CONTAINER = os.getenv("OUTPUT_CONTAINER")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")
SENDGRID_TO_EMAIL = os.getenv("SENDGRID_TO_EMAIL")

# OCR Processing function
def analyze_image(image_url: str):
    client = VisionClient(endpoint=COMPUTER_VISION_ENDPOINT, credential=COMPUTER_VISION_KEY)
    options = ImageAnalysisOptions(image=ImageSource(url=image_url), features=["read"])
    result = client.analyze_image(options)
    
    if result.reason == ImageAnalysisResultReason.ANALYZED:
        lines = result.read_result.content
        return {"extracted_text": lines}
    else:
        raise Exception("Image analysis failed")

# Upload JSON to output blob container
def upload_output_to_blob(blob_service_client, filename, data):
    blob_client = blob_service_client.get_blob_client(container=OUTPUT_CONTAINER, blob=filename)
    blob_client.upload_blob(json.dumps(data), overwrite=True)

# Send notification email
def send_email_notification(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDGRID_FROM_EMAIL
    msg["To"] = SENDGRID_TO_EMAIL

    # Use smtplib (can replace with SendGrid API later)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)

# Azure Function Trigger

def main(blob: func.InputStream):
    logging.info(f"Processing blob: {blob.name}, Size: {blob.length} bytes")

    try:
        # Build image URL for Computer Vision API
        image_url = f"https://<your_storage_account>.blob.core.windows.net/input-container/{blob.name}"

        # Analyze image
        analysis_result = analyze_image(image_url)

        # Upload JSON output
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
        output_filename = blob.name.replace(".jpg", ".json").replace(".png", ".json")
        upload_output_to_blob(blob_service_client, output_filename, analysis_result)

        # Send email
        send_email_notification("Image Processed", f"OCR completed for file: {blob.name}")

    except Exception as e:
        logging.error(f"Failed to process image: {e}")
