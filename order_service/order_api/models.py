from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Orders(models.Model):
    item_uid = models.UUIDField(default=uuid.uuid4)
    order_date = models.DateTimeField(default=timezone.now)
    order_uid = models.UUIDField(default=uuid.uuid4)
    status = models.CharField(max_length=60)
    user_uid = models.UUIDField(default=uuid.uuid4)
