# Generated by Django 4.1.2 on 2022-11-13 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_contributor_permission"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="description",
            field=models.CharField(default="default", max_length=2048),
            preserve_default=False,
        ),
    ]
