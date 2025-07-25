# Generated by Django 5.2.4 on 2025-07-15 21:28

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
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_type', models.CharField(choices=[('deposit', 'Unfair Deposit Deduction'), ('maintenance', 'Poor Maintenance / Repairs'), ('harassment', 'Harassment / Unlawful Entry'), ('rent', 'Unregulated Rent / Charges'), ('conditions', 'Poor Living Conditions'), ('other', 'Other')], max_length=50)),
                ('property_address', models.CharField(max_length=255)),
                ('landlord_name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending Review'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('category', models.CharField(choices=[('legal', 'Legal Advice'), ('accommodation', 'Finding Accommodation'), ('maintenance', 'Maintenance Tips'), ('local', 'Local Area Guides'), ('other', 'Other')], default='other', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='fairrent_app.forumpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LandlordReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('landlord_name', models.CharField(max_length=255)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comments', models.TextField()),
                ('reviewed_at', models.DateTimeField(auto_now_add=True)),
                ('property_address', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoommateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('', 'Prefer not to say'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=20)),
                ('sleep_schedule', models.CharField(blank=True, choices=[('', 'Select your schedule'), ('early_bird', 'Early bird (bed by 10pm)'), ('average', 'Average (bed by 11pm-12am)'), ('night_owl', 'Night owl (bed after 12am)'), ('irregular', 'Irregular schedule')], max_length=20)),
                ('cleanliness', models.CharField(blank=True, choices=[('', 'Select your preference'), ('very_clean', 'Very clean (clean daily)'), ('clean', 'Clean (tidy most days)'), ('average', 'Average (clean weekly)'), ('relaxed', 'Relaxed about cleaning')], max_length=20)),
                ('lifestyle_preferences', models.JSONField(blank=True, default=list)),
                ('budget', models.PositiveIntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='roommate_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
