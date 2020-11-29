# Generated by Django 3.1.3 on 2020-11-25 21:12

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_uid', models.UUIDField(default=uuid.uuid4)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_uid', models.UUIDField(default=uuid.uuid4)),
                ('status', models.CharField(max_length=60)),
                ('user_uid', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
    ]