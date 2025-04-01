'''
    Filename: vision_api.py
    Author: Bhuwan Shrestha, Alen Varghese, Shubh Soni, and Dev Patel
    Date: 2025-04-01
    Project: Handwritten OCR | Capstone Project 2025
    Course: Systems Project
    Description: This is the vision API for the Handwritten OCR project.
'''


'''
    References: We have used the Google Vision API to extract text from images. The API is free to use and has a limit of 1000 requests per user. 
    The link to the API is given below: 
    - https://cloud.google.com/vision/docs/ocr
    - https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate
'''
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