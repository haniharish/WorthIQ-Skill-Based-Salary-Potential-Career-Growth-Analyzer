# Generated for WorthIQ Phase 2 Part 2

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_role', models.CharField(help_text='Standardized or input job role', max_length=150)),
                ('skills', models.JSONField(default=list, help_text='List of technical skills evaluated')),
                ('years_of_experience', models.DecimalField(decimal_places=1, help_text='Years of professional experience', max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)])),
                ('location', models.CharField(help_text='Geographic location or tech hub', max_length=150)),
                ('education', models.CharField(blank=True, default='', help_text='Highest level of education', max_length=150)),
                ('predicted_low_salary', models.DecimalField(decimal_places=2, help_text='P10 (10th percentile) estimated annual salary in INR', max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('predicted_median_salary', models.DecimalField(decimal_places=2, help_text='P50 (Median) estimated annual salary in INR', max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('predicted_high_salary', models.DecimalField(decimal_places=2, help_text='P90 (90th percentile) estimated annual salary in INR', max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('confidence', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', help_text='Confidence tier based on data representation and interval ratio', max_length=20)),
                ('model_version', models.CharField(default='2.0.0', help_text='Version of ML model bundle generating the prediction', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Salary Prediction',
                'verbose_name_plural': 'Salary Predictions',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['user', '-created_at'], name='predictions_user_created_idx'),
                    models.Index(fields=['job_role'], name='predictions_role_idx'),
                    models.Index(fields=['location'], name='predictions_location_idx'),
                ],
            },
        ),
    ]
