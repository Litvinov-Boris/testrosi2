from django.db import models
import uuid

# Create your models here.
class Store(models.Model):
    name = models.CharField('Имя', max_length=60)
    user_uid = models.UUIDField(default=uuid.uuid4)