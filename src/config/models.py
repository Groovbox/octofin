from django.db import models
from typing import Any

class SettingType(models.TextChoices):
    STRING = 'string', 'String'
    INTEGER = 'integer', 'Integer'
    BOOL = 'bool', 'Boolean'
    PATH = 'path', 'Path'
    URL = 'url', 'URL'

    choices: Any # type: ignore

class Settings(models.Model):
    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255, default=name)
    value = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    group = models.TextField(default="General")
    type = models.CharField(
        max_length=20,
        choices=SettingType.choices,
        default=SettingType.STRING,
    )