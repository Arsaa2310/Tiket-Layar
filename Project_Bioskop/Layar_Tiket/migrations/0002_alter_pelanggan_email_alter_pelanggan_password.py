# Generated by Django 5.1.4 on 2024-12-10 22:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Layar_Tiket", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pelanggan",
            name="email",
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="pelanggan",
            name="password",
            field=models.CharField(max_length=5000),
        ),
    ]
