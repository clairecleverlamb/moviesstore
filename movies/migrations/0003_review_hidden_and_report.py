import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_review'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ReviewReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reason', models.CharField(blank=True, max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reports',
                    to='movies.review',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.AddConstraint(
            model_name='reviewreport',
            constraint=models.UniqueConstraint(
                fields=('review', 'user'),
                name='unique_review_report_per_user',
            ),
        ),
    ]
