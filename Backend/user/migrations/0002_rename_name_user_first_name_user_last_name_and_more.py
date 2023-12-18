# Generated by Django 4.1.1 on 2022-09-30 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user", old_name="name", new_name="first_name",
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("customer", "customer"),
                    ("operator", "operator"),
                    ("manager", "manager"),
                ],
                default="customer",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]