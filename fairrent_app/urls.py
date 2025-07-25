from django.urls import path
from . import views

app_name = 'fairrent_app'

urlpatterns = [
    # Page Views
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'), # Custom login view
    path('logout/', views.logout_view, name='logout'), # Custom logout view
    path('profile/', views.profile_view, name='profile'),

    # API Endpoints
    path('api/check_auth/', views.check_auth, name='api_check_auth'), # Changed name for consistency

    # Complaint APIs
    path('api/complaints/', views.get_complaints, name='api_get_complaints'),
    path('api/submit_complaint/', views.submit_complaint, name='api_submit_complaint'),

    # Review APIs
    path('api/reviews/', views.get_reviews, name='api_get_reviews'),
    path('api/submit_review/', views.submit_review, name='api_submit_review'),

    # Forum APIs
    path('api/forum_posts/', views.get_forum_posts, name='api_get_forum_posts'),
    path('api/submit_forum_post/', views.submit_forum_post, name='api_submit_forum_post'),

    # AI-Powered APIs
    path('api/refine_text/', views.refine_text_api, name='api_refine_text'),
    path('api/generate_forum_idea/', views.generate_forum_idea_api, name='api_generate_forum_idea'),
    path('api/analyze_contract/', views.analyze_contract_api, name='api_analyze_contract'), # NEW API

    # Rent & Roommate APIs
    path('api/predict_rent/', views.predict_rent, name='api_predict_rent'),
    path('api/save_roommate_profile/', views.save_roommate_profile, name='api_save_roommate_profile'),
    path('api/find_roommate_matches/', views.find_roommate_matches_api, name='api_find_roommate_matches'),
    path('api/save_liked_profile/', views.save_liked_profile, name='api_save_liked_profile'),

    # NEW: Chat APIs (corrected names to match views.py)
    path('api/send_chat_message/', views.send_chat_message, name='api_send_chat_message'),
    path('api/get_chat_messages/<str:partner_uid>/', views.get_chat_messages, name='api_get_chat_messages'),

    # NEW: Notification APIs (corrected names to match views.py)
    path('api/notifications/', views.get_notifications, name='api_get_notifications'),
    path('api/mark_notification_read/', views.mark_notification_read, name='api_mark_notification_read'),

    # NEW: Connection Request APIs
    path('api/send_connection_request/', views.send_connection_request, name='api_send_connection_request'),
    path('api/respond_to_connection_request/', views.respond_to_connection_request, name='api_respond_to_connection_request'),

    # Utility APIs (corrected name to match views.py)
    path('api/address_suggestions/', views.get_address_suggestions, name='api_get_address_suggestions'), # Changed name for consistency
    path('api/check_rent_declaration/', views.check_rent_declaration_api, name='api_check_rent_declaration'), # Changed name for consistency
]
