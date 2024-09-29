# feedJson.py

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz  # PyMuPDF for PDF handling
import re
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_schedule_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    
    pdf_document.close()
    
    pattern = re.compile(r"(?P<course>[A-Z]{4}\s\d{3})\s(?P<title>.+?)\s(?P<days>[A-Z]{2,3})\s(?P<times>\d{1,2}:\d{2}\s?[APMapm]{2} - \d{1,2}:\d{2}\s?[APMapm]{2})")
    matches = pattern.findall(text)
    
    schedule = []
    for match in matches:
        schedule.append({
            'course': match[0],
            'title': match[1],
            'days': match[2],
            'times': match[3]
        })
    
    return schedule

@app.route('/schedule', methods=['POST'])
def handle_schedule():
    print("Received request with form data:", request.form)
    print("Received file:", request.files.get('schedule'))
    
    schedule_pdf = request.files['schedule']
    sleep_schedule = request.form['sleepSchedule']
    work_schedule = request.form.get('workSchedule', '')  # Optional
    exercise = request.form.get('exercise', '')           # Optional
    study_time = request.form.get('studyTime', '')        # Optional
    miscellaneous = request.form.get('miscellaneous', '') # Optional

    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    pdf_path = os.path.join("uploads", schedule_pdf.filename)
    schedule_pdf.save(pdf_path)
    extracted_schedule = extract_schedule_pdf(pdf_path)

    formatted_schedule = ""
    for class_info in extracted_schedule:
        formatted_schedule += f"{class_info['course']} {class_info['title']} on {class_info['days']} from {class_info['times']}, "

    # Prepare prompt for Gemini AI
    prompt = f"""
    This is my daily schedule:
    - Wake up time: {sleep_schedule}
    - Sleep time: {sleep_schedule}
    - Work hours: {work_schedule if work_schedule else 'None'}
    - Study time: {study_time if study_time else 'None'}
    - Exercise time: {exercise if exercise else 'None'}
    - Other times: {miscellaneous if miscellaneous else 'None'}

    My class schedule is as follows:
    {formatted_schedule}

    Provide only the schedule, no additional information is needed.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    print("Generated Schedule:", response.text)

    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, "generated_schedule.txt")
    with open(output_file_path, 'w') as f:
        f.write(response.text.strip())

    return jsonify({"generated_schedule": response.text.strip()})

if __name__ == '__main__':
    app.run(debug=True)
