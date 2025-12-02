from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.db import connection

from .models import RoadmapItem


def index(request):
    current_time = datetime.now()

    # Берём активные пункты дорожной карты, в порядке section/position
    items = list(
        RoadmapItem.objects.filter(is_active=True).order_by("section", "position", "id")
    )

    # Плоский список для превью на главной (первые 3)
    roadmap_preview = [
        {
            "section": item.get_section_display(),
            "text": item.text,
        }
        for item in items[:3]
    ]
    roadmap_has_more = len(items) > 3

    context = {
        "current_time": current_time,
        "roadmap_preview": roadmap_preview,
        "roadmap_has_more": roadmap_has_more,
    }
    return render(request, 'home/index.html', context)

def robots_txt(request):
    # Динамически определяем домен из запроса
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    sitemap_url = f"{scheme}://{host}/sitemap.xml"
    
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}"
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


def health_check(request):
    """Простой health check (проверка БД)."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "connected"
        overall = "healthy"
        status_code = 200
    except Exception as e:
        db_status = f"disconnected: {e}"
        overall = "unhealthy"
        status_code = 503

    return JsonResponse(
        {
            "status": overall,
            "database": db_status,
            "timestamp": datetime.now().isoformat(),
        },
        status=status_code,
    )


def status(request):
    """
    /status — страница статуса сервисов.
    Показывает, что сейчас работает.
    """
    from django.contrib.staticfiles import finders

    current_time = datetime.now()
    services = []

    # Проверка базы данных
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        services.append({
            "name": "База данных",
            "status": True,
            "description": "Подключение к базе данных работает нормально"
        })
    except Exception:
        services.append({
            "name": "База данных",
            "status": False,
            "description": "Ошибка подключения"
        })

    # Проверка статических файлов
    try:
        static_found = finders.find('css/style.css') is not None
        services.append({
            "name": "Статические файлы",
            "status": static_found,
            "description": "Статические файлы доступны" if static_found else "Проблемы с загрузкой статических файлов"
        })
    except Exception:
        services.append({
            "name": "Статические файлы",
            "status": False,
            "description": "Ошибка при проверке статических файлов"
        })

    # Основной сайт
    services.append({
        "name": "Веб-сервер",
        "status": True,
        "description": "Сервер обрабатывает запросы"
    })

    # Sitemap
    services.append({
        "name": "Карта сайта (Sitemap)",
        "status": True,
        "description": "XML карта сайта доступна по адресу /sitemap.xml"
    })

    # Robots.txt
    services.append({
        "name": "Robots.txt",
        "status": True,
        "description": "Файл для поисковых роботов доступен"
    })

    # Общий статус
    overall_status = all(s["status"] for s in services)

    context = {
        "current_time": current_time,
        "is_online": overall_status,
        "services": services,
        "year": current_time.year,
    }

    return render(request, "home/status.html", context)


def map_view(request):
    """Дорожная карта / план развития сайта и студии."""
    # Группируем пункты по разделам
    sections_map = {
        "now": {"title": "Сейчас", "items": []},
        "soon": {"title": "В ближайших планах", "items": []},
        "later": {"title": "Дальше", "items": []},
    }

    for item in RoadmapItem.objects.filter(is_active=True).order_by(
        "section", "position", "id"
    ):
        sections_map[item.section]["items"].append(item.text)

    roadmap_sections = [
        sections_map["now"],
        sections_map["soon"],
        sections_map["later"],
    ]

    context = {
        "roadmap_sections": roadmap_sections,
        "year": datetime.now().year,
    }

    return render(request, "home/map.html", context)
