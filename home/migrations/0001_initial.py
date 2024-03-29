# Generated by Django 4.1 on 2022-10-23 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Batch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("batch", models.IntegerField()),
            ],
            options={
                "verbose_name_plural": "Batches",
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "code",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("short", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Institute",
            fields=[
                (
                    "code",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("short", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="rsFiles",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("migrated", models.BooleanField(default=False)),
                (
                    "examination",
                    models.CharField(
                        choices=[("REGULAR ", "REGULAR"), ("REAPPEAR", "REAPPEAR")],
                        default="Regular",
                        max_length=8,
                    ),
                ),
                ("pdf", models.FileField(upload_to="result_pdfs/")),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.batch"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.course"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Files",
            },
        ),
        migrations.CreateModel(
            name="MCA",
            fields=[
                ("semester", models.JSONField(blank=True, default=dict)),
                (
                    "enrollment",
                    models.CharField(max_length=11, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(blank=True, max_length=100)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.batch"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.course"
                    ),
                ),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.institute"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "MCA",
            },
        ),
        migrations.AddField(
            model_name="course",
            name="institute",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="home.institute"
            ),
        ),
        migrations.CreateModel(
            name="BCA",
            fields=[
                ("semester", models.JSONField(blank=True, default=dict)),
                (
                    "enrollment",
                    models.CharField(max_length=11, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(blank=True, max_length=100)),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.batch"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.course"
                    ),
                ),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.institute"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "BCA",
            },
        ),
    ]
