# Generated by Django 4.1.2 on 2022-11-13 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_comment_description_alter_issue_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.CharField(default="default", max_length=2048),
            preserve_default=False,
        ),
    ]