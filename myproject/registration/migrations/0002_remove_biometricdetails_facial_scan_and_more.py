# Generated by Django 5.0.7 on 2024-07-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biometricdetails',
            name='facial_scan',
        ),
        migrations.AddField(
            model_name='biometricdetails',
            name='fingerprint',
            field=models.BinaryField(default=1),
            preserve_default=False,
        ),
    ]
