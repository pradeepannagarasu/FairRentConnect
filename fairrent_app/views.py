# =============================================================================
# FILE: fairrent_app/views.py
# =============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings # Import settings to access API keys
from django.db import transaction # For atomic operations
from django.contrib.auth.models import User  # Import User model
from django.db.models import Q  # Import Q for complex queries

import json
import requests
import random
import logging
import uuid # Import uuid for generating unique IDs for AI profiles
from decimal import Decimal # Import Decimal to handle precise numbers
from datetime import datetime # Import datetime for date parsing

from .models import Complaint, LandlordReview, RoommateProfile, ForumPost, ForumReply, RentCheck, LikedProfile, RentalContract, RentDeclarationCheck, ChatMessage, Notification # Import all models, including Notification

# Get an instance of a logger
logger = logging.getLogger(__name__)

# --- Page Rendering Views ---

def index(request):
    """
    Renders the main application homepage.
    FIXED: Removed the redirect for authenticated users. Now, it always renders index.html.
    """
    return render(request, 'fairrent_app/index.html')

@login_required
def profile_view(request):
    """
    Renders the user's profile dashboard with real-time data for
    complaints, reviews, roommate profile, rent checks, forum posts, and liked profiles.
    Handles cases where a RoommateProfile might not yet exist for the user.
    """
    user_complaints = Complaint.objects.filter(user=request.user).order_by('-submitted_at')[:5]
    user_reviews = LandlordReview.objects.filter(user=request.user).order_by('-reviewed_at')[:5]
    
    # CRITICAL CHANGE: Fetch the roommate profile, and handle if it doesn't exist
    user_roommate_profile = RoommateProfile.objects.filter(user=request.user).first()
    
    # Add a message if the profile is missing, guiding the user to create it
    if not user_roommate_profile:
        messages.info(request, "Welcome! Please create your roommate profile to unlock all features and find matches.")

    user_rent_checks = RentCheck.objects.filter(user=request.user).order_by('-checked_at')[:5] # Fetch user's rent checks
    user_forum_posts = ForumPost.objects.filter(user=request.user).order_by('-created_at')[:5]
    # IMPORTANT: Select related user for liked profiles to get their UID
    user_liked_profiles = LikedProfile.objects.filter(user=request.user).order_by('-liked_at')[:5]  
    user_rental_contracts = RentalContract.objects.filter(user=request.user).order_by('-analyzed_at')[:5] # Fetch user's analyzed contracts
    user_rent_declaration_checks = RentDeclarationCheck.objects.filter(user=request.user).order_by('-checked_at')[:5] # Fetch user's rent declaration checks

    # Fetch unread notifications count
    unread_notifications_count = Notification.objects.filter(recipient=request.user, is_read=False).count()


    # Combine all user activities for the 'Recent Activity' section, sort by timestamp
    all_activities = []
    for complaint in user_complaints:
        all_activities.append({
            'type': 'Complaint',
            'description': f"Submitted complaint about {complaint.get_issue_type_display()}",
            'timestamp': complaint.submitted_at,
            'icon': 'exclamation-triangle',
            'color': 'red',
            'details': { # Include details for modal display
                'issue_type': complaint.get_issue_type_display(),
                'property_address': complaint.property_address,
                'landlord_name': complaint.landlord_name,
                'description': complaint.description,
                'status': complaint.get_status_display(),
                'submitted_at': complaint.submitted_at.isoformat() if complaint.submitted_at else None
            }
        })
    for review in user_reviews:
        all_activities.append({
            'type': 'Review',
            'description': f"Submitted review for {review.landlord_name}",
            'timestamp': review.reviewed_at,
            'icon': 'star',
            'color': 'green',
            'details': { # Include details for modal display
                'landlord_name': review.landlord_name,
                'property_address': review.property_address,
                'rating': review.rating,
                'comments': review.comments,
                'reviewed_at': review.reviewed_at.isoformat() if review.reviewed_at else None,
                'reviewer': review.user.username
            }
        })
    for rent_check in user_rent_checks:
        all_activities.append({
            'type': 'Rent Check',
            'description': f"Checked rent for {rent_check.postcode} ({rent_check.bedrooms} bed)",
            'timestamp': rent_check.checked_at,
            'icon': 'gbp-sign',
            'color': 'blue',
            'details': { # Include details for modal display
                'postcode': rent_check.postcode,
                'bedrooms': rent_check.bedrooms,
                'estimated_rent': str(rent_check.estimated_rent) if rent_check.estimated_rent else None, # Convert Decimal to string
                'checked_at': rent_check.checked_at.isoformat() if rent_check.checked_at else None
            }
        })
    for post in user_forum_posts:
        all_activities.append({
            'type': 'Forum Post',
            'description': f"Posted in Community Forums: '{post.title}'",
            'timestamp': post.created_at,
            'icon': 'comments',
            'color': 'yellow',
            'details': { # Include details for modal display
                'title': post.title,
                'content': post.content,
                'category': post.get_category_display(),
                'created_at': post.created_at.isoformat() if post.created_at else None,
                'author': post.user.username
            }
        })
    for liked_profile in user_liked_profiles:
        all_activities.append({
            'type': 'Liked Profile',
            'description': f"Liked profile: {liked_profile.liked_user_name}",
            'timestamp': liked_profile.liked_at,
            'icon': 'heart', # Using a heart icon for liked profiles
            'color': 'pink', # Using pink for liked profiles
            'details': { # Store full details to reopen modal
                'name': liked_profile.liked_user_name,
                'age': liked_profile.liked_user_age,
                'gender': liked_profile.liked_user_gender,
                'location': liked_profile.liked_user_location,
                'budget': liked_profile.liked_user_budget,
                'bio': liked_profile.liked_user_bio,
                'compatibility_score': liked_profile.liked_user_compatibility_score,
                'avatar_url': liked_profile.liked_user_avatar_url,
                'uid': liked_profile.liked_user_uid # NEW: Pass the liked user's UID for chat
            }
        })
    for contract in user_rental_contracts: # Add rental contracts to activities
        all_activities.append({
            'type': 'Contract Analysis',
            'description': f"Analyzed a rental contract",
            'timestamp': contract.analyzed_at,
            'icon': 'file-contract',
            'color': 'indigo',
            'details': {
                'original_text': contract.original_text,
                'analysis_result': contract.analysis_result,
                'analyzed_at': contract.analyzed_at.isoformat() if contract.analyzed_at else None
            }
        })
    for declaration_check in user_rent_declaration_checks: # Add rent declaration checks to activities
        all_activities.append({
            'type': 'Rent Declaration Check',
            'description': f"Checked rent declaration for {declaration_check.postcode}",
            'timestamp': declaration_check.checked_at,
            'icon': 'file-invoice-dollar', # Icon for financial documents/invoices
            'color': 'orange', # A distinct color
            'details': {
                'postcode': declaration_check.postcode,
                'bedrooms': declaration_check.bedrooms,
                'actual_rent_paid': str(declaration_check.actual_rent_paid),
                'council_tax_band': declaration_check.council_tax_band,
                'estimated_council_tax': str(declaration_check.estimated_council_tax) if declaration_check.estimated_council_tax else 'N/A',
                'discrepancy_found': declaration_check.discrepancy_found,
                'analysis_result': declaration_check.analysis_result,
                'checked_at': declaration_check.checked_at.isoformat() if declaration_check.checked_at else None
            }
        })


    # Sort all activities by timestamp in descending order
    all_activities.sort(key=lambda x: x['timestamp'], reverse=True)

    context = {
        'user_complaints': user_complaints,
        'user_reviews': user_reviews,
        'user_roommate_profile': user_roommate_profile, # Pass the fetched profile (could be None)
        'user_rent_checks': user_rent_checks,
        'user_forum_posts': user_forum_posts,
        'user_liked_profiles': user_liked_profiles,
        'user_rental_contracts': user_rental_contracts,
        'user_rent_declaration_checks': user_rent_declaration_checks,
        'recent_activities': all_activities[:5],
        'current_date': timezone.now(),
        'unread_notifications_count': unread_notifications_count, # Pass count to template
    }
    return render(request, 'fairrent_app/profile.html', context)

