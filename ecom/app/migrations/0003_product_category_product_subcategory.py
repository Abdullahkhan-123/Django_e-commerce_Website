# Generated by Django 4.2.3 on 2023-08-14 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.categories'),
        ),
        migrations.AddField(
            model_name='product',
            name='SubCategory',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.subcategory'),
        ),
    ]
