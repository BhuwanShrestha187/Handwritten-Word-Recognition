import os
from google.cloud import vision
import io

# Set Google API Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "lucid-diode-452919-p1-e5138e5e4227.json"  # Replace with your JSON path

def extract_text(image_path):
    """Extracts handwritten text using Google Vision API."""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API Error: {response.error.message}")

    return response.full_text_annotation.text