# Generated by Django 4.1.3 on 2022-11-12 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("yard", "0004_part_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssemblyGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="part",
            name="assembly_group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="yard.assemblygroup",
            ),
        ),
    ]