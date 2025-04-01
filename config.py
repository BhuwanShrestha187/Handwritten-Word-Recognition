'''
    Filename: config.py
    Author: Bhuwan Shrestha, Alen Varghese, Shubh Soni, and Dev Patel
    Date: 2025-04-01
    Project: Handwritten OCR | Capstone Project 2025
    Course: Systems Project
    Description: This is the configuration file for the Handwritten OCR project.
'''
import os

UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)