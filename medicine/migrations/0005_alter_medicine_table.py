# Generated by Django 4.1.3 on 2022-12-01 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("medicine", "0004_alter_medicine_medicineimg"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="medicine",
            table="medicines",
        ),
    ]
