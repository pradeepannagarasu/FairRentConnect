from django.contrib import admin
from .models import Complaint, LandlordReview, RoommateProfile, ForumPost, ForumReply, RentCheck, LikedProfile, RentalContract, RentDeclarationCheck # Import new model

# Customizing the admin interface for better usability
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'issue_type', 'property_address', 'status', 'submitted_at')
    list_filter = ('status', 'issue_type')
    search_fields = ('user__username', 'property_address', 'description')

class LandlordReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'landlord_name', 'rating', 'property_address', 'reviewed_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'landlord_name', 'comments')

class RoommateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'budget', 'location', 'updated_at')
    search_fields = ('user__username', 'location', 'bio')

class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'content', 'user__username')

class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('content', 'user__username')

class RentCheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'postcode', 'bedrooms', 'estimated_rent', 'checked_at')
    list_filter = ('bedrooms',)
    search_fields = ('user__username', 'postcode')

class LikedProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'liked_user_name', 'liked_user_location', 'liked_user_compatibility_score', 'liked_at')
    search_fields = ('user__username', 'liked_user_name', 'liked_user_location')

class RentalContractAdmin(admin.ModelAdmin):
    list_display = ('user', 'analyzed_at')
    search_fields = ('user__username', 'original_text')
    list_filter = ('analyzed_at',)

# NEW: Admin configuration for RentDeclarationCheck
class RentDeclarationCheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'postcode', 'actual_rent_paid', 'council_tax_band', 'discrepancy_found', 'checked_at')
    list_filter = ('discrepancy_found', 'council_tax_band')
    search_fields = ('user__username', 'postcode', 'analysis_result')
    readonly_fields = ('checked_at',) # Make this field read-only in the admin


# Register your models with the custom admin classes
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(LandlordReview, LandlordReviewAdmin)
admin.site.register(RoommateProfile, RoommateProfileAdmin)
admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(ForumReply, ForumReplyAdmin)
admin.site.register(RentCheck, RentCheckAdmin)
admin.site.register(LikedProfile, LikedProfileAdmin)
admin.site.register(RentalContract, RentalContractAdmin)
admin.site.register(RentDeclarationCheck, RentDeclarationCheckAdmin) # Register the new model
