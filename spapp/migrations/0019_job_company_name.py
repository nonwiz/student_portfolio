# Generated by Django 4.0.3 on 2022-03-31 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0018_job_posted_job_type_alter_job_website_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='company_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
