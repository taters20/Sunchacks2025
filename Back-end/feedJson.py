# feedJson.py

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz  # PyMuPDF for PDF handling
import re
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_schedule_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    pattern = r'(\d{5})\s+([\w\n]+)+([\w\s]+)\s+(\d+.\d+)\s+([\w\s]+(?:,\sStaff)?)\n+([\w\s]+)\s+([\d:]+\s(?:AM|PM)?\s-\s[\d:]+\s(?:AM|PM)?)\s+([\d/]+\s-\s[\d/]+)\s+([\w\n\w\n]+)'
    matches = re.findall(pattern, text)

    schedule = []
    for match in matches:
        class_num, course, title, units, instructor, days, times, dates, location = match
        schedule.append({
            "class_num": class_num,
            "course": course,
            "title": title,
            "units": units,
            "instructor": instructor,
            "days": days,
            "times": times,
            "dates": dates,
            "location": location
        })
    
    return schedule
    
@app.route('/', methods=['POST'])
def handle_schedule():
    ''' these are test cases
    print("Received request with form data:", request.form)
    print("Received file:", request.files.get('schedule'))
    '''
    
    schedule_pdf = request.files['schedule']
    sleep_schedule = request.form['sleepSchedule']
    work_schedule = request.form.get('workSchedule', '')  # Optional
    exercise = request.form.get('exercise', '')           # Optional
    study_time = request.form.get('studyTime', '')        # Optional
    miscellaneous = request.form.get('miscellaneous', '') # Optional

    ''' this is another test case
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    '''


    pdf_path = os.path.join("uploads", schedule_pdf.filename)
    schedule_pdf.save(pdf_path)
    
    extracted_schedule = extract_schedule_pdf(pdf_path)
    print(extracted_schedule)

    formatted_schedule = ""

    for class_info in extracted_schedule:
        formatted_schedule += f"{class_info['course']} {class_info['title']} on {class_info['days']} from {class_info['times']}, "

    model = genai.GenerativeModel("gemini-1.5-flash")
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
    Fit the study time, exercise time, and miscellaneous whenever appropriate so it doesn't overlap
    """

 
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