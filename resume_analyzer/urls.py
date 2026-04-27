from django.contrib import admin
from django.urls import path
from resume_check.views import analyze_resume,home,analyze_resume_text

urlpatterns = [
    path('', home),  # 👈 fixes 404
    path('admin/', admin.site.urls),
    path('api/analyze/', analyze_resume),
    path('',analyze_resume_text)
]