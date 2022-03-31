# Generated by Django 4.0.3 on 2022-03-31 00:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spapp', '0017_alter_student_id_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='posted',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='type',
            field=models.CharField(default='Full Time', max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='website',
            field=models.CharField(max_length=90, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='bio_char',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(default='theme/static/user_image/default-image.png', null=True, upload_to='theme/static/user_image'),
        ),
    ]
