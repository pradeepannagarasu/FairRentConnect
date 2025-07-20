document.addEventListener('DOMContentLoaded', function() {
    // --- CSRF Token Setup ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // --- DOM Element References (Centralized for common elements) ---
    const DOM = {
        // Global Alerts
        alertToast: document.getElementById('alert-toast'),
        alertMessage: document.getElementById('alert-message'),

        // All modal close buttons (shared class)
        closeModalBtns: document.querySelectorAll('.close-modal-btn'),

        // Index Page Modals
        rentCheckerModal: document.getElementById('rent-checker-modal'),
        landlordReviewsModal: document.getElementById('landlord-reviews-modal'),
        complaintSubmissionModal: document.getElementById('complaint-submission-modal'),
        communityForumsModal: document.getElementById('community-forums-modal'),
        legalSupportModal: document.getElementById('legal-support-modal'),
        rentalContractModal: document.getElementById('rental-contract-modal'),
        forumPostModal: document.getElementById('forum-post-modal'), // Nested modal
        legalAiModal: document.getElementById('legal-ai-modal'), // Nested modal

        // Index Page Forms/Elements
        heroRentCheckerForm: document.getElementById('hero-rent-checker-form'),
        heroModalPostcode: document.getElementById('hero_modal_postcode'),
        heroModalBedrooms: document.getElementById('hero_modal_bedrooms'),

        rentCheckerForm: document.getElementById('rent-checker-form'), // Main rent checker form inside modal
        modalPostcode: document.getElementById('modal_postcode'), // Input inside rent checker modal
        modalBedrooms: document.getElementById('modal_bedrooms'), // Select inside rent checker modal
        modalRentResults: document.getElementById('modal-rent-results'),
        modalRentPredictionLoader: document.getElementById('modal-rent-prediction-loader'),
        modalRentPredictionOutput: document.getElementById('modal-rent-prediction-output'),
        modalRentPredictionMessage: document.getElementById('modal-rent-prediction-message'),
        amenityImpactOutput: document.getElementById('amenity-impact-output'),
        marketTrendOutput: document.getElementById('market-trend-output'),
        utilitiesCostOutput: document.getElementById('utilities-cost-output'),
        councilTaxOutput: document.getElementById('council-tax-output'),

        reviewForm: document.getElementById('review-form'),
        recentReviewsList: document.getElementById('recent-reviews-list'),
        reviewPropertyAddressInput: document.getElementById('review_property_address'),

        complaintForm: document.getElementById('complaint-form'),
        refineComplaintBtn: document.getElementById('refine-complaint-btn'),
        refinedTextLoader: document.getElementById('refined-text-loader'),
        refinedTextOutput: document.getElementById('refined-text-output'),
        refinedTextContent: document.getElementById('refined-text-content'),
        useRefinedTextBtn: document.getElementById('use-refined-text-btn'),
        complaintDescription: document.getElementById('complaint_description'),
        complaintPropertyAddressInput: document.getElementById('complaint_property_address'),

        createPostBtn: document.getElementById('create-post-btn'),
        closeForumPostModalBtn: document.getElementById('close-forum-post-modal-btn'),
        forumPostForm: document.getElementById('forum-post-form'),
        generateForumIdeaBtn: document.getElementById('generate-forum-idea-btn'),
        forumIdeaLoader: document.getElementById('forum-idea-loader'),
        forumIdeaOutput: document.getElementById('forum-idea-output'),
        forumIdeaContent: document.getElementById('forum-idea-content'),
        useForumIdeaBtn: document.getElementById('use-forum-idea-btn'),
        postTitle: document.getElementById('post_title'),
        postContent: document.getElementById('post_content'),
        recentForumPostsList: document.getElementById('recent-forum-posts-list'),

        askLegalAiBtn: document.getElementById('ask-legal-ai-btn'),
        closeLegalAiModalBtn: document.getElementById('close-legal-ai-modal-btn'),
        submitLegalQueryBtn: document.getElementById('submit-legal-query-btn'),
        legalQueryInput: document.getElementById('legal-query-input'),
        legalAiLoader: document.getElementById('legal-ai-loader'),
        legalAiOutput: document.getElementById('legal-ai-output'),
        legalAiContent: document.getElementById('legal-ai-content'),

        rentalContractForm: document.getElementById('rental-contract-form'),
        contractTextarea: document.getElementById('contract_text'),
        contractAnalysisLoader: document.getElementById('contract-analysis-loader'),
        contractAnalysisOutput: document.getElementById('contract-analysis-output'),
        analysisContent: document.getElementById('analysis-content'),

        // Profile Page Elements (if applicable)
        profileModal: document.getElementById('profile-modal'),
        editProfileBtnDashboardHome: document.getElementById('edit-profile-btn-dashboard-home'),
        editProfileBtnRoommateSection: document.getElementById('edit-profile-btn-roommate-section'),
        closeProfileModalBtn: document.getElementById('close-profile-modal-btn'),
        profileFormCancelBtn: document.getElementById('profile-form-cancel-btn'),
        roommateProfileForm: document.getElementById('roommate-profile-form'),
        lifestylePreferencesTagsContainer: document.getElementById('lifestyle-preferences-tags'),
        lifestylePreferencesHiddenInput: document.getElementById('lifestyle_preferences_hidden'),
        profileLocationInput: document.getElementById('location'),

        findMatchesBtn: document.getElementById('find-matches-btn'),
        roommateMatchesLoader: document.getElementById('roommate-matches-loader'),
        roommateMatchCardDisplay: document.getElementById('roommate-match-card-display'),
        roommatePrompt: document.getElementById('roommate-prompt'),
        noMoreMatchesPrompt: document.getElementById('no-more-matches-prompt'),
        resetMatchesBtn: document.getElementById('reset-matches-btn'),
        swipeButtonsContainer: document.getElementById('swipe-buttons-container'),
        skipMatchBtn: document.getElementById('skip-match-btn'),
        likeMatchBtn: document.getElementById('like-match-btn'),

        activityDetailsModal: document.getElementById('activity-details-modal'),
        closeActivityModalBtn: document.getElementById('close-activity-modal-btn'),
        activityModalContent: document.getElementById('activity-modal-content'),
    };

    // --- Helper Function for Event Listeners ---
    function addEventListenerIfPresent(element, eventType, handler) {
        if (element) {
            element.addEventListener(eventType, handler);
        }
    }

    // --- Toast/Alert Notification ---
    function showToast(message, type = 'success') {
        if (!DOM.alertToast || !DOM.alertMessage) return;
        DOM.alertMessage.textContent = message;

        DOM.alertToast.className = `fixed bottom-5 right-5 z-50 p-4 rounded-lg text-white transition-transform transform`;
        if (type === 'success') {
            DOM.alertToast.classList.add('bg-green-500');
        } else if (type === 'error') {
            DOM.alertToast.classList.add('bg-red-500');
        } else {
            DOM.alertToast.classList.add('bg-gray-700');
        }

        DOM.alertToast.classList.remove('translate-y-20', 'hidden'); // Show toast
        DOM.alertToast.classList.add('translate-y-0');

        setTimeout(() => {
            DOM.alertToast.classList.remove('translate-y-0');
            DOM.alertToast.classList.add('translate-y-20'); // Hide toast
            setTimeout(() => DOM.alertToast.classList.add('hidden'), 300); // Fully hide after transition
        }, 3000);
    }

    // --- Generic Modal Handling Helper ---
    function setupGenericModal(openTrigger, modalElement, closeButtons, initialFocusElement = null) {
        if (!modalElement) return;

        const openHandler = () => {
            modalElement.classList.remove('hidden');
            modalElement.classList.add('flex'); // Use flex to center
            modalElement.setAttribute('aria-hidden', 'false');
            modalElement.setAttribute('tabindex', '-1'); // Make modal focusable
            if (initialFocusElement) initialFocusElement.focus();
        };

        // Attach open handler to trigger(s)
        if (openTrigger) {
            if (NodeList.prototype.isPrototypeOf(openTrigger) || Array.isArray(openTrigger)) {
                openTrigger.forEach(trigger => addEventListenerIfPresent(trigger, 'click', openHandler));
            } else {
                addEventListenerIfPresent(openTrigger, 'click', openHandler);
            }
        }

        const closeHandler = () => {
            modalElement.classList.add('hidden');
            modalElement.classList.remove('flex');
            modalElement.setAttribute('aria-hidden', 'true');
            modalElement.removeAttribute('tabindex');
            // Optionally re-focus the element that opened the modal if needed for specific UX flows
        };

        // Attach close handler to close button(s)
        if (closeButtons) {
            if (NodeList.prototype.isPrototypeOf(closeButtons) || Array.isArray(closeButtons)) {
                closeButtons.forEach(btn => addEventListenerIfPresent(btn, 'click', closeHandler));
            } else {
                addEventListenerIfPresent(closeButtons, 'click', closeHandler);
            }
        }

        // Allow closing with Escape key
        addEventListenerIfPresent(document, 'keydown', (e) => {
            if (e.key === 'Escape' && !modalElement.classList.contains('hidden')) {
                closeHandler();
            }
        });
    }

    // --- API Request Helper ---
    async function apiRequest(url, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        };
        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            const result = await response.json();
            if (!response.ok) {
                const errorMessage = result.message || (result.errors ? Object.values(result.errors).flat().join(', ') : 'An unknown error occurred.');
                throw new Error(errorMessage);
            }
            return result;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error; // Re-throw to be caught by specific handlers
        }
    }

    // --- Address Suggestions (for various forms) ---
    function setupAddressSuggestions(inputElement) {
        if (!inputElement) return;

        let timeout = null;
        const datalistId = `${inputElement.id}-suggestions`;
        let datalist = document.getElementById(datalistId);
        if (!datalist) {
            datalist = document.createElement('datalist');
            datalist.id = datalistId;
            inputElement.setAttribute('list', datalistId);
            document.body.appendChild(datalist);
        }

        addEventListenerIfPresent(inputElement, 'input', () => {
            clearTimeout(timeout);
            const query = inputElement.value.trim();
            if (query.length < 3) {
                datalist.innerHTML = ''; // Clear suggestions if query too short
                return;
            }

            timeout = setTimeout(async () => {
                try {
                    const result = await apiRequest('/api/address_suggestions/', 'POST', { query: query });
                    if (result.status === 'success' && result.data && result.data.suggestions) {
                        datalist.innerHTML = ''; // Clear previous suggestions
                        result.data.suggestions.forEach(suggestion => {
                            const option = document.createElement('option');
                            option.value = suggestion;
                            datalist.appendChild(option);
                        });
                    } else {
                        console.warn('Address suggestions API did not return success:', result.message);
                    }
                } catch (error) {
                    console.error('Error fetching address suggestions:', error);
                }
            }, 300); // Debounce time
        });
    }

    // --- Page Specific Logic ---

    // Logic for the Index Page (/)
    if (window.location.pathname === '/') {
        // Get all service cards that open modals (using the new class name)
        const serviceCards = document.querySelectorAll('.service-card[data-service-target]');

        // Setup each main service modal using the generic function
        serviceCards.forEach(card => {
            const targetModalId = card.dataset.serviceTarget;
            const targetModal = document.getElementById(targetModalId);
            if (targetModal) {
                setupGenericModal(card, targetModal, targetModal.querySelectorAll('.close-modal-btn'));
            }
        });

        // --- Hero Section Rent Checker Form Logic ---
        if (DOM.heroRentCheckerForm) {
            addEventListenerIfPresent(DOM.heroRentCheckerForm, 'submit', (e) => {
                e.preventDefault();
                const heroPostcode = DOM.heroModalPostcode.value;
                const heroBedrooms = DOM.heroModalBedrooms.value;

                // Open the main rent checker modal
                if (DOM.rentCheckerModal) {
                    DOM.rentCheckerModal.classList.remove('hidden');
                    DOM.rentCheckerModal.classList.add('flex');

                    // Pre-fill modal form fields
                    if (DOM.modalPostcode) DOM.modalPostcode.value = heroPostcode;
                    if (DOM.modalBedrooms) DOM.modalBedrooms.value = heroBedrooms;
                }
            });
        }
        // Setup address suggestions for the hero rent checker postcode input
        setupAddressSuggestions(DOM.heroModalPostcode);


        // --- Rent Checker Modal Form Logic ---
        if (DOM.rentCheckerForm) {
            addEventListenerIfPresent(DOM.rentCheckerForm, 'submit', async (e) => {
                e.preventDefault();
                DOM.modalRentResults.classList.add('hidden');
                DOM.modalRentPredictionLoader.classList.remove('hidden');
                DOM.modalRentPredictionOutput.textContent = '';
                DOM.modalRentPredictionMessage.textContent = '';
                DOM.amenityImpactOutput.textContent = '';
                DOM.marketTrendOutput.textContent = '';
                DOM.utilitiesCostOutput.textContent = '';
                DOM.councilTaxOutput.textContent = '';

                const formData = new FormData(DOM.rentCheckerForm);
                const data = Object.fromEntries(formData.entries());

                try {
                    const result = await apiRequest('/api/predict_rent/', 'POST', data);

                    DOM.modalRentPredictionLoader.classList.add('hidden');
                    DOM.modalRentResults.classList.remove('hidden');

                    if (result.status === 'success') {
                        DOM.modalRentPredictionOutput.textContent = result.data.predicted_rent;
                        DOM.modalRentPredictionMessage.textContent = result.data.range;
                        DOM.amenityImpactOutput.textContent = result.data.amenity_impact;
                        DOM.marketTrendOutput.textContent = result.data.market_trend;
                        DOM.utilitiesCostOutput.textContent = `£${result.data.cost_breakdown.utilities || 'N/A'}`;
                        DOM.councilTaxOutput.textContent = `£${result.data.cost_breakdown.council_tax || 'N/A'}`;
                        showToast(result.message, 'success');
                    } else {
                        DOM.modalRentPredictionOutput.textContent = 'Error';
                        DOM.modalRentPredictionMessage.textContent = result.message || 'Failed to predict rent.';
                        showToast(result.message || 'Failed to predict rent.', 'error');
                    }
                } catch (error) {
                    console.error('Network error:', error);
                    DOM.modalRentPredictionLoader.classList.add('hidden');
                    DOM.modalRentResults.classList.remove('hidden');
                    DOM.modalRentPredictionOutput.textContent = 'Error';
                    DOM.modalRentPredictionMessage.textContent = 'Network error. Please try again.';
                    showToast('Network error. Please try again.', 'error');
                }
            });
        }
        // Setup address suggestions for the modal rent checker postcode input
        setupAddressSuggestions(DOM.modalPostcode);


        // --- Landlord Review Form Logic ---
        async function fetchRecentReviews() {
            if (!DOM.recentReviewsList) return;
            DOM.recentReviewsList.innerHTML = '<p class="text-center text-gray-500">Loading recent reviews...</p>';
            try {
                const response = await fetch('/api/reviews/');
                const result = await response.json();
                if (result.status === 'success') {
                    DOM.recentReviewsList.innerHTML = ''; // Clear existing
                    if (result.data.reviews.length > 0) {
                        result.data.reviews.forEach(review => {
                            const reviewItem = document.createElement('div');
                            reviewItem.className = 'bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-100';
                            reviewItem.innerHTML = `
                                <p class="font-semibold text-gray-800">${review.landlord_name} - <span class="text-yellow-500">${'★'.repeat(review.rating)}</span></p>
                                <p class="text-sm text-gray-600 mt-1">"${review.comments}"</p>
                                <p class="text-xs text-gray-400 mt-2">Reviewed by ${review.user__username} on ${new Date(review.reviewed_at).toLocaleDateString()}</p>
                            `;
                            DOM.recentReviewsList.appendChild(reviewItem);
                        });
                    } else {
                        DOM.recentReviewsList.innerHTML = '<p class="text-center text-gray-500 py-4">No reviews yet.</p>';
                    }
                } else {
                    DOM.recentReviewsList.innerHTML = `<p class="text-center text-red-500 py-4">Failed to load reviews: ${result.message || 'Unknown error'}</p>`;
                }
            } catch (error) {
                console.error('Error fetching reviews:', error);
                DOM.recentReviewsList.innerHTML = '<p class="text-center text-red-500 py-4">Network error loading reviews.</p>';
            }
        }

        if (DOM.reviewForm) {
            addEventListenerIfPresent(DOM.reviewForm, 'submit', async (e) => {
                e.preventDefault();
                const submitBtn = DOM.reviewForm.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Submitting...';

                const formData = new FormData(DOM.reviewForm);
                const data = Object.fromEntries(formData.entries());
                data.rating = parseInt(data.rating); // Ensure rating is an integer

                try {
                    const response = await fetch('/api/submit_review/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(data)
                    });
                    const result = await response.json();
                    if (result.status === 'success') {
                        showToast(result.message, 'success');
                        DOM.reviewForm.reset(); // Clear form
                        await fetchRecentReviews(); // Reload reviews
                    } else {
                        showToast(result.message || 'Failed to submit review.', 'error');
                        console.error('Error submitting review:', result.errors);
                    }
                } catch (error) {
                    console.error('Network error:', error);
                    showToast('Network error. Please try again.', 'error');
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Submit Review <i class="fas fa-paper-plane ml-2"></i>';
                }
            });
            // Initial load of reviews when the modal is opened
            if (DOM.landlordReviewsModal) {
                DOM.landlordReviewsModal.addEventListener('transitionend', () => {
                    if (!DOM.landlordReviewsModal.classList.contains('hidden')) {
                        fetchRecentReviews();
                    }
                });
            }
        }
        setupAddressSuggestions(DOM.reviewPropertyAddressInput);


        // --- Complaint Submission Form Logic ---
        if (DOM.complaintForm) {
            addEventListenerIfPresent(DOM.complaintForm, 'submit', async (e) => {
                e.preventDefault();
                const submitBtn = DOM.complaintForm.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Submitting...';

                const formData = new FormData(DOM.complaintForm);
                const data = Object.fromEntries(formData.entries());

                try {
                    const result = await apiRequest('/api/submit_complaint/', 'POST', data);
                    if (result.status === 'success') {
                        showToast(result.message, 'success');
                        DOM.complaintForm.reset(); // Clear form
                        if (DOM.refinedTextOutput) DOM.refinedTextOutput.classList.add('hidden'); // Hide refined text
                    } else {
                        showToast(result.message || 'Failed to submit complaint.', 'error');
                        console.error('Error submitting complaint:', result.errors);
                    }
                } catch (error) {
                    console.error('Network error:', error);
                    showToast('Network error. Please try again.', 'error');
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Submit Complaint <i class="fas fa-paper-plane ml-2"></i>';
                }
            });
        }

        if (DOM.refineComplaintBtn) {
            addEventListenerIfPresent(DOM.refineComplaintBtn, 'click', async () => {
                const originalText = DOM.complaintDescription.value.trim();
                if (originalText.length < 20) {
                    showToast('Please write a more detailed description (at least 20 characters) to refine.', 'error');
                    return;
                }

                if (DOM.refinedTextOutput) DOM.refinedTextOutput.classList.add('hidden');
                if (DOM.refinedTextLoader) DOM.refinedTextLoader.classList.remove('hidden');

                try {
                    const result = await apiRequest('/api/refine_text/', 'POST', { text: originalText });
                    if (result.status === 'success' && result.data && result.data.refined_text) {
                        if (DOM.refinedTextContent) DOM.refinedTextContent.textContent = result.data.refined_text;
                        if (DOM.refinedTextOutput) DOM.refinedTextOutput.classList.remove('hidden');
                        showToast('Text refined by AI!', 'success');
                    } else {
                        showToast(result.message || 'Failed to refine text.', 'error');
                    }
                } catch (error) {
                    showToast(error.message, 'error');
                } finally {
                    if (DOM.refinedTextLoader) DOM.refinedTextLoader.classList.add('hidden');
                }
            });
        }

        if (DOM.useRefinedTextBtn) {
            addEventListenerIfPresent(DOM.useRefinedTextBtn, 'click', () => {
                if (DOM.complaintDescription && DOM.refinedTextContent) DOM.complaintDescription.value = DOM.refinedTextContent.textContent;
                if (DOM.refinedTextOutput) DOM.refinedTextOutput.classList.add('hidden');
                showToast('Refined text applied!', 'success');
            });
        }
        setupAddressSuggestions(DOM.complaintPropertyAddressInput);


        // --- Community Forums Modal Logic ---
        // Setup the nested forum post modal
        setupGenericModal(DOM.createPostBtn, DOM.forumPostModal, DOM.closeForumPostModalBtn, DOM.postTitle);

        async function fetchRecentForumPosts() {
            if (!DOM.recentForumPostsList) return;
            DOM.recentForumPostsList.innerHTML = '<p class="text-center text-gray-500">Loading recent forum posts...</p>';
            try {
                const response = await fetch('/api/forum_posts/');
                const result = await response.json();
                if (result.status === 'success') {
                    DOM.recentForumPostsList.innerHTML = ''; // Clear existing
                    if (result.data.posts.length > 0) {
                        result.data.posts.forEach(post => {
                            const postItem = document.createElement('div');
                            postItem.className = 'bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-100';
                            postItem.innerHTML = `
                                <p class="font-semibold text-gray-800">${post.title} - <span class="text-indigo-600">${post.category}</span></p>
                                <p class="text-sm text-gray-600 mt-1">"${post.content.substring(0, 100)}..."</p>
                                <p class="text-xs text-gray-400 mt-2">By ${post.user__username} on ${new Date(post.created_at).toLocaleDateString()}</p>
                            `;
                            DOM.recentForumPostsList.appendChild(postItem);
                        });
                    } else {
                        DOM.recentForumPostsList.innerHTML = '<p class="text-center text-gray-500 py-4">No posts yet.</p>';
                    }
                } else {
                    DOM.recentForumPostsList.innerHTML = `<p class="text-center text-red-500 py-4">Failed to load posts: ${result.message || 'Unknown error'}</p>`;
                }
            } catch (error) {
                console.error('Error fetching forum posts:', error);
                DOM.recentForumPostsList.innerHTML = '<p class="text-center text-red-500 py-4">Network error loading posts.</p>';
            }
        }

        if (DOM.generateForumIdeaBtn) {
            addEventListenerIfPresent(DOM.generateForumIdeaBtn, 'click', async () => {
                const topic = document.getElementById('post_category').value || 'general tenant advice';

                if (DOM.forumIdeaOutput) DOM.forumIdeaOutput.classList.add('hidden');
                if (DOM.forumIdeaLoader) DOM.forumIdeaLoader.classList.remove('hidden');

                try {
                    const result = await apiRequest('/api/generate_forum_idea/', 'POST', { topic: topic });
                    if (result.status === 'success' && result.data && result.data.idea_text) {
                        if (DOM.forumIdeaContent) DOM.forumIdeaContent.textContent = result.data.idea_text;
                        if (DOM.forumIdeaOutput) DOM.forumIdeaOutput.classList.remove('hidden');
                        showToast('Forum idea generated by AI!', 'success');
                    } else {
                        showToast(result.message || 'Failed to generate idea.', 'error');
                    }
                } catch (error) {
                    showToast(error.message, 'error');
                } finally {
                    if (DOM.forumIdeaLoader) DOM.forumIdeaLoader.classList.add('hidden');
                }
            });
        }

        if (DOM.useForumIdeaBtn) {
            addEventListenerIfPresent(DOM.useForumIdeaBtn, 'click', () => {
                const ideaText = DOM.forumIdeaContent ? DOM.forumIdeaContent.textContent : '';
                const lines = ideaText.split('\n').filter(line => line.trim() !== '');
                if (lines.length > 0) {
                    if (DOM.postTitle) DOM.postTitle.value = lines[0].replace(/^(Title:|Question:)\s*/i, '').trim();
                    if (DOM.postContent) DOM.postContent.value = lines.slice(1).join('\n').trim();
                } else {
                    if (DOM.postContent) DOM.postContent.value = ideaText; // Fallback
                }
                if (DOM.forumIdeaOutput) DOM.forumIdeaOutput.classList.add('hidden');
                showToast('AI idea applied to form!', 'success');
            });
        }

        if (DOM.forumPostForm) {
            addEventListenerIfPresent(DOM.forumPostForm, 'submit', async (e) => {
                e.preventDefault();
                const submitBtn = DOM.forumPostForm.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Submitting...';

                const formData = new FormData(DOM.forumPostForm);
                const data = Object.fromEntries(formData.entries());

                try {
                    const result = await apiRequest('/api/submit_forum_post/', 'POST', data);
                    if (result.status === 'success') {
                        showToast(result.message, 'success');
                        DOM.forumPostForm.reset(); // Clear form
                        if (DOM.forumIdeaOutput) DOM.forumIdeaOutput.classList.add('hidden'); // Hide idea
                        if (DOM.forumPostModal) {
                            DOM.forumPostModal.classList.add('hidden'); // Close modal
                            DOM.forumPostModal.classList.remove('flex');
                        }
                        await fetchRecentForumPosts(); // Reload posts
                    } else {
                        showToast(result.message || 'Failed to submit post.', 'error');
                        console.error('Error submitting post:', result.errors);
                    }
                } catch (error) {
                    console.error('Network error:', error);
                    showToast('Network error. Please try again.', 'error');
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Submit Post <i class="fas fa-paper-plane ml-2"></i>';
                }
            });
        }
        // Load posts when the main community forums modal is opened
        if (DOM.communityForumsModal) {
            DOM.communityForumsModal.addEventListener('transitionend', () => {
                if (!DOM.communityForumsModal.classList.contains('hidden')) {
                    fetchRecentForumPosts();
                }
            });
        }


        // --- Legal AI Logic ---
        setupGenericModal(DOM.askLegalAiBtn, DOM.legalAiModal, DOM.closeLegalAiModalBtn, DOM.legalQueryInput);

        if (DOM.submitLegalQueryBtn) {
            addEventListenerIfPresent(DOM.submitLegalQueryBtn, 'click', async () => {
                const query = DOM.legalQueryInput.value.trim();
                if (query.length < 10) {
                    showToast('Please enter a more detailed question (at least 10 characters).', 'error');
                    return;
                }

                if (DOM.legalAiOutput) DOM.legalAiOutput.classList.add('hidden');
                if (DOM.legalAiLoader) DOM.legalAiLoader.classList.remove('hidden');

                try {
                    const result = await apiRequest('/api/refine_text/', 'POST', { text: `Provide general information on UK rental law for this query: "${query}". Keep it concise and state it's not legal advice.` });
                    
                    if (result.status === 'success' && result.data && result.data.refined_text) {
                        if (DOM.legalAiContent) DOM.legalAiContent.textContent = result.data.refined_text;
                        if (DOM.legalAiOutput) DOM.legalAiOutput.classList.remove('hidden');
                        showToast('AI answer generated!', 'success');
                    } else {
                        showToast(result.message || 'Failed to get AI answer.', 'error');
                    }
                } catch (error) {
                    showToast(error.message, 'error');
                } finally {
                    if (DOM.legalAiLoader) DOM.legalAiLoader.classList.add('hidden');
                }
            });
        }

        // --- NEW: Rental Contract Analyzer Logic ---
        if (DOM.rentalContractForm) {
            addEventListenerIfPresent(DOM.rentalContractForm, 'submit', async (e) => {
                e.preventDefault();
                const contractText = DOM.contractTextarea.value.trim();

                if (!contractText) {
                    showToast('Please paste your contract text to analyze.', 'error');
                    return;
                }
                if (contractText.length < 100) { // Minimum length for meaningful analysis
                    showToast('Please provide more text for a meaningful analysis (min 100 characters).', 'error');
                    return;
                }

                if (DOM.contractAnalysisOutput) DOM.contractAnalysisOutput.classList.add('hidden');
                if (DOM.contractAnalysisLoader) DOM.contractAnalysisLoader.classList.remove('hidden');
                const submitBtn = DOM.rentalContractForm.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Analyzing...';

                try {
                    const response = await fetch('/api/analyze_contract/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({ contract_text: contractText })
                    });
                    const result = await response.json();

                    if (DOM.contractAnalysisLoader) DOM.contractAnalysisLoader.classList.add('hidden');
                    if (DOM.contractAnalysisOutput) DOM.contractAnalysisOutput.classList.remove('hidden');

                    if (result.status === 'success' && result.data && result.data.analysis_result) {
                        // Replace newlines with <br> for proper display of markdown-like output
                        if (DOM.analysisContent) DOM.analysisContent.innerHTML = result.data.analysis_result.replace(/\n/g, '<br>');
                        showToast(result.message, 'success');
                    } else {
                        if (DOM.analysisContent) DOM.analysisContent.innerHTML = `<p class="text-red-500">${result.message || 'Failed to analyze contract.'}</p>`;
                        showToast(result.message || 'Failed to analyze contract.', 'error');
                    }
                } catch (error) {
                    console.error('Network error:', error);
                    if (DOM.contractAnalysisLoader) DOM.contractAnalysisLoader.classList.add('hidden');
                    if (DOM.contractAnalysisOutput) DOM.contractAnalysisOutput.classList.remove('hidden');
                    if (DOM.analysisContent) DOM.analysisContent.innerHTML = '<p class="text-red-500">Network error. Please try again.</p>';
                    showToast('Network error. Please try again.', 'error');
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Analyze Contract <i class="fas fa-robot ml-2"></i>';
                }
            });
        }
    }


    // Logic for the Profile Page (/profile)
    if (window.location.pathname.includes('/profile')) {
        // --- Sidebar Navigation Logic ---
        const sidebarToggleBtn = document.getElementById('sidebar-toggle-btn');
        const sidebar = document.getElementById('sidebar');
        const contentArea = document.getElementById('content-area');
        const sidebarNavItems = document.querySelectorAll('.sidebar-nav-item');
        const contentSections = document.querySelectorAll('.content-section');

        // Toggle sidebar for mobile
        if (sidebarToggleBtn) {
            addEventListenerIfPresent(sidebarToggleBtn, 'click', () => {
                sidebar.classList.toggle('open');
                if (sidebar.classList.contains('open')) {
                    const overlay = document.createElement('div');
                    overlay.id = 'sidebar-overlay';
                    overlay.className = 'fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden';
                    document.body.appendChild(overlay);
                    addEventListenerIfPresent(overlay, 'click', () => {
                        sidebar.classList.remove('open');
                        overlay.remove();
                    });
                } else {
                    document.getElementById('sidebar-overlay')?.remove();
                }
            });
        }

        // Switch content sections based on sidebar navigation
        sidebarNavItems.forEach(item => {
            addEventListenerIfPresent(item, 'click', (e) => {
                const targetId = item.dataset.contentTarget;
                if (targetId) {
                    e.preventDefault();
                    sidebarNavItems.forEach(nav => nav.classList.remove('active', 'bg-slate-700'));
                    item.classList.add('active', 'bg-slate-700');

                    contentSections.forEach(section => section.classList.add('hidden'));
                    const targetSection = document.getElementById(targetId);
                    if (targetSection) {
                        targetSection.classList.remove('hidden');
                    }

                    if (window.innerWidth < 1024) {
                        sidebar.classList.remove('open');
                        document.getElementById('sidebar-overlay')?.remove();
                    }
                }
            });
        });

        // Initialize active sidebar item and content section on load
        document.addEventListener('DOMContentLoaded', () => {
            const initialSectionId = window.location.hash ? window.location.hash.substring(1) : 'dashboard-home';
            const initialNavItem = document.querySelector(`.sidebar-nav-item[data-content-target="${initialSectionId}"]`);
            const initialContentSection = document.getElementById(initialSectionId);

            if (initialNavItem) {
                initialNavItem.classList.add('active', 'bg-slate-700');
            } else {
                document.querySelector('.sidebar-nav-item[data-content-target="dashboard-home"]').classList.add('active', 'bg-slate-700');
            }

            if (initialContentSection) {
                initialContentSection.classList.remove('hidden');
            } else {
                document.getElementById('dashboard-home').classList.remove('hidden');
            }

            if (window.innerWidth >= 1024) {
                contentArea.style.marginLeft = '250px';
            }
        });


        // --- Roommate Profile Edit Modal Logic ---
        // Pre-defined lifestyle preferences
        const ALL_LIFESTYLE_PREFERENCES = [
            'Quiet', 'Social', 'Pet-Friendly', 'Clean', 'Messy', 'Early Bird',
            'Night Owl', 'Studious', 'Party-goer', 'Vegetarian', 'Vegan',
            'Cooks Often', 'Rarely Cooks', 'Non-Smoker', 'Smoker', 'Introvert', 'Extrovert'
        ];

        // Function to render lifestyle preference tags
        function renderLifestylePreferenceTags(selectedPreferences = []) {
            if (!DOM.lifestylePreferencesTagsContainer) return;
            DOM.lifestylePreferencesTagsContainer.innerHTML = ''; // Clear existing tags
            ALL_LIFESTYLE_PREFERENCES.forEach(pref => {
                const tag = document.createElement('span');
                tag.className = 'tag';
                tag.textContent = pref;
                if (selectedPreferences.includes(pref)) {
                    tag.classList.add('selected');
                }
                addEventListenerIfPresent(tag, 'click', () => {
                    tag.classList.toggle('selected');
                    updateLifestylePreferencesHiddenInput();
                });
                DOM.lifestylePreferencesTagsContainer.appendChild(tag);
            });
        }

        // Function to update the hidden input based on selected tags
        function updateLifestylePreferencesHiddenInput() {
            if (!DOM.lifestylePreferencesTagsContainer || !DOM.lifestylePreferencesHiddenInput) return;
            const selectedTags = Array.from(DOM.lifestylePreferencesTagsContainer.querySelectorAll('.tag.selected')).map(tag => tag.textContent);
            DOM.lifestylePreferencesHiddenInput.value = selectedTags.join(', ');
        }

        // Event listeners for opening profile modal from different buttons
        const openProfileModal = () => {
            const currentPrefsString = DOM.lifestylePreferencesHiddenInput ? DOM.lifestylePreferencesHiddenInput.value : '';
            const currentPrefsArray = currentPrefsString.split(',').map(item => item.trim()).filter(item => item.length > 0);
            renderLifestylePreferenceTags(currentPrefsArray);
            if (DOM.profileModal) {
                DOM.profileModal.classList.remove('hidden');
                DOM.profileModal.classList.add('flex');
            }
        };
        addEventListenerIfPresent(DOM.editProfileBtnDashboardHome, 'click', openProfileModal);
        addEventListenerIfPresent(DOM.editProfileBtnRoommateSection, 'click', openProfileModal);

        // Setup generic modal for profile
        setupGenericModal(null, DOM.profileModal, [DOM.closeProfileModalBtn, DOM.profileFormCancelBtn]); // Open handled by specific buttons above


        // Roommate Profile Form Submission
        if (DOM.roommateProfileForm) {
            addEventListenerIfPresent(DOM.roommateProfileForm, 'submit', async (e) => {
                e.preventDefault();
                const submitBtn = DOM.roommateProfileForm.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Saving...';

                const formData = new FormData(DOM.roommateProfileForm);
                const data = Object.fromEntries(formData.entries());
                data.age = data.age ? parseInt(data.age) : null;
                data.budget = data.budget ? parseInt(data.budget) : null;

                try {
                    const result = await apiRequest('/api/save_roommate_profile/', 'POST', data);
                    showToast(result.message || 'Profile saved successfully!', 'success');
                    setTimeout(() => {
                        if (DOM.profileModal) {
                            DOM.profileModal.classList.add('hidden');
                            DOM.profileModal.classList.remove('flex');
                        }
                        location.reload(); // Reload to update Django context and display
                    }, 1500);
                } catch (error) {
                    showToast(error.message, 'error');
                    if (DOM.profileModal) {
                        DOM.profileModal.classList.remove('hidden');
                        DOM.profileModal.classList.add('flex');
                    }
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Save Profile';
                }
            });
        }
        setupAddressSuggestions(DOM.profileLocationInput);


        // --- Roommate Match Finder Logic (Swipe UI) ---
        let currentMatches = [];
        let currentMatchIndex = 0;

        function displayCurrentMatch() {
            if (!DOM.roommateMatchCardDisplay || !DOM.roommatePrompt || !DOM.noMoreMatchesPrompt || !DOM.swipeButtonsContainer) return;

            DOM.roommateMatchCardDisplay.innerHTML = ''; // Clear current card
            DOM.roommatePrompt.classList.add('hidden');
            DOM.noMoreMatchesPrompt.classList.add('hidden');

            if (currentMatchIndex < currentMatches.length) {
                const match = currentMatches[currentMatchIndex];
                const matchCard = document.createElement('div');
                matchCard.className = 'roommate-match-card';
                matchCard.innerHTML = `
                    <img src="${match.avatar_url}" alt="${match.name}" onerror="this.onerror=null;this.src='https://placehold.co/160x160/cccccc/ffffff?text=User'">
                    <h4 class="text-3xl font-bold text-gray-900">${match.name}, ${match.age || 'N/A'}</h4>
                    <p class="text-lg text-gray-600 mb-2">${match.location || 'N/A'}</p>
                    <div class="compatibility-score">${match.compatibility_score || 'N/A'}% Match</div>
                    <p class="text-gray-700 text-sm italic max-w-xs overflow-hidden text-ellipsis whitespace-nowrap">${match.bio || 'No bio provided.'}</p>
                    <button class="match-details-btn btn-secondary mt-4" data-match='${JSON.stringify(match)}'>View Details</button>
                `;
                DOM.roommateMatchCardDisplay.appendChild(matchCard);
                DOM.swipeButtonsContainer.classList.remove('hidden');

                addEventListenerIfPresent(matchCard.querySelector('.match-details-btn'), 'click', (e) => {
                    const matchData = JSON.parse(e.target.dataset.match);
                    displayActivityDetails('Liked Profile', matchData); // Use generic modal
                });

            } else {
                DOM.roommateMatchCardDisplay.innerHTML = '';
                DOM.swipeButtonsContainer.classList.add('hidden');
                DOM.noMoreMatchesPrompt.classList.remove('hidden');
            }
        }

        async function fetchRoommateMatches() {
            if (!DOM.roommatePrompt || !DOM.noMoreMatchesPrompt || !DOM.roommateMatchesLoader || !DOM.roommateMatchCardDisplay || !DOM.swipeButtonsContainer) return;

            DOM.roommatePrompt.classList.add('hidden');
            DOM.noMoreMatchesPrompt.classList.add('hidden');
            DOM.roommateMatchesLoader.classList.remove('hidden');
            DOM.roommateMatchCardDisplay.innerHTML = ''; // Clear any previous cards
            DOM.swipeButtonsContainer.classList.add('hidden');

            try {
                const result = await apiRequest('/api/find_roommate_matches/', 'POST', {});

                DOM.roommateMatchesLoader.classList.add('hidden');

                if (result.status === 'success' && result.data && result.data.matches) {
                    currentMatches = result.data.matches;
                    currentMatchIndex = 0;
                    if (currentMatches.length > 0) {
                        displayCurrentMatch();
                    } else {
                        DOM.noMoreMatchesPrompt.classList.remove('hidden');
                    }
                } else {
                    showToast(result.message || 'Failed to find matches.', 'error');
                    DOM.roommatePrompt.classList.remove('hidden');
                }
            } catch (error) {
                console.error('Network error:', error);
                DOM.roommateMatchesLoader.classList.add('hidden');
                showToast('Network error. Please try again.', 'error');
                DOM.roommatePrompt.classList.remove('hidden');
            }
        }

        async function animateAndAdvance(direction) {
            const currentCard = DOM.roommateMatchCardDisplay.querySelector('.roommate-match-card');
            if (currentCard) {
                if (direction === 'like') {
                    const likedMatchData = currentMatches[currentMatchIndex];
                    const dataToSend = {
                        name: likedMatchData.name || '',
                        age: parseInt(likedMatchData.age) || null,
                        gender: likedMatchData.gender || '',
                        location: likedMatchData.location || '',
                        budget: parseInt(likedMatchData.budget) || null,
                        bio: likedMatchData.bio || '',
                        compatibility_score: parseInt(likedMatchData.compatibility_score) || null,
                        avatar_url: likedMatchData.avatar_url || ''
                    };

                    try {
                        const saveResult = await apiRequest('/api/save_liked_profile/', 'POST', dataToSend);
                        if (saveResult.status === 'success') {
                            showToast(saveResult.message, 'success');
                            // Animate and then reload to show updated liked profiles in activity
                            currentCard.classList.add('swiping-right');
                            currentCard.addEventListener('transitionend', () => {
                                currentMatchIndex++;
                                displayCurrentMatch();
                                location.reload(); // Reload to update liked profiles in dashboard
                            }, { once: true });
                        } else {
                            showToast(saveResult.message || 'Failed to save liked profile.', 'error');
                            console.error('Error saving liked profile:', saveResult.errors);
                        }
                    } catch (error) {
                        console.error('Network error saving liked profile:', error);
                        showToast('Network error saving liked profile. Please try again.', 'error');
                    }
                } else { // If skipping
                    currentCard.classList.add('swiping-left');
                    currentCard.addEventListener('transitionend', () => {
                        currentMatchIndex++;
                        displayCurrentMatch();
                    }, { once: true });
                }
            }
        }

        addEventListenerIfPresent(DOM.findMatchesBtn, 'click', fetchRoommateMatches);
        addEventListenerIfPresent(DOM.resetMatchesBtn, 'click', fetchRoommateMatches);
        addEventListenerIfPresent(DOM.skipMatchBtn, 'click', () => animateAndAdvance('skip'));
        addEventListenerIfPresent(DOM.likeMatchBtn, 'click', () => animateAndAdvance('like'));


        // --- Generic Activity/Service Details Modal Logic ---
        setupGenericModal(null, DOM.activityDetailsModal, DOM.closeActivityModalBtn); // Open handled by specific activity items

        function displayActivityDetails(activityType, details) {
            if (!DOM.activityModalContent || !DOM.activityDetailsModal) return;

            DOM.activityModalContent.innerHTML = ''; // Clear previous content
            let contentHtml = `<h3 class="text-2xl font-bold text-gray-900 mb-4">${activityType} Details</h3>`;

            if (activityType === 'Liked Profile') {
                contentHtml += `
                    <img src="${details.avatar_url}" alt="${details.name}" class="mx-auto mb-4 w-24 h-24 rounded-full object-cover border-4 border-blue-400" onerror="this.onerror=null;this.src='https://placehold.co/96x96/cccccc/ffffff?text=User'">
                    <h4 class="text-xl font-bold text-gray-900 mb-2">${details.name}, ${details.age || 'N/A'}</h4>
                    <p class="text-md text-gray-700 mb-4">${details.gender || 'N/A'} | ${details.location || 'N/A'}</p>
                    <div class="text-left space-y-3">
                        <div class="detail-item"><i class="fas fa-money-bill-wave"></i><span class="font-semibold">Budget:</span> £${details.budget || 'N/A'} / month</div>
                        <div class="detail-item"><i class="fas fa-user-friends"></i><span class="font-semibold">Compatibility:</span> <span class="compatibility-score-modal">${details.compatibility_score || 'N/A'}%</span></div>
                        <div class="detail-item"><i class="fas fa-info-circle"></i><span class="font-semibold">Bio:</span> ${details.bio || 'No bio provided.'}</div>
                    </div>
                    <!-- <button class="btn-primary mt-6 w-full">Connect with ${details.name}</button> -->
                `;
            } else if (activityType === 'Rent Check') {
                contentHtml += `
                    <div class="text-left space-y-3">
                        <div class="detail-item"><i class="fas fa-map-marker-alt"></i><span class="font-semibold">Postcode:</span> ${details.postcode}</div>
                        <div class="detail-item"><i class="fas fa-bed"></i><span class="font-semibold">Bedrooms:</span> ${details.bedrooms}</div>
                        <div class="detail-item"><i class="fas fa-gbp-sign"></i><span class="font-semibold">Estimated Rent:</span> £${details.estimated_rent} / month</div>
                        <div class="detail-item"><i class="fas fa-calendar-alt"></i><span class="font-semibold">Checked At:</span> ${new Date(details.checked_at).toLocaleString()}</div>
                    </div>
                `;
            } else if (activityType === 'Review') {
                contentHtml += `
                    <div class="text-left space-y-3">
                        <div class="detail-item"><i class="fas fa-user-tie"></i><span class="font-semibold">Landlord:</span> ${details.landlord_name}</div>
                        <div class="detail-item"><i class="fas fa-map-marker-alt"></i><span class="font-semibold">Property:</span> ${details.property_address}</div>
                        <div class="detail-item"><i class="fas fa-star"></i><span class="font-semibold">Rating:</span> ${details.rating} Stars</div>
                        <div class="detail-item"><i class="fas fa-comment-alt"></i><span class="font-semibold">Comments:</span> <p>${details.comments}</p></div>
                        <div class="detail-item"><i class="fas fa-calendar-alt"></i><span class="font-semibold">Reviewed At:</span> ${new Date(details.reviewed_at).toLocaleString()}</div>
                        <div class="detail-item"><i class="fas fa-user"></i><span class="font-semibold">Reviewer:</span> ${details.reviewer}</div>
                    </div>
                `;
            } else if (activityType === 'Complaint') {
                contentHtml += `
                    <div class="text-left space-y-3">
                        <div class="detail-item"><i class="fas fa-exclamation-triangle"></i><span class="font-semibold">Issue Type:</span> ${details.issue_type}</div>
                        <div class="detail-item"><i class="fas fa-map-marker-alt"></i><span class="font-semibold">Property:</span> ${details.property_address}</div>
                        <div class="detail-item"><i class="fas fa-user-tie"></i><span class="font-semibold">Landlord (Optional):</span> ${details.landlord_name || 'N/A'}</div>
                        <div class="detail-item"><i class="fas fa-file-alt"></i><span class="font-semibold">Description:</span> <p>${details.description}</p></div>
                        <div class="detail-item"><i class="fas fa-info-circle"></i><span class="font-semibold">Status:</span> ${details.status}</div>
                        <div class="detail-item"><i class="fas fa-calendar-alt"></i><span class="font-semibold">Submitted At:</span> ${new Date(details.submitted_at).toLocaleString()}</div>
                    </div>
                `;
            } else if (activityType === 'Forum Post') {
                contentHtml += `
                    <div class="text-left space-y-3">
                        <div class="detail-item"><i class="fas fa-heading"></i><span class="font-semibold">Title:</span> ${details.title}</div>
                        <div class="detail-item"><i class="fas fa-tags"></i><span class="font-semibold">Category:</span> ${details.category}</div>
                        <div class="detail-item"><i class="fas fa-file-alt"></i><span class="font-semibold">Content:</span> <p>${details.content}</p></div>
                        <div class="detail-item"><i class="fas fa-calendar-alt"></i><span class="font-semibold">Posted At:</span> ${new Date(details.created_at).toLocaleString()}</div>
                        <div class="detail-item"><i class="fas fa-user"></i><span class="font-semibold">Author:</span> ${details.author}</div>
                    </div>
                `;
            } else if (activityType === 'Contract Analysis') {
                contentHtml += `
                    <div class="text-left space-y-3">
                        <div class="detail-item"><i class="fas fa-calendar-alt"></i><span class="font-semibold">Analyzed At:</span> ${new Date(details.analyzed_at).toLocaleString()}</div>
                        <div class="detail-item"><i class="fas fa-file-alt"></i><span class="font-semibold">Original Text:</span> <p class="whitespace-pre-wrap text-sm max-h-40 overflow-y-auto border p-2 rounded">${details.original_text}</p></div>
                        <div class="detail-item"><i class="fas fa-robot"></i><span class="font-semibold">AI Analysis:</span> <p class="whitespace-pre-wrap text-sm max-h-60 overflow-y-auto border p-2 rounded">${details.analysis_result}</p></div>
                    </div>
                `;
            } else {
                contentHtml += `<p class="text-center text-gray-500">Details for this activity type are not available.</p>`;
            }

            DOM.activityModalContent.innerHTML = contentHtml;
            DOM.activityDetailsModal.classList.remove('hidden');
            DOM.activityDetailsModal.classList.add('flex');
        }

        // Event listener for clicking on Activity/Service items
        document.addEventListener('click', (event) => {
            const activityItem = event.target.closest('.activity-item[data-activity-details]');
            const serviceResultCard = event.target.closest('.service-result-card[data-activity-details]');

            if (activityItem) {
                const activityType = activityItem.dataset.activityType;
                const scriptTag = activityItem.querySelector('script[type="application/json"]');
                let details;
                if (scriptTag) {
                    try {
                        details = JSON.parse(scriptTag.textContent);
                    } catch (e) {
                        console.error('Error parsing activity details from script tag:', e);
                        showToast('Error loading activity details.', 'error');
                        return;
                    }
                } else {
                    try {
                        details = JSON.parse(activityItem.dataset.activityDetails);
                    } catch (e) {
                        console.error('Error parsing activity details from data attribute:', e);
                        showToast('Error loading activity details.', 'error');
                        return;
                    }
                }
                displayActivityDetails(activityType, details);
            } else if (serviceResultCard) {
                const activityType = serviceResultCard.dataset.activityType;
                const details = JSON.parse(serviceResultCard.dataset.activityDetails);
                displayActivityDetails(activityType, details);
            }
        });

        // Tab switching logic for My Services section
        const mainContentTabButtons = document.querySelectorAll('#my-services-section .main-content-tab-button');
        const mainContentTabContents = document.querySelectorAll('#my-services-section .main-content-tab-content');

        mainContentTabButtons.forEach(button => {
            addEventListenerIfPresent(button, 'click', () => {
                const targetTabId = button.dataset.tabId;

                mainContentTabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                mainContentTabContents.forEach(content => {
                    if (content.id === targetTabId) {
                        content.classList.remove('hidden');
                    } else {
                        content.classList.add('hidden');
                    }
                });
            });
        });
    }
});
