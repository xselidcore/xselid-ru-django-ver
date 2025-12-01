from django.conf import settings

from .models import Visit


class VisitorTrackingMiddleware:
    """
    Middleware для логирования визитов.

    Пишет в БД:
    - путь
    - метод
    - IP
    - user-agent
    - referer
    - время (auto_now_add в модели)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            path = request.path

            # Не логируем админку и статику
            if path.startswith("/admin/"):
                return response
            static_url = getattr(settings, "STATIC_URL", "/static/")
            if path.startswith(static_url):
                return response

            # IP (учитываем X-Forwarded-For, если есть)
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip = x_forwarded_for.split(",")[0].strip()
            else:
                ip = request.META.get("REMOTE_ADDR")

            Visit.objects.create(
                path=path,
                method=request.method,
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                ip_address=ip or None,
                referer=request.META.get("HTTP_REFERER", ""),
            )
        except Exception:
            # Никак не мешаем основному потоку, если что-то пошло не так
            pass

        return response


