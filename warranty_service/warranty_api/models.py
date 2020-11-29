from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class Warranty(models.Model):
    comment = models.CharField('Комментарий', max_length=120)
    item_uid = models.UUIDField(default=uuid.uuid4)
    status = models.CharField('status', max_length=60)
    warranty_date = models.DateTimeField(default=timezone.now)