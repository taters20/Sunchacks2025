import os
from dotenv import load_dotenv # Import for API
import google.generativeai as genai # Import for the Gemini AI
import fitz # Pdf to Json
import json 
import re

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_schedule_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # use regex to scrape the information
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

# Replace these with the variables from the front-end website
wakeTime = "6:00am"
sleepTime = "9:00pm"
workHours = "1:00pm ~ 5:00pm"
studytime = "5:00pm ~ 7:00pm"
exerciseTime = "8:00pm ~ 9:00pm"
otherTimes = ""

# Extract schedule from pdf 
pdf_path = "Schedule.pdf"
extracted_schedule = extract_schedule_pdf(pdf_path)

# Fromat the class schedule idk how tf this loop works tbh ai did this part
formatted_schedule = ""
for class_info in extracted_schedule:
    formatted_schedule += f"{class_info['course']} {class_info['title']} on {class_info['days']} from {class_info['times']}, "

model = genai.GenerativeModel("gemini-1.5-flash") # Specify model
# Prompt 
# Updated prompt including class schedule
prompt = f"""
This is my daily schedule:
- Wake up time: {wakeTime}
- Sleep time: {sleepTime}
- Work hours: {workHours}
- Study time: {studytime}
- Exercise time: {exerciseTime}
- Other times: {otherTimes}

My class schedule is as follows:
{formatted_schedule}

provide only the schedule no additional information is needed.
"""

response = model.generate_content(prompt)
print(response.text)
