# Generated by Django 3.2.12 on 2022-03-23 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0008_remove_research_co_author_research_co_authors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='website',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
