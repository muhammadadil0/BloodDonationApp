# Generated by Django 5.1.3 on 2024-11-26 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0011_alter_blooddonate_id_alter_bloodrequest_id_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="patient",
            options={},
        ),
        migrations.AddField(
            model_name="patient",
            name="reason",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="patient",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="unit",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
