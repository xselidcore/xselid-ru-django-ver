from django.db import models


class Visit(models.Model):
    """Логи посещений сайта."""

    path = models.CharField("URL", max_length=255)
    method = models.CharField("Метод", max_length=10)
    user_agent = models.TextField("User-Agent", blank=True)
    ip_address = models.GenericIPAddressField("IP-адрес", null=True, blank=True)
    referer = models.TextField("Referer", blank=True)
    created_at = models.DateTimeField("Время визита", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Визит"
        verbose_name_plural = "Визиты"

    def __str__(self):
        return f"{self.ip_address} {self.path} [{self.created_at:%Y-%m-%d %H:%M:%S}]"