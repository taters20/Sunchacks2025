import fitz
import json

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text()
    return text

def prep_for_json(text):
    clean_text = text.replace('\n', ' ').replace('\r', '').replace('\u00a0', ' ')
    return {"content": clean_text,}

def write_to_json(data):
    with open("/Users/ishaanbalani24/Downloads/My ASU - Schedule.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)

def pdf_to_json():
    text = extract_text_from_pdf("/Users/ishaanbalani24/Downloads/My ASU - Schedule.pdf")
    data = prep_for_json(text)
    write_to_json(data)

pdf_to_json()