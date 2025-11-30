from django.shortcuts import render
from datetime import datetime
from django.urls import path
from django.http import HttpResponse

def index(request):
    current_time = datetime.now()
    context = {
        "current_time": current_time
    }
    return render(request, 'home/index.html', context)

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Sitemap: https://www.xselid.ru/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def error_page(request, exception=None, code=500, message="Произошла ошибка", description="Что-то пошло не так"):
    context = {
        "code": code,
        "message": message,
        "description": description,
        "year": datetime.now().year,
    }
    return render(request, "home/error.html", context, status=code)

def custom_404(request, exception):
    return error_page(request, exception, code=404, message="Страница не найдена", description="К сожалению, такой страницы не существует.")

def custom_500(request):
    return error_page(request, code=500, message="Серверная ошибка", description="Произошла ошибка на сервере. Попробуйте позже.")
