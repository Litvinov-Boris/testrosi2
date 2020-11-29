from django.db import models
import uuid

# Create your models here.
class Items(models.Model):
    available_count = models.IntegerField()
    model = models.CharField(max_length=60)
    size = models.CharField(max_length=60)

class Order_item(models.Model):
    canceled = models.BooleanField(default=False)
    order_item_uid = models.UUIDField(default=uuid.uuid4)
    order_uid = models.UUIDField(default=uuid.uuid4)
    item_id = models.IntegerField()