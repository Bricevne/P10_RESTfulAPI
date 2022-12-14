# Generated by Django 4.1.2 on 2022-11-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_project_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributor",
            name="permission",
            field=models.CharField(
                choices=[("A", "Admin"), ("R", "Restricted access"), ("M", "Member")],
                max_length=50,
            ),
        ),
    ]
