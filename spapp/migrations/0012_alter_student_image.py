# Generated by Django 3.2.12 on 2022-03-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0011_student_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(null=True, upload_to='theme/static/user_image'),
        ),
    ]