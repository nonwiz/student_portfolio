# Generated by Django 4.0.3 on 2022-03-30 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0012_alter_student_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='website',
            field=models.CharField(max_length=50, null=True),
        ),
    ]