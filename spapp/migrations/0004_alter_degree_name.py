# Generated by Django 4.0.3 on 2022-03-16 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0003_alter_degree_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degree',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
