# Generated by Django 4.1.2 on 2022-10-31 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="description",
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name="issue",
            name="description",
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.CharField(max_length=2048, null=True),
        ),
    ]
