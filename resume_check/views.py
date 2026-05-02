from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from resume_check.services.parser import extract_text
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import re

@csrf_exempt





# 🔹 Core logic function
def analyze_resume_text(text):

    SKILL_DB = [
        "python", "java", "c++", "c", "dart",
        "django", "flask", "angular", "angularjs",
        "react", "sql", "mongodb", "html", "css",
        "flutter", "arduino"
    ]

    EDUCATION_DB = {
        "10th": ["10th", "matric", "secondary school"],
        "12th": ["12th", "higher secondary"],
        "Graduation": ["bachelor", "b.tech", "bsc", "bca", "ba"],
        "Post Graduation": ["master", "m.tech", "msc", "mca", "mba"]
    }

    # 🔹 Skills detection
    found_skills = []
    for skill in SKILL_DB:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill.capitalize())

    # 🔹 Education detection
    found_education = []
    for level, keywords in EDUCATION_DB.items():
        if any(keyword in text for keyword in keywords):
            found_education.append(level)

    # 🔹 Score logic
    score = len(found_skills) * 10 + len(found_education) * 5
    score = min(score, 100)

    # 🔹 Feedback
    if score > 80:
        feedback = "Excellent profile with strong skills and education."
    elif score > 60:
        feedback = "Good resume, but can improve skills or experience."
    else:
        feedback = "Add more skills and improve your profile."

    return score, feedback, found_skills, found_education


# 🔹 API View
@api_view(['POST'])
def analyze_resume(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    text = extract_text(file).lower()

    print("TEXT 👉", text[:500])

    score, feedback, skills, education = analyze_resume_text(text)

    return Response({
        "filename": file.name,
        "score": score,
        "feedback": feedback,
        "skills": skills,
        "education": education
    })


# 🔹 Test route
def home(request):
    return HttpResponse("Background is running.")