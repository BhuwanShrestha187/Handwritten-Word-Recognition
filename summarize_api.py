'''
    Filename: summarize_api.py
    Author: Bhuwan Shrestha, Alen Varghese, Shubh Soni, and Dev Patel
    Date: 2025-04-01
    Project: Handwritten OCR | Capstone Project 2025
    Course: Systems Project
    Description: This is the summarize API for the Handwritten OCR project.
'''
'''
    References: We have used the Pegasus model to summarize the text. The model is free to use and has a limit of 1000 requests per user. 
    The link to the model is given below: 
    - https://huggingface.co/google/pegasus-xsum
    - https://huggingface.co/google/pegasus-large
    - https://huggingface.co/google/pegasus-small
    - https://huggingface.co/google/pegasus-large-cnn
    - https://huggingface.co/google/pegasus-small-cnn
'''

from transformers import PegasusForConditionalGeneration, PegasusTokenizer

model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

def summarize_text(text):
    inputs = tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")
    summary_ids = model.generate(inputs["input_ids"], max_length=150, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)