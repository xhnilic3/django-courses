# Generated by Django 3.2.7 on 2021-09-17 22:06

import autoslug.fields
import courses.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chapter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250)),
                ("slug", autoslug.fields.AutoSlugField(editable=True, populate_from="title", unique=True)),
                (
                    "perex",
                    models.TextField(
                        blank=True,
                        help_text="Short description of the chapter displayed in the list of all chapters.",
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Full description of the chapter. Explain what will user learn in this lesson.",
                        null=True,
                    ),
                ),
                (
                    "length",
                    models.IntegerField(
                        default=7,
                        help_text="Number of days that chapter will be open. If all chapters length is set to 0 course is considered self-paced.",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250)),
                (
                    "perex",
                    models.TextField(
                        blank=True,
                        help_text="Short description of the course displayed in the list of all courses. If empty description will be used.",
                        null=True,
                    ),
                ),
                ("slug", autoslug.fields.AutoSlugField(editable=True, populate_from="name", unique=True)),
                ("description", models.TextField(help_text="Full description of the course.")),
                (
                    "state",
                    models.CharField(
                        choices=[("D", "Draft"), ("O", "Open"), ("C", "Closed"), ("P", "Private")],
                        default="D",
                        max_length=1,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        help_text="Creaator of the course, mainly responsible for the content",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lecture",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250)),
                ("slug", autoslug.fields.AutoSlugField(editable=True, populate_from="title", unique=True)),
                ("subtitle", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Introduce the study material, explain what data are uploaded.", null=True
                    ),
                ),
                (
                    "data",
                    models.FileField(
                        blank=True,
                        help_text="Upload study material (document, video, image).",
                        null=True,
                        upload_to="lectures",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["jpg", "jpeg", "gif", "png", "tiff", "svg", "pdf", "mkv", "avi", "mp4", "mov"]
                            ),
                            courses.validators.FileSizeValidator(50),
                        ],
                    ),
                ),
                (
                    "data_metadata",
                    models.JSONField(
                        blank=True, help_text="Metadata about uploaded data to use in template generator.", null=True
                    ),
                ),
                ("video", embed_video.fields.EmbedVideoField(blank=True, null=True)),
                (
                    "lecture_type",
                    models.CharField(
                        choices=[
                            ("V", "Video Lesson"),
                            ("T", "Text to read"),
                            ("PF", "Peer Feedback"),
                            ("P", "Project"),
                            ("F", "Feedback"),
                            ("L", "Live lesson"),
                        ],
                        default="V",
                        max_length=2,
                    ),
                ),
                (
                    "require_submission",
                    models.CharField(
                        choices=[
                            ("N", "Not required"),
                            ("C", "Required for next chapter"),
                            ("E", "Required to end course"),
                        ],
                        default="N",
                        help_text="A submission can be required either for continuing to the next chapter or to finish the course.",
                        max_length=1,
                    ),
                ),
                (
                    "require_submission_review",
                    models.CharField(
                        choices=[
                            ("N", "Not required"),
                            ("C", "Required for next chapter"),
                            ("E", "Required to end course"),
                        ],
                        default="N",
                        help_text="Submission is accepted only after being accepted by a review.",
                        max_length=1,
                    ),
                ),
                ("order", models.IntegerField(default=0, help_text="Order number for the lecture in the chapter.")),
                ("chapter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.chapter")),
            ],
        ),
        migrations.CreateModel(
            name="Run",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250)),
                ("slug", autoslug.fields.AutoSlugField(editable=True, populate_from="title", unique=True)),
                (
                    "perex",
                    models.TextField(
                        blank=True,
                        help_text="Short description displayed in course list, use as course perex. If empty course perex will be used.",
                        null=True,
                    ),
                ),
                ("start", models.DateField()),
                (
                    "end",
                    models.DateField(
                        blank=True,
                        help_text="Date will be calculated automatically if any of the chapter has length set.",
                        null=True,
                    ),
                ),
                (
                    "price",
                    models.FloatField(
                        default=0, help_text="Price for the course run that will have to be payed by the subscriber."
                    ),
                ),
                (
                    "limit",
                    models.IntegerField(
                        default=0,
                        help_text="Max number of attendees, after which registration for the Run will close. If set to 0 the course will have no limit.",
                    ),
                ),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.course")),
                (
                    "manager",
                    models.ForeignKey(
                        help_text="Manager of the course run, responsible for the smoothness of the run.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="manager",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250)),
                ("description", models.TextField(blank=True, help_text="Describe what you have learned.", null=True)),
                (
                    "data",
                    models.FileField(
                        blank=True,
                        help_text="Upload proof of your work (document, video, image).",
                        null=True,
                        upload_to="submissions",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["jpg", "jpeg", "png", "pdf", "doc", "docx", "txt"]
                            ),
                            courses.validators.FileSizeValidator(2),
                        ],
                    ),
                ),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                (
                    "chapter",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="courses.chapter"
                    ),
                ),
                (
                    "lecture",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="courses.lecture"
                    ),
                ),
                ("run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.run")),
            ],
        ),
        migrations.CreateModel(
            name="RunUsers",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("payment", models.FloatField(default=0)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.run")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name="run",
            name="users",
            field=models.ManyToManyField(blank=True, through="courses.RunUsers", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="Meeting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("link", models.URLField(max_length=250)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "leader",
                    models.ForeignKey(
                        blank=True,
                        help_text="Leader of the meeting, eg. lecturer, vip...",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leader",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("lecture", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.lecture")),
                (
                    "organizer",
                    models.ForeignKey(
                        help_text="Organizer of the meeting, responsible for the meeting.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organizer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.run")),
            ],
        ),
        migrations.AddField(
            model_name="chapter",
            name="course",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.course"),
        ),
        migrations.AddField(
            model_name="chapter",
            name="previous",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="courses.chapter"
            ),
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250)),
                (
                    "description",
                    models.TextField(blank=True, help_text="Describe your opinion about the submission.", null=True),
                ),
                (
                    "accepted",
                    models.BooleanField(
                        help_text="Check if the submission if acceptable. If not, the reviewee will have to submit a new submission."
                    ),
                ),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("submission", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.submission")),
            ],
            options={
                "unique_together": {("submission", "author")},
            },
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "data",
                    models.FileField(
                        upload_to="certificates",
                        validators=[
                            django.core.validators.FileExtensionValidator(["pdf"]),
                            courses.validators.FileSizeValidator(2),
                        ],
                    ),
                ),
                ("run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="courses.run")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "unique_together": {("run", "user")},
            },
        ),
    ]
