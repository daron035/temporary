# Generated by Django 4.2.5 on 2023-09-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_useraccount_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]