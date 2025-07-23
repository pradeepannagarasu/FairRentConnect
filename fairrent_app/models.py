# =============================================================================
# FILE: fairrent_app/models.py
# =============================================================================

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid # Import uuid for generating unique IDs for AI profiles

class RoommateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # NEW: Add a name field for display purposes
    name = models.CharField(max_length=100, blank=True, null=True, help_text="Your preferred display name.")
    age = models.IntegerField(blank=True, null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    SLEEP_SCHEDULE_CHOICES = [
        ('early_bird', 'Early Bird'),
        ('night_owl', 'Night Owl'),
        ('flexible', 'Flexible'),
    ]
    sleep_schedule = models.CharField(max_length=20, choices=SLEEP_SCHEDULE_CHOICES, blank=True, null=True)
    CLEANLINESS_CHOICES = [
        ('very_tidy', 'Very Tidy'),
        ('average', 'Average'),
        ('relaxed', 'Relaxed'),
    ]
    cleanliness = models.CharField(max_length=20, choices=CLEANLINESS_CHOICES, blank=True, null=True)
    lifestyle_preferences = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated list of preferences (e.g., 'Quiet, Pet-Friendly')")
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # ADDED: created_at and updated_at fields for RoommateProfile
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name or self.user.username}'s Roommate Profile"

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, 'N/A')

    def get_sleep_schedule_display(self):
        return dict(self.SLEEP_SCHEDULE_CHOICES).get(self.sleep_schedule, 'N/A')

    def get_cleanliness_display(self):
        return dict(self.CLEANLINESS_CHOICES).get(self.cleanliness, 'N/A')

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ISSUE_TYPE_CHOICES = [
        ('repairs', 'Repairs'),
        ('noise', 'Noise Disturbance'),
        ('deposit', 'Deposit Dispute'),
        ('harassment', 'Harassment'),
        ('privacy', 'Privacy Invasion'),
        ('other', 'Other'),
    ]
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES)
    property_address = models.CharField(max_length=255)
    landlord_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.username} - {self.get_issue_type_display()}"

    def get_issue_type_display(self):
        return dict(self.ISSUE_TYPE_CHOICES).get(self.issue_type, 'N/A')

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'N/A')

class LandlordReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    landlord_name = models.CharField(max_length=255)
    property_address = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.landlord_name} by {self.user.username} - {self.rating} stars"

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    CATEGORY_CHOICES = [
        ('legal', 'Legal Advice'),
        ('accommodation', 'Finding Accommodation'),
        ('maintenance', 'Maintenance Tips'),
        ('local', 'Local Area Guides'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

class ForumReply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} to '{self.post.title}'"

class RentCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Nullable if public users can check
    postcode = models.CharField(max_length=10)
    bedrooms = models.CharField(max_length=10) # e.g., 'studio', '1', '2', '3', '4+'
    estimated_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rent Check for {self.postcode} ({self.bedrooms} bed) by {self.user.username if self.user else 'Anonymous'}"

class LikedProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_profiles')
    # NEW: Store the Firebase UID of the liked user for chat functionality
    # Changed to CharField as it will store Django PK for real users or UUID string for AI profiles
    liked_user_uid = models.CharField(max_length=255, blank=True, null=True, unique=True, help_text="Unique ID (Django PK or UUID) of the liked user.")
    liked_user_name = models.CharField(max_length=255)
    liked_user_age = models.IntegerField(null=True, blank=True)
    liked_user_gender = models.CharField(max_length=100, blank=True)
    liked_user_location = models.CharField(max_length=255, blank=True)
    liked_user_budget = models.IntegerField(null=True, blank=True)
    liked_user_bio = models.TextField(blank=True)
    liked_user_compatibility_score = models.IntegerField(null=True, blank=True)
    liked_user_avatar_url = models.URLField(max_length=500, blank=True)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'liked_user_uid') # Prevent liking the same profile multiple times

    def __str__(self):
        return f"Liked: {self.liked_user_name} by {self.user.username}"

class RentalContract(models.Model):
    """
    Model to store rental contract analysis results.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_contracts')
    original_text = models.TextField()
    analysis_result = models.TextField(blank=True, null=True) # Stores the AI's analysis
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract analysis by {self.user.username} on {self.analyzed_at.strftime('%Y-%m-%d')}"

class RentDeclarationCheck(models.Model):
    """
    Model to store results of rent vs. council tax declaration checks.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_declaration_checks')
    postcode = models.CharField(max_length=10)
    bedrooms = models.CharField(max_length=10) # e.g., 'studio', '1', '2', '3', '4+'
    actual_rent_paid = models.DecimalField(max_digits=10, decimal_places=2)
    council_tax_band = models.CharField(max_length=50, blank=True, null=True) # e.g., 'A', 'B', 'C'
    estimated_council_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discrepancy_found = models.BooleanField(default=False)
    analysis_result = models.TextField(blank=True, null=True) # AI's analysis of discrepancy
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rent Declaration Check for {self.postcode} by {self.user.username}"

# NEW: ChatMessage Model for direct messaging
class ChatMessage(models.Model):
    # Use CharField for sender_uid and receiver_uid to accommodate both Django PKs (strings) and AI UUIDs
    sender_uid = models.CharField(max_length=255, db_index=True)
    receiver_uid = models.CharField(max_length=255, db_index=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # Order messages by time

    def __str__(self):
        return f"From {self.sender_uid} to {self.receiver_uid}: {self.message[:50]}..."

