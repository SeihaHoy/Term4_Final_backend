# Generated by Django 5.1.4 on 2024-12-25 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0002_alter_cv_image_pred'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='image',
            field=models.ImageField(upload_to='images/cv'),
        ),
        migrations.AlterField(
            model_name='cv',
            name='image_pred',
            field=models.ImageField(upload_to='images/cv'),
        ),
    ]
