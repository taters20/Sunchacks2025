# feedJson.py

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz  # PyMuPDF for PDF handling
import re

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

@app.route('/schedule', methods=['POST'])
def handle_schedule():
    # Extract data from the request
    schedule_pdf = request.files['schedule']
    sleep_schedule = request.form['sleepSchedule']
    work_schedule = request.form['workSchedule']
    exercise = request.form['exercise']
    study_time = request.form['studyTime']
    miscellaneous = request.form['miscellaneous']

    # Extract schedule from the uploaded PDF file
    pdf_path = os.path.join("uploads", schedule_pdf.filename)
    schedule_pdf.save(pdf_path)
    extracted_schedule = extract_schedule_pdf(pdf_path)

    # Format class schedule for the prompt
    formatted_schedule = ""
    for class_info in extracted_schedule:
        formatted_schedule += f"{class_info['course']} {class_info['title']} on {class_info['days']} from {class_info['times']}, "

    # Prompt for Gemini AI
    prompt = f"""
    This is my daily schedule:
    - Wake up time: {sleep_schedule}
    - Sleep time: {sleep_schedule}
    - Work hours: {work_schedule}
    - Study time: {study_time}
    - Exercise time: {exercise}
    - Other times: {miscellaneous}

    My class schedule is as follows:
    {formatted_schedule}

    Provide only the schedule, no additional information is needed.
    """

    # Generate AI response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Log the generated schedule for debugging
    print("Generated Schedule:", response.text)

    # Return the generated schedule as JSON
    return jsonify({"generated_schedule": response.text.strip()})

# Function to extract schedule from PDF
def extract_schedule_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    pattern = r'(\d{5})\s+([\w\s]+)\s+([\w\s]+)\s+(\d+\.\d+)\s+([\w,\s]+)\s+([\w\s]+)\s+([\d:]+\s*(?:AM|PM)?\s*-\s*[\d:]+\s*(?:AM|PM)?)\s+([\d/]+\s*-\s*[\d/]+)\s+([\w\s]+)'
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

if __name__ == '__main__':
    app.run(debug=True)
