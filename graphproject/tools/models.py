from django.db import models


class EndPointCall(models.Model):
    path = models.CharField(max_length=255, unique=True, verbose_name="Endpoint Path")
    call_count = models.PositiveIntegerField(default=0, verbose_name="Call Count")

    def __str__(self):
        return f"{self.path}: {self.call_count} calls"
