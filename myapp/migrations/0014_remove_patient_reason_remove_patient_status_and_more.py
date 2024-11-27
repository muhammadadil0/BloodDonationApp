# Generated by Django 5.1.3 on 2024-11-26 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0013_merge_20241126_1818"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patient",
            name="reason",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="status",
        ),
        migrations.RemoveField(
            model_name="patient",
            name="unit",
        ),
        migrations.AlterField(
            model_name="blooddonate",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="bloodrequest",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="contactus",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="donor",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="age",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="patient",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="patientrequest",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
