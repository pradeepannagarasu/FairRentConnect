# Generated by Django 5.2.4 on 2025-07-23 14:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fairrent_app', '0006_rentdeclarationcheck'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='likedprofile',
            name='liked_user_uid',
            field=models.CharField(blank=True, help_text='Firebase UID of the liked user, if applicable.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='roommateprofile',
            name='name',
            field=models.CharField(blank=True, help_text='Your preferred display name.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='issue_type',
            field=models.CharField(choices=[('repairs', 'Repairs'), ('noise', 'Noise Disturbance'), ('deposit', 'Deposit Dispute'), ('harassment', 'Harassment'), ('privacy', 'Privacy Invasion'), ('other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='roommateprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roommateprofile',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='roommateprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='roommateprofile',
            name='lifestyle_preferences',
            field=models.CharField(blank=True, help_text="Comma-separated list of preferences (e.g., 'Quiet, Pet-Friendly')", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='roommateprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='roommateprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='roommateprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='likedprofile',
            unique_together={('user', 'liked_user_uid')},
        ),
    ]