# --- Authentication Views (no changes needed) ---
def signup_view(request):
    """Handles user registration."""
    if request.user.is_authenticated:
        return redirect('fairrent_app:profile')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome.")
            return redirect('fairrent_app:profile')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return render(request, 'fairrent_app/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'fairrent_app/signup.html', {'form': form})

def login_view(request):
    """Handles user login."""
    if request.user.is_authenticated:
        return redirect('fairrent_app:profile')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('fairrent_app:profile')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'fairrent_app/login.html', {'form': form})

def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('fairrent_app:index')

# --- API Views ---

@require_http_methods(["GET"])
def check_auth(request):
    """API endpoint to check if a user is authenticated."""
    return JsonResponse({'status': 'success', 'data': {'authenticated': request.user.is_authenticated}})

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def save_roommate_profile(request):
    """API endpoint to save or update a user's roommate profile."""
    try:
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        user_type = data.get('user_type') # NEW: Get user_type

        if not name:
            return JsonResponse({'status': 'error', 'message': 'Name is required for your profile.'}, status=400)
        if not user_type:
            return JsonResponse({'status': 'error', 'message': 'Please select if you are looking for a room or offering one.'}, status=400)

        profile_defaults = {
            'name': name,
            'user_type': user_type,
            'location': data.get('location'),
            'bio': data.get('bio')
        }

        if user_type == 'looking_for_room':
            age = data.get('age')
            if age is not None:
                try:
                    age = int(age)
                    if not (18 <= age <= 99):
                        raise ValueError("Age must be between 18 and 99.")
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Invalid age provided. Must be a number between 18 and 99.'}, status=400)
            else:
                age = None

            budget = data.get('budget')
            if budget is not None:
                try:
                    budget = int(budget)
                    if not (100 <= budget <= 5000):
                        raise ValueError("Budget must be between £100 and £5000.")
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Invalid budget provided. Must be a number between £100 and £5000.'}, status=400)
            else:
                budget = None

            lifestyle_preferences_raw = data.get('lifestyle_preferences', '')
            if isinstance(lifestyle_preferences_raw, list):
                lifestyle_preferences = ", ".join([str(item).strip() for item in lifestyle_preferences_raw if str(item).strip()])
            else:
                lifestyle_preferences = lifestyle_preferences_raw.strip()

            profile_defaults.update({
                'age': age,
                'gender': data.get('gender'),
                'sleep_schedule': data.get('sleep_schedule'),
                'cleanliness': data.get('cleanliness'),
                'lifestyle_preferences': lifestyle_preferences,
                'budget': budget,
                # Clear fields specific to 'offering_room' if switching type
                'num_available_rooms': None,
                'rent_amount_offering': None,
                'room_size': None,
                'house_rules': None,
                'availability_date': None,
                'property_photos': None,
            })
        elif user_type == 'offering_room':
            num_available_rooms = data.get('num_available_rooms')
            if num_available_rooms is not None:
                try:
                    num_available_rooms = int(num_available_rooms)
                    if not (1 <= num_available_rooms <= 10):
                        raise ValueError("Number of available rooms must be between 1 and 10.")
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Invalid number of available rooms. Must be a number between 1 and 10.'}, status=400)
            else:
                num_available_rooms = None
            
            rent_amount_offering = data.get('rent_amount_offering')
            if rent_amount_offering is not None:
                try:
                    rent_amount_offering = Decimal(str(rent_amount_offering))
                    if not (100 <= rent_amount_offering <= 5000):
                        raise ValueError("Rent amount must be between £100 and £5000.")
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Invalid rent amount. Must be a number between £100 and £5000.'}, status=400)
            else:
                rent_amount_offering = None

            availability_date_str = data.get('availability_date')
            availability_date = None
            if availability_date_str:
                try:
                    availability_date = datetime.strptime(availability_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid availability date format. Use YYYY-MM-DD.'}, status=400)

            profile_defaults.update({
                'num_available_rooms': num_available_rooms,
                'rent_amount_offering': rent_amount_offering,
                'room_size': data.get('room_size'),
                'house_rules': data.get('house_rules', ''), # Assuming comma-separated string
                'property_photos': data.get('property_photos', ''), # Assuming comma-separated URLs
                'availability_date': availability_date,
                # Clear fields specific to 'looking_for_room' if switching type
                'age': None,
                'gender': None,
                'sleep_schedule': None,
                'cleanliness': None,
                'lifestyle_preferences': None,
                'budget': None,
            })

        profile, created = RoommateProfile.objects.update_or_create(
            user=request.user,
            defaults=profile_defaults
        )
        profile.full_clean()
        profile.save()
        return JsonResponse({'status': 'success', 'message': 'Profile saved successfully!'})
    except (json.JSONDecodeError) as e:
        logger.error(f"JSON Decode Error in save_roommate_profile: {e}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except ValidationError as e:
        error_messages = e.message_dict if hasattr(e, 'message_dict') else {'__all__': e.messages}
        logger.warning(f"Validation Error in save_roommate_profile: {error_messages}")
        return JsonResponse({'status': 'error', 'message': 'Validation failed.', 'errors': error_messages}, status=400)
    except Exception as e:
        logger.exception("An unexpected error occurred in save_roommate_profile")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def find_roommate_matches_api(request):
    """
    API endpoint to find roommate matches. Prioritizes real users,
    then falls back to AI-generated profiles if insufficient real matches.
    Matching logic now depends on the current user's 'user_type'.
    """
    user_profile = None
    try:
        user_profile = RoommateProfile.objects.get(user=request.user)
    except RoommateProfile.DoesNotExist:
        logger.warning(f"User {request.user.username} tried to find matches without a profile.")
        return JsonResponse({'status': 'error', 'message': 'Please create your profile first to find matches.'}, status=404)

    if not user_profile.user_type:
        return JsonResponse({'status': 'error', 'message': 'Please specify if you are looking for a room or offering one in your profile.'}, status=400)

    openai_api_key = settings.OPENAI_API_KEY
    if not openai_api_key:
        logger.error("OpenAI API key not configured. AI matching disabled.")
        return JsonResponse({'status': 'error', 'message': 'AI service is currently unavailable. OpenAI API key not configured.'}, status=503)

    # **MODIFIED**: Adjusted target matches to a more reasonable number for performance.
    target_matches_count = 15 
    found_matches = []

    # Determine the type of profiles to search for
    if user_profile.user_type == 'looking_for_room':
        target_user_type = 'offering_room'
        # Filter out profiles that are not offering a room or are the current user
        all_other_profiles = RoommateProfile.objects.filter(user_type='offering_room').exclude(user=request.user)
    else: # user_profile.user_type == 'offering_room'
        target_user_type = 'looking_for_room'
        # Filter out profiles that are not looking for a room or are the current user
        all_other_profiles = RoommateProfile.objects.filter(user_type='looking_for_room').exclude(user=request.user)
    
    potential_real_matches = []

    for other_profile in all_other_profiles:
        score = 0
        
        if user_profile.user_type == 'looking_for_room':
            # User is looking for a room, matching with someone offering a room
            # Match on location (exact or broad area)
            if user_profile.location and other_profile.location and \
               user_profile.location.lower() in other_profile.location.lower() or \
               other_profile.location.lower() in user_profile.location.lower():
                score += 3
            
            # Match on budget (user's max budget vs. room's offered rent)
            if user_profile.budget and other_profile.rent_amount_offering:
                if user_profile.budget >= other_profile.rent_amount_offering:
                    score += 2 # User can afford it
                elif user_profile.budget * Decimal('1.20') >= other_profile.rent_amount_offering:
                    score += 1 # User can afford with some flexibility (20% above budget)

            # Room size preference (simple match)
            if other_profile.room_size:
                score += 0.5 

            # Lifestyle/House Rules compatibility
            user_prefs = set(p.strip().lower() for p in (user_profile.lifestyle_preferences or '').split(',') if p.strip())
            other_rules = set(p.strip().lower() for p in (other_profile.house_rules or '').split(',') if p.strip())
            
            # Penalize for direct conflicts
            if 'non-smoker' in user_prefs and 'smoker' in other_rules:
                score -= 2
            if 'pet-friendly' in user_prefs and 'no pets' in other_rules:
                score -= 1
            if 'pet-friendly' not in user_prefs and 'pets allowed' in other_rules:
                score += 0.5

            # Reward for alignment
            if 'quiet' in user_prefs and 'quiet hours' in other_rules:
                score += 1
            if 'social' in user_prefs and 'no parties' not in other_rules:
                score += 0.5
            
            # Gender preference
            if user_profile.gender and other_profile.gender:
                if user_profile.gender == other_profile.gender:
                    score += 1.5
                elif user_profile.gender == 'other' or other_profile.gender == 'other':
                    score += 0.5

            # Age proximity
            if user_profile.age and other_profile.age:
                age_diff = abs(user_profile.age - other_profile.age)
                if age_diff <= 5: score += 1.5
                elif age_diff <= 10: score += 0.5


            potential_real_matches.append({
                'score': score,
                'user_type': other_profile.user_type,
                'name': other_profile.name or other_profile.user.username,
                'location': other_profile.location,
                'rent_amount_offering': str(other_profile.rent_amount_offering) if other_profile.rent_amount_offering else None,
                'num_available_rooms': other_profile.num_available_rooms,
                'room_size': other_profile.room_size,
                'house_rules': other_profile.house_rules,
                'availability_date': other_profile.availability_date.isoformat() if other_profile.availability_date else None,
                'bio': other_profile.bio,
                'compatibility_score': min(95, max(50, 70 + int(score * 3))), # Scale score to 50-95 range
                'avatar_url': f"https://placehold.co/160x160/cccccc/ffffff?text={ (other_profile.name or other_profile.user.username)[0].upper() }" if (other_profile.name or other_profile.user.username) else 'https://placehold.co/160x160/cccccc/ffffff?text=U',
                'uid': str(other_profile.user.pk)
            })

        else: # User is offering a room, matching with someone looking for a room
            # Match on location (exact or broad area)
            if user_profile.location and other_profile.location and \
               user_profile.location.lower() in other_profile.location.lower() or \
               other_profile.location.lower() in user_profile.location.lower():
                score += 3
            
            # Match on budget (room's offered rent vs. user's max budget)
            if user_profile.rent_amount_offering and other_profile.budget:
                if user_profile.rent_amount_offering <= other_profile.budget:
                    score += 2 # Other user can afford it
                elif user_profile.rent_amount_offering <= other_profile.budget * Decimal('1.20'):
                    score += 1 # Other user can afford with some flexibility

            # Lifestyle/House Rules compatibility (inverse of above)
            user_rules = set(p.strip().lower() for p in (user_profile.house_rules or '').split(',') if p.strip())
            other_prefs = set(p.strip().lower() for p in (other_profile.lifestyle_preferences or '').split(',') if p.strip())

            if 'no smoking' in user_rules and 'smoker' in other_prefs:
                score -= 2
            if 'no pets' in user_rules and 'pet-friendly' in other_prefs:
                score -= 1
            if 'quiet hours' in user_rules and 'quiet' in other_prefs:
                score += 1
            if 'no parties' in user_rules and 'party-goer' in other_prefs:
                score -= 1.5
            
            # Gender preference
            if user_profile.gender and other_profile.gender:
                if user_profile.gender == other_profile.gender:
                    score += 1.5
                elif user_profile.gender == 'other' or other_profile.gender == 'other':
                    score += 0.5

            # Age proximity
            if user_profile.age and other_profile.age:
                age_diff = abs(user_profile.age - other_profile.age)
                if age_diff <= 5: score += 1.5
                elif age_diff <= 10: score += 0.5

            potential_real_matches.append({
                'score': score,
                'user_type': other_profile.user_type,
                'name': other_profile.name or other_profile.user.username,
                'age': other_profile.age,
                'gender': other_profile.get_gender_display(),
                'location': other_profile.location,
                'budget': str(other_profile.budget) if other_profile.budget else None,
                'bio': other_profile.bio,
                'compatibility_score': min(95, max(50, 70 + int(score * 3))),
                'avatar_url': f"https://placehold.co/160x160/cccccc/ffffff?text={ (other_profile.name or other_profile.user.username)[0].upper() }" if (other_profile.name or other_profile.user.username) else 'https://placehold.co/160x160/cccccc/ffffff?text=U',
                'uid': str(other_profile.user.pk)
            })

    # Sort real matches by score and select the best ones
    potential_real_matches.sort(key=lambda x: x['score'], reverse=True)
    
    # Determine how many AI profiles to generate based on total user count
    total_real_users = User.objects.count()
    AI_THRESHOLD = 50 # The number of real users after which AI profiles start to reduce
    
    if total_real_users < AI_THRESHOLD:
        # If below threshold, generate enough AI profiles to reach target_matches_count
        num_ai_to_generate = target_matches_count - len(potential_real_matches)
    else:
        # If above threshold, reduce AI profiles (e.g., no AI profiles)
        num_ai_to_generate = 0 

    # Ensure we don't try to generate negative number of AI profiles
    num_ai_to_generate = max(0, num_ai_to_generate)

    # Add real matches first
    found_matches.extend(potential_real_matches[:target_matches_count])

    # Generate AI matches if needed
    if num_ai_to_generate > 0 and openai_api_key:
        try:
            prompt_parts = []
            if user_profile.user_type == 'looking_for_room':
                prompt_parts.append(f"Generate a JSON object with a single key 'matches' which contains a JSON array of {num_ai_to_generate} fictional roommate profiles OFFERING a room.")
                prompt_parts.append(f"These profiles should be compatible with a user who is LOOKING for a room with these preferences: Location: {user_profile.location or 'any'}, Budget: £{user_profile.budget or 'any'}, Lifestyle: {user_profile.lifestyle_preferences or 'any'}.")
                prompt_parts.append("Each generated profile must include: 'name', 'location', 'rent_amount_offering' (integer), 'num_available_rooms' (integer 1-3), 'room_size' (e.g., 'Double'), 'house_rules' (comma-separated), 'availability_date' (YYYY-MM-DD), 'bio' (2-3 sentences), 'compatibility_score' (integer 70-95), 'avatar_url' (using https://picsum.photos/seed/UNIQUE_NUMBER/160/160), and 'uid' (unique string 'ai_profile_UUID').")
            else: # user_profile.user_type == 'offering_room'
                prompt_parts.append(f"Generate a JSON object with a single key 'matches' which contains a JSON array of {num_ai_to_generate} fictional roommate profiles LOOKING for a room.")
                prompt_parts.append(f"These profiles should be compatible with a user who is OFFERING a room with these details: Location: {user_profile.location or 'any'}, Rent: £{user_profile.rent_amount_offering or 'any'}, House Rules: {user_profile.house_rules or 'any'}.")
                prompt_parts.append("Each generated profile must include: 'name', 'age' (integer 18-40), 'gender', 'location', 'budget' (integer), 'sleep_schedule', 'cleanliness', 'lifestyle_preferences' (comma-separated), 'bio' (2-3 sentences), 'compatibility_score' (integer 70-95), 'avatar_url' (using https://picsum.photos/seed/UNIQUE_NUMBER/160/160), and 'uid' (unique string 'ai_profile_UUID').")
            
            prompt_parts.append("Ensure the response is ONLY a JSON object. Do not include any text, comments, or markdown formatting outside of the single JSON object.")
            prompt = "\n".join(prompt_parts)

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.9,
                    "response_format": {"type": "json_object"}
                }
            )
            response.raise_for_status()
            ai_content = response.json()['choices'][0]['message']['content']
            
            try:
                ai_matches_data = json.loads(ai_content)
                ai_matches = ai_matches_data.get('matches', [])
                if not isinstance(ai_matches, list):
                    ai_matches = [ai_matches]
            except json.JSONDecodeError:
                ai_matches = []
                logger.error(f"Failed to decode AI response as JSON list for roommate matches: {ai_content}")

            # Only add AI profiles if we haven't reached the target count with real users
            current_found_count = len(found_matches)
            for match in ai_matches:
                if current_found_count >= target_matches_count:
                    break # Stop adding AI profiles if we have enough matches
                if isinstance(match, dict):
                    match['uid'] = f"ai_profile_{uuid.uuid4()}"
                    match['user_type'] = target_user_type 
                    found_matches.append(match)
                    current_found_count += 1
                else:
                    logger.warning(f"Skipping non-dictionary AI match: {match}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAI API request failed for AI matches: {e}")
            return JsonResponse({'status': 'warning', 'message': f'Failed to generate AI matches: {e}. Showing available real matches.' if found_matches else 'Failed to generate AI matches and no real matches found.'}, status=500)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response JSON for AI matches: {e}. Content: {ai_content}")
            return JsonResponse({'status': 'error', 'message': 'AI service returned an unreadable response for matches.'}, status=500)
        except Exception as e:
            logger.exception("An unexpected error occurred during AI match generation")
            return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred during AI matching: {e}'}, status=500)

    if not found_matches:
        return JsonResponse({'status': 'info', 'message': 'No compatible roommates found at this time. Try updating your profile preferences.'}, status=200)

    random.shuffle(found_matches)

    return JsonResponse({'status': 'success', 'message': 'Matches found successfully.', 'data': {'matches': found_matches}})

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def save_liked_profile(request):
    """
    API endpoint to save a liked roommate profile and create a notification for the liked user.
    """
    try:
        data = json.loads(request.body)
        # Explicitly get and sanitize/convert each field
        liked_user_name = data.get('name', '')
        liked_user_age = None
        if isinstance(data.get('age'), (int, float)):
            liked_user_age = int(data.get('age'))
        elif isinstance(data.get('age'), str) and data.get('age').isdigit():
            liked_user_age = int(data.get('age'))

        liked_user_gender = data.get('gender', '')
        liked_user_location = data.get('location', '')
        
        liked_user_budget = None
        if isinstance(data.get('budget'), (int, float)):
            liked_user_budget = int(data.get('budget'))
        elif isinstance(data.get('budget'), str) and data.get('budget').isdigit():
            liked_user_budget = int(data.get('budget'))

        liked_user_bio = data.get('bio', '')
        
        liked_user_compatibility_score = None
        if isinstance(data.get('compatibility_score'), (int, float)):
            liked_user_compatibility_score = int(data.get('compatibility_score'))
        elif isinstance(data.get('compatibility_score'), str) and data.get('compatibility_score').isdigit():
            liked_user_compatibility_score = int(data.get('compatibility_score'))

        liked_user_avatar_url = data.get('avatar_url', '')
        liked_user_uid = data.get('uid', '') # The UID of the liked profile (Django PK or AI UUID)
        # liked_user_type = data.get('user_type', '') # If you add this to LikedProfile model

        # Basic validation for required fields
        if not liked_user_name or not liked_user_uid:
            return JsonResponse({'status': 'error', 'message': 'Liked user name and UID are required.'}, status=400)

        # Check if a LikedProfile with this user and liked_user_uid already exists
        if LikedProfile.objects.filter(user=request.user, liked_user_uid=liked_user_uid).exists():
            return JsonResponse({'status': 'info', 'message': 'You have already liked this profile.'})

        with transaction.atomic(): # Ensure both operations succeed or fail together
            # Save the liked profile
            LikedProfile.objects.create(
                user=request.user,
                liked_user_uid=liked_user_uid,
                liked_user_name=liked_user_name,
                liked_user_age=liked_user_age,
                liked_user_gender=liked_user_gender,
                liked_user_location=liked_user_location,
                liked_user_budget=liked_user_budget,
                liked_user_bio=liked_user_bio,
                liked_user_compatibility_score=liked_user_compatibility_score,
                liked_user_avatar_url=liked_user_avatar_url,
                # liked_user_type=liked_user_type # Uncomment if you add this field to LikedProfile model
            )

            # Create a notification for the liked user (if it's a real user)
            # Check if liked_user_uid corresponds to a real User's primary key
            try:
                # Attempt to get the User object for the liked_user_uid
                # This works if liked_user_uid is a string representation of a Django User's PK
                target_user = User.objects.get(pk=liked_user_uid)
                
                # Ensure the user is not liking their own profile
                if target_user != request.user:
                    notification_message = f"{request.user.username} liked your profile!"
                    notification_link = f"/profile/#roommate-finder-section" # Link back to their profile/roommate finder
                    Notification.objects.create(
                        recipient=target_user,
                        sender=request.user, # The user who performed the like
                        type='like',
                        message=notification_message,
                        link=notification_link
                    )
                    logger.info(f"Notification created for {target_user.username}: {notification_message}")
                else:
                    logger.info(f"User {request.user.username} liked their own profile. No notification generated.")
            except User.DoesNotExist:
                # If liked_user_uid does not correspond to a real User (e.g., it's an AI profile UUID)
                logger.info(f"Liked profile with UID {liked_user_uid} is not a real user. No notification generated.")
            except Exception as e:
                logger.error(f"Error creating notification for liked profile {liked_user_uid}: {e}")

        return JsonResponse({'status': 'success', 'message': 'Profile liked and saved successfully!'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except Exception as e:
        logger.exception("An unexpected error occurred in save_liked_profile")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def predict_rent(request):
    """
    API endpoint to predict rent using OpenAI API, providing more detailed insights.
    Saves the rent check result for authenticated users.
    """
    openai_api_key = settings.OPENAI_API_KEY
    if not openai_api_key:
        logger.error("OpenAI API key not configured. Rent prediction service disabled.")
        return JsonResponse({'status': 'error', 'message': 'Rent prediction service is currently unavailable. API key not configured.'}, status=503)

    try:
        data = json.loads(request.body)
        postcode = data.get('postcode', '').strip()
        bedrooms = data.get('bedrooms')

        if not all([postcode, bedrooms]):
            return JsonResponse({'status': 'error', 'message': 'Postcode and number of bedrooms are required.'}, status=400)
        
        # Prepare a more detailed prompt for OpenAI
        prompt = f"""
        Act as a UK property market expert. Given the postcode "{postcode}" and number of bedrooms "{bedrooms}",
        provide the following information in a JSON format.
        
        1.  **estimated_rent**: An estimated monthly rent in GBP (£), as a whole number.
        2.  **rent_range**: A plausible range for the rent (e.g., "£X - £Y pcm").
        3.  **amenity_impact**: A brief, 1-2 sentence analysis of how local amenities (e.g., transport links, schools, parks, shops) might influence rent in this specific postcode. If no specific local amenities are known, provide a general statement.
        4.  **market_trend**: A brief, 1-2 sentence description of the current market trend for rentals in this area (e.g., "stable," "slight increase," "high demand").
        5.  **cost_breakdown**: Estimated monthly costs for utilities (electricity, gas, water, internet) and council tax for a property of this size in a typical UK city, as a whole number. Provide this as a dictionary with keys 'utilities' and 'council_tax'.
        
        Ensure the response is ONLY a JSON object and contains all these keys.
        Example response format:
        {{
            "estimated_rent": 1500,
            "rent_range": "£1400 - £1600 pcm",
            "amenity_impact": "Proximity to central London transport hubs significantly drives up rental prices.",
            "market_trend": "The rental market in this area is currently experiencing high demand, leading to slight increases.",
            "cost_breakdown": {{
                "utilities": 150,
                "council_tax": 100
            }}
        }}
        """
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-3.5-turbo", # Or gpt-4, gpt-4o if available and desired
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7, # Balance creativity and factual accuracy
                "response_format": {"type": "json_object"} # Crucial for getting JSON back
            }
        )
        response.raise_for_status()
        
        # Parse the JSON response from OpenAI
        ai_response_content = response.json()['choices'][0]['message']['content']
        rent_data = json.loads(ai_response_content)

        # Extract predicted_rent and range, and other new fields
        predicted_rent_value = rent_data.get('estimated_rent')
        rent_range_str = rent_data.get('rent_range')
        amenity_impact = rent_data.get('amenity_impact', 'N/A')
        market_trend = rent_data.get('market_trend', 'N/A')
        cost_breakdown = rent_data.get('cost_breakdown', {'utilities': None, 'council_tax': None})
        
        # Save the rent check result if the user is authenticated
        if request.user.is_authenticated:
            # Ensure estimated_rent is a Decimal for the model
            estimated_rent_decimal = None
            if predicted_rent_value is not None:
                try:
                    estimated_rent_decimal = Decimal(str(predicted_rent_value)) # Convert to Decimal
                except (ValueError, TypeError):
                    logger.warning(f"Invalid estimated_rent from OpenAI: {predicted_rent_value}")

            RentCheck.objects.create(
                user=request.user,
                postcode=postcode,
                bedrooms=bedrooms,
                estimated_rent=estimated_rent_decimal # Save as Decimal
            )

        return JsonResponse({
            'status': 'success',
            'message': "Rent prediction and insights generated by AI.",
            'data': {
                'predicted_rent': f"£{predicted_rent_value:,} pcm" if predicted_rent_value is not None else 'N/A',
                'range': rent_range_str,
                'amenity_impact': amenity_impact,
                'market_trend': market_trend,
                'cost_breakdown': cost_breakdown
            }
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API request failed for rent prediction: {e}")
        return JsonResponse({'status': 'error', 'message': f'Failed to connect to AI rent prediction service: {e}'}, status=500)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI response JSON for rent prediction: {e}. Content: {ai_response_content}")
        return JsonResponse({'status': 'error', 'message': 'AI service returned an unreadable response for rent prediction. Please try again.'}, status=500)
    except Exception as e:
        logger.exception("An unexpected error occurred in predict_rent")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)


@login_required
@require_http_methods(["GET"])
def get_complaints(request):
    """API endpoint to get a user's complaints."""
    complaints = Complaint.objects.filter(user=request.user).order_by('-submitted_at').values(
        'id', 'issue_type', 'property_address', 'landlord_name', 'description', 'status', 'submitted_at'
    )
    return JsonResponse({'status': 'success', 'message': 'Complaints retrieved.', 'data': {'complaints': list(complaints)}})

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def submit_complaint(request):
    """API endpoint to submit a new complaint."""
    try:
        data = json.loads(request.body)
        if not all(k in data for k in ['issue_type', 'property_address', 'description']):
            return JsonResponse({'status': 'error', 'message': 'Missing required complaint fields (issue type, address, description).'}, status=400)

        Complaint.objects.create(
            user=request.user,
            issue_type=data['issue_type'],
            property_address=data['property_address'],
            landlord_name=data.get('landlord_name', ''),
            description=data['description']
        )
        return JsonResponse({'status': 'success', 'message': 'Complaint submitted successfully!'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except Exception as e:
        logger.exception("An unexpected error occurred in submit_complaint")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@login_required
@require_http_methods(["GET"])
def get_reviews(request):
    """API endpoint to get all landlord reviews."""
    reviews = LandlordReview.objects.all().order_by('-reviewed_at').values(
        'id', 'landlord_name', 'rating', 'comments', 'property_address', 'reviewed_at', 'user__username'
    )
    return JsonResponse({'status': 'success', 'message': 'Reviews retrieved.', 'data': {'reviews': list(reviews)}})

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def submit_review(request):
    """API endpoint to submit a new landlord review."""
    try:
        data = json.loads(request.body)
        rating = data.get('rating')
        if not all(k in data for k in ['landlord_name', 'comments', 'property_address']) or not (isinstance(rating, int) and 1 <= rating <= 5):
            return JsonResponse({'status': 'error', 'message': 'Missing required review fields (landlord name, rating (1-5), comments, address).'}, status=400)

        LandlordReview.objects.create(
            user=request.user,
            landlord_name=data['landlord_name'],
            rating=int(data['rating']),
            comments=data['comments'],
            property_address=data['property_address']
        )
        return JsonResponse({'status': 'success', 'message': 'Review submitted successfully!'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except Exception as e:
        logger.exception("An unexpected error occurred in submit_review")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@login_required
@require_http_methods(["GET"])
def get_forum_posts(request):
    """API endpoint to get all forum posts."""
    posts = ForumPost.objects.all().order_by('-created_at').values(
        'id', 'title', 'content', 'category', 'created_at', 'user__username'
    )
    return JsonResponse({'status': 'success', 'message': 'Forum posts retrieved.', 'data': {'posts': list(posts)}})

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def submit_forum_post(request):
    """API endpoint to submit a new forum post."""
    try:
        data = json.loads(request.body)
        if not all(k in data for k in ['title', 'content', 'category']):
            return JsonResponse({'status': 'error', 'message': 'Missing required forum post fields (title, content, category).'}, status=400)

        ForumPost.objects.create(
            user=request.user,
            title=data['title'],
            content=data['content'],
            category=data['category']
        )
        return JsonResponse({'status': 'success', 'message': 'Post submitted successfully!'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except Exception as e:
        logger.exception("An unexpected error occurred in submit_forum_post")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)
        
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def refine_text_api(request):
    """API endpoint to refine text using OpenAI API."""
    openai_api_key = settings.OPENAI_API_KEY
    if not openai_api_key:
        logger.error("OpenAI API key not configured. Text refinement service disabled.")
        return JsonResponse({'status': 'error', 'message': 'Text refinement service is currently unavailable. API key not configured.'}, status=503)
    try:
        data = json.loads(request.body)
        original_text = data.get('text')
        if not original_text:
            return JsonResponse({'status': 'error', 'message': 'No text provided for refinement.'}, status=400)

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are an assistant that refines complaint texts to be clear, concise, and professional for a UK audience. Keep responses under 200 words."},
                    {"role": "user", "content": f"Refine this complaint: \"{original_text}\""}
                ],
                "max_tokens": 200
            }
        )
        response.raise_for_status()
        refined_text = response.json()['choices'][0]['message']['content']
        return JsonResponse({'status': 'success', 'message': 'Text refined successfully.', 'data': {'refined_text': refined_text}})
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API request failed for text refinement: {e}")
        return JsonResponse({'status': 'error', 'message': f'Failed to connect to AI text refinement service: {e}'}, status=500)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI response JSON for text refinement: {e}")
        return JsonResponse({'status': 'error', 'message': 'AI service returned an unreadable response for text refinement.'}, status=500)
    except Exception as e:
        logger.exception("An unexpected error occurred in refine_text_api")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def generate_forum_idea_api(request):
    """API endpoint to generate forum post ideas using OpenAI API."""
    openai_api_key = settings.OPENAI_API_KEY
    if not openai_api_key:
        logger.error("OpenAI API key not configured. Forum idea generation service disabled.")
        return JsonResponse({'status': 'error', 'message': 'Forum idea generation service is currently unavailable. API key not configured.'}, status=503)
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        if not query:  
            return JsonResponse({'status': 'success', 'message': 'No query provided.', 'data': {'suggestions': []}})
        
        # Corrected to use requests.post for OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are an assistant that generates engaging UK-focused forum post ideas for tenants. Provide a short, catchy title and a brief starting question."},
                    {"role": "user", "content": f"Generate a forum post idea about: \"{query}\""}
                ],
                "max_tokens": 100
            }
        )
        response.raise_for_status()
        idea_text = response.json()['choices'][0]['message']['content']
        return JsonResponse({'status': 'success', 'message': 'Forum idea generated.', 'data': {'idea_text': idea_text}})
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API request failed for forum idea: {e}")
        return JsonResponse({'status': 'error', 'message': f'Failed to connect to AI forum idea service: {e}'}, status=500)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI response JSON for forum idea: {e}")
        return JsonResponse({'status': 'error', 'message': 'AI service returned an unreadable response for forum idea.'}, status=500)
    except Exception as e:
        logger.exception("An unexpected error occurred in generate_forum_idea_api")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def get_address_suggestions(request):
    """API endpoint for address suggestions using OpenCage."""
    opencage_api_key = settings.OPENCAGE_API_KEY
    if not opencage_api_key:
        logger.error("OpenCage API key not configured. Address suggestion service disabled.")
        return JsonResponse({'status': 'error', 'message': 'Address suggestion service is not configured. API key missing.'}, status=503)
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        if not query:  
            return JsonResponse({'status': 'success', 'message': 'No query provided.', 'data': {'suggestions': []}})
        
        # Corrected to use requests.get for OpenCage API
        response = requests.get(
            "https://api.opencagedata.com/geocode/v1/json",
            params={'q': query, 'key': opencage_api_key, 'countrycode': 'gb', 'limit': 5}
        )
        response.raise_for_status()
        suggestions = [res['formatted'] for res in response.json().get('results', [])]
        return JsonResponse({'status': 'success', 'message': 'Address suggestions retrieved.', 'data': {'suggestions': suggestions}})
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenCage API request failed: {e}")
        return JsonResponse({'status': 'error', 'message': f'Failed to connect to address suggestion service: {e}'}, status=500)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenCage response JSON: {e}")
        return JsonResponse({'status': 'error', 'message': 'AI service returned an unreadable response.'}, status=500)
    except Exception as e:
        logger.exception("An unexpected error occurred in get_address_suggestions")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def analyze_contract_api(request):
    """
    API endpoint to analyze rental contract text using OpenAI API.
    Saves the original text and the AI's analysis result for authenticated users.
    """
    openai_api_key = settings.OPENAI_API_KEY # Use OpenAI API key
    if not openai_api_key:
        logger.error("OpenAI API key not configured. Contract analysis service disabled.")
        return JsonResponse({'status': 'error', 'message': 'Contract analysis service is currently unavailable. API key not configured.'}, status=503)

    try:
        data = json.loads(request.body)
        contract_text = data.get('contract_text', '').strip()

        if not contract_text:
            return JsonResponse({'status': 'error', 'message': 'No contract text provided for analysis.'}, status=400)
        
        # Define a comprehensive prompt for the AI
        prompt = f"""
        You are a highly knowledgeable AI assistant specializing in UK residential tenancy law.
        Analyze the following rental contract text and provide a concise, clear, and actionable summary.
        Focus on identifying:
        
        1.  **Key Terms**: Rent amount, payment frequency, tenancy start/end dates, notice periods (for both landlord and tenant).
        2.  **Tenant Obligations**: Major responsibilities (e.g., repairs, cleanliness, pets, sub-letting).
        3.  **Landlord Obligations**: Key responsibilities (e.g., repairs, gas safety, deposit protection).
        4.  **Potentially Unfair Clauses**: Highlight any clauses that might be considered unfair or unenforceable under UK consumer law or tenancy legislation (e.g., excessive charges, broad exclusion clauses). Explain why they might be unfair.
        5.  **Important Rights**: Briefly mention key tenant rights relevant to the contract (e.g., right to quiet enjoyment, deposit protection).
        6.  **Actionable Advice**: Provide 1-2 practical next steps or considerations for the tenant based on the analysis.
        
        Present the information clearly using bullet points or numbered lists under each heading.
        Crucially, include a **DISCLAIMER** at the very beginning and end stating: "This analysis is for informational purposes only and does not constitute legal advice. For specific legal guidance, consult a qualified solicitor or housing expert."
        
        Contract Text:
        ---
        {contract_text}
        ---
        """
        
        # Correct API call for OpenAI's chat completions API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-3.5-turbo", # Using gpt-3.5-turbo as it's a common OpenAI model
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5, # Keep temperature lower for more factual/less creative output
                "max_tokens": 1500 # Allow for a comprehensive analysis
            }
        )
        response.raise_for_status()
        
        ai_analysis_content = response.json()['choices'][0]['message']['content']

        # Save the contract and analysis result if the user is authenticated
        if request.user.is_authenticated:
            RentalContract.objects.create(
                user=request.user,
                original_text=contract_text,
                analysis_result=ai_analysis_content
            )

        return JsonResponse({
            'status': 'success',
            'message': "Rental contract analyzed successfully!",
            'data': {
                'analysis_result': ai_analysis_content
            }
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API request failed for contract analysis: {e}")
        return JsonResponse({'status': 'error', 'message': f'Failed to connect to AI contract analysis service: {e}. Please ensure your API key is valid and the service is available.'}, status=500)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to parse OpenAI response JSON for contract analysis: {e}. Content: {response.text if 'response' in locals() else 'N/A'}")
        return JsonResponse({'status': 'error', 'message': 'AI service returned an unreadable response for contract analysis. Please try again.'}, status=500)
    except Exception as e:
        logger.exception("An unexpected error occurred in analyze_contract_api")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def check_rent_declaration_api(request):
    """
    API endpoint to check for discrepancies between actual rent paid and estimated council tax.
    Uses OpenAI API for analysis and saves the result.
    """
    openai_api_key = settings.OPENAI_API_KEY
    if not openai_api_key:
        logger.error("OpenAI API key not configured. Rent declaration check service disabled.")
        return JsonResponse({'status': 'error', 'message': 'Rent declaration check service is currently unavailable. API key not configured.'}, status=503)

    try:
        data = json.loads(request.body)
        postcode = data.get('postcode', '').strip()
        bedrooms = data.get('bedrooms', '').strip()
        actual_rent_paid = data.get('actual_rent_paid')
        council_tax_band = data.get('council_tax_band', '').strip()

        # Basic validation
        if not all([postcode, bedrooms, actual_rent_paid, council_tax_band]):
            return JsonResponse({'status': 'error', 'message': 'All fields (Postcode, Bedrooms, Actual Rent Paid, Council Tax Band) are required.'}, status=400)
        
        try:
            actual_rent_paid = float(actual_rent_paid)
            if actual_rent_paid <= 0:
                raise ValueError("Actual rent paid must be a positive number.")
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid value for Actual Rent Paid. Must be a positive number.'}, status=400)

        # Construct prompt for OpenAI
        prompt = f"""
        Act as a UK property and council tax expert. A tenant in the UK is paying £{actual_rent_paid} per month for a {bedrooms}-bedroom property with postcode {postcode}, which is in Council Tax Band {council_tax_band}.

        Please provide the following information in JSON format:

        1.  **estimated_council_tax**: An estimated monthly council tax amount for a property of this size and band in this postcode area (as a whole number in GBP, e.g., 150). If specific data is not available, provide a reasonable estimate for a typical UK property in that band.
        2.  **common_rent_for_band_area**: A general estimate of common monthly rent for a {bedrooms}-bedroom property in Council Tax Band {council_tax_band} in the {postcode} area (as a whole number in GBP, e.g., 1200).
        3.  **discrepancy_found**: A boolean (true/false) indicating if there appears to be a significant discrepancy between the actual rent paid (£{actual_rent_paid}) and what might be expected given the council tax band and typical rents for the area. Consider if the rent seems unusually high or low relative to the council tax band.
        4.  **analysis_result**: A concise, 2-3 sentence explanation of the findings. If a discrepancy is found, suggest potential reasons (e.g., property misrepresented, market changes, specific amenities) and actionable advice for the tenant (e.g., "Contact your local council for official council tax records," "Seek advice from a housing charity if you suspect fraud," "Research local rental comparables."). If no significant discrepancy, state that.

        Ensure the response is ONLY a JSON object and contains all these keys.
        Example response format:
        {{
            "estimated_council_tax": 180,
            "common_rent_for_band_area": 1600,
            "discrepancy_found": true,
            "analysis_result": "The rent of £{actual_rent_paid} seems significantly higher than typical for a {bedrooms}-bedroom property in Council Tax Band {council_tax_band} in {postcode}. This could indicate a misrepresentation of the property's value or other factors. We recommend contacting your local council to verify the property's council tax banding and seeking advice from a housing charity."
        }}
        """
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-3.5-turbo", # Use a suitable model
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7, # Balance creativity and factual accuracy
                "response_format": {"type": "json_object"}
            }
        )
        response.raise_for_status()
        
        ai_response_content = response.json()['choices'][0]['message']['content']
        declaration_data = json.loads(ai_response_content)

        # Extract data from AI response
        estimated_council_tax = declaration_data.get('estimated_council_tax')
        discrepancy_found = declaration_data.get('discrepancy_found', False)
        analysis_result = declaration_data.get('analysis_result', 'No analysis provided.')

        # Save the rent declaration check result for authenticated users
        if request.user.is_authenticated:
            RentDeclarationCheck.objects.create(
                user=request.user,
                postcode=postcode,
                bedrooms=bedrooms,
                actual_rent_paid=actual_rent_paid,
                council_tax_band=council_tax_band,
                estimated_council_tax=estimated_council_tax,
                discrepancy_found=discrepancy_found,
                analysis_result=analysis_result
            )

        return JsonResponse({
            'status': 'success',
            'message': "Rent declaration check completed.",
            'data': {
                'estimated_council_tax': estimated_council_tax,
                'common_rent_for_band_area': declaration_data.get('common_rent_for_band_area'),
                'discrepancy_found': discrepancy_found,
                'analysis_result': analysis_result
            }
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API request failed for rent declaration check: {e}")
        return JsonResponse({'status': 'error', 'message': f'Failed to connect to AI service: {e}. Please ensure your API key is valid and the service is available.'}, status=500)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to parse OpenAI response JSON for rent declaration check: {e}. Content: {ai_response_content if 'ai_response_content' in locals() else 'N/A'}")
        return JsonResponse({'status': 'error', 'message': 'AI service returned an unreadable response. Please try again.'}, status=500)
    except Exception as e:
        logger.exception("An unexpected error occurred in check_rent_declaration_api")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def send_chat_message(request):
    """
    API endpoint to send a chat message.
    Messages can be sent between two real users (using their Django PKs)
    or between a real user and an AI profile (using its UUID).
    """
    try:
        data = json.loads(request.body)
        receiver_uid = data.get('receiver_uid')
        message_text = data.get('message', '').strip()

        if not receiver_uid or not message_text:
            return JsonResponse({'status': 'error', 'message': 'Receiver UID and message are required.'}, status=400)
        
        # Determine sender and receiver to store in the database
        sender_uid = str(request.user.pk)

        # For simplicity, we'll store messages as is.
        # In a more complex system, you might want to differentiate
        # between real user UIDs (Django PKs) and AI UIDs (UUID strings).
        ChatMessage.objects.create(
            sender_uid=sender_uid,
            receiver_uid=receiver_uid,
            message=message_text
        )

        # Optional: Create a notification for the receiver if they are a real user
        try:
            target_user = User.objects.get(pk=receiver_uid)
            if target_user != request.user: # Don't notify self
                Notification.objects.create(
                    recipient=target_user,
                    sender=request.user,
                    type='message',
                    message=f"New message from {request.user.username}: '{message_text[:50]}...'",
                    link=f"/profile/#chat-modal" # Could link directly to chat with sender if possible
                )
        except User.DoesNotExist:
            logger.info(f"Receiver {receiver_uid} is not a real user (or does not exist). No message notification created.")
        except Exception as e:
            logger.error(f"Error creating message notification for {receiver_uid}: {e}")

        return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except Exception as e:
        logger.exception("An unexpected error occurred in send_chat_message")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)


@login_required
@require_http_methods(["GET"])
def get_chat_messages(request, partner_uid):
    """
    API endpoint to retrieve chat messages between the current user and a specific partner (real user or AI).
    Messages are ordered by timestamp.
    """
    current_user_uid = str(request.user.pk)

    # Fetch messages where current user is sender AND partner is receiver
    messages = ChatMessage.objects.filter(
        (Q(sender_uid=current_user_uid) & Q(receiver_uid=partner_uid)) |
        (Q(sender_uid=partner_uid) & Q(receiver_uid=current_user_uid))
    ).order_by('timestamp').values('sender_uid', 'message', 'timestamp')

    # Convert messages to a list of dicts for JSON serialization
    message_list = []
    for msg in messages:
        # Convert datetime objects to ISO format string for JSON
        msg_timestamp = msg['timestamp'].isoformat() if msg['timestamp'] else None
        message_list.append({
            'sender_uid': msg['sender_uid'],
            'message': msg['message'],
            'timestamp': msg_timestamp
        })

    return JsonResponse({'status': 'success', 'messages': message_list})

@login_required
@require_http_methods(["GET"])
def get_notifications(request):
    """
    API endpoint to retrieve notifications for the current user.
    Includes an optional 'unread_only' parameter.
    """
    unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
    
    notifications_query = Notification.objects.filter(recipient=request.user)
    if unread_only:
        notifications_query = notifications_query.filter(is_read=False)
    
    notifications = notifications_query.order_by('-created_at').values(
        'id', 'type', 'message', 'link', 'created_at', 'is_read', 'sender__username'
    )

    notification_list = []
    for notif in notifications:
        notification_list.append({
            'id': notif['id'],
            'type': notif['type'],
            'message': notif['message'],
            'link': notif['link'],
            'created_at': notif['created_at'].isoformat() if notif['created_at'] else None,
            'is_read': notif['is_read'],
            'sender_username': notif['sender__username'] if notif['sender__username'] else 'System'
        })
    
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()

    return JsonResponse({
        'status': 'success',
        'notifications': notification_list,
        'unread_count': unread_count
    })

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def mark_notification_read(request):
    """
    API endpoint to mark one or all notifications as read for the current user.
    Expects 'notification_id' (single ID) or 'mark_all' (boolean) in the request body.
    """
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        mark_all = data.get('mark_all', False)

        if mark_all:
            # Mark all unread notifications for the user as read
            count, _ = Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success', 'message': f'Marked {count} notifications as read.'})
        elif notification_id:
            # Mark a specific notification as read
            notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
            if not notification.is_read:
                notification.is_read = True
                notification.save()
                return JsonResponse({'status': 'success', 'message': 'Notification marked as read.'})
            else:
                return JsonResponse({'status': 'info', 'message': 'Notification was already read.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No notification ID or mark_all flag provided.'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except Exception as e:
        logger.exception("An unexpected error occurred in mark_notification_read")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)
