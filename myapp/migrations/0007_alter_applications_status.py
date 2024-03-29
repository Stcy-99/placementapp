# Generated by Django 4.2.7 on 2024-01-01 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_studentprofile_saved_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('rejected', 'rejected'), ('processing', 'processing'), ('shortlisted', 'shortlisted')], default='pending', max_length=200),
        ),
    ]
