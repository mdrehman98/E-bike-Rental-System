# Generated by Django 4.1.1 on 2022-10-22 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0007_wallet"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="active",
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
