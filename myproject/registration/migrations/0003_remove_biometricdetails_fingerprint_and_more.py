# Generated by Django 5.0.7 on 2024-07-28 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_remove_biometricdetails_facial_scan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biometricdetails',
            name='fingerprint',
        ),
        migrations.AddField(
            model_name='biometricdetails',
            name='facial_scan',
            field=models.ImageField(default=1, upload_to='facial_scans/'),
            preserve_default=False,
        ),
    ]
