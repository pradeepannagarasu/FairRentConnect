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

    // --- DOM Element References (Centralized for all pages) ---
    const DOM = {
        // Global Alerts
        alertToast: document.getElementById('alert-toast'),
        alertMessage: document.getElementById('alert-message'),

        // All modal close buttons (shared class)
        closeModalBtns: document.querySelectorAll('.close-modal-btn'),

        // Index Page Modals & Elements
        rentCheckerModal: document.getElementById('rent-checker-modal'),
        landlordReviewsModal: document.getElementById('landlord-reviews-modal'),
        complaintSubmissionModal: document.getElementById('complaint-submission-modal'),
        communityForumsModal: document.getElementById('community-forums-modal'),
        legalSupportModal: document.getElementById('legal-support-modal'),
        rentalContractModal: document.getElementById('rental-contract-modal'),
        forumPostModal: document.getElementById('forum-post-modal'),
        legalAiModal: document.getElementById('legal-ai-modal'),
        heroRentCheckerForm: document.getElementById('hero-rent-checker-form'),
        heroModalPostcode: document.getElementById('hero_modal_postcode'),
        heroModalBedrooms: document.getElementById('hero_modal_bedrooms'),
        rentCheckerForm: document.getElementById('rent-checker-form'),
        modalPostcode: document.getElementById('modal_postcode'),
        modalBedrooms: document.getElementById('modal_bedrooms'),
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

        // Profile Page Elements
        sidebar: document.getElementById('sidebar'),
        sidebarToggle: document.getElementById('sidebarToggle'),
        sidebarOverlay: document.getElementById('sidebarOverlay'),
        mainContent: document.getElementById('mainContent'),
        sidebarNavItems: document.querySelectorAll('.sidebar-nav-item'),
        contentSections: document.querySelectorAll('.content-section'),
        myServicesHeaderBtn: document.getElementById('my-services-header-btn'),
        profileModal: document.getElementById('profile-modal'),
        editProfileBtnDashboardHome: document.getElementById('edit-profile-btn-dashboard-home'),
        editProfileBtnRoommateSection: document.getElementById('edit-profile-btn-roommate-section'),
        closeProfileModalBtn: document.getElementById('close-profile-modal-btn'),
        profileFormCancelBtn: document.getElementById('profile-form-cancel-btn'),
        roommateProfileForm: document.getElementById('roommate-profile-form'),
        lifestylePreferencesTagsContainer: document.getElementById('lifestyle-preferences-tags'),
        lifestylePreferencesHiddenInput: document.getElementById('lifestyle_preferences_hidden'),
        profileLocationInput: document.getElementById('location'),
        findMatchesBtn: document.getElementById('find-matches-btn-inner'), // Use the one inside the prompt
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
        mainContentTabButtons: document.querySelectorAll('#my-services-section .main-content-tab-button'),
        mainContentTabContents: document.querySelectorAll('#my-services-section .main-content-tab-content'),
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

        DOM.alertToast.classList.remove('translate-y-20', 'hidden');
        DOM.alertToast.classList.add('translate-y-0');

        setTimeout(() => {
            DOM.alertToast.classList.remove('translate-y-0');
            DOM.alertToast.classList.add('translate-y-20');
            setTimeout(() => DOM.alertToast.classList.add('hidden'), 300);
        }, 3000);
    }

    // --- Generic Modal Handling Helper ---
    function setupGenericModal(openTriggers, modalElement, closeButtons, initialFocusElement = null) {
        if (!modalElement) return;

        const openHandler = () => {
            modalElement.classList.remove('hidden');
            modalElement.classList.add('flex');
            modalElement.setAttribute('aria-hidden', 'false');
            modalElement.setAttribute('tabindex', '-1');
            if (initialFocusElement) initialFocusElement.focus();
        };

        if (openTriggers) {
            const triggers = NodeList.prototype.isPrototypeOf(openTriggers) || Array.isArray(openTriggers) ? openTriggers : [openTriggers];
            triggers.forEach(trigger => addEventListenerIfPresent(trigger, 'click', openHandler));
        }

        const closeHandler = () => {
            modalElement.classList.add('hidden');
            modalElement.classList.remove('flex');
            modalElement.setAttribute('aria-hidden', 'true');
            modalElement.removeAttribute('tabindex');
        };

        if (closeButtons) {
            const buttons = NodeList.prototype.isPrototypeOf(closeButtons) || Array.isArray(closeButtons) ? closeButtons : [closeButtons];
            buttons.forEach(btn => addEventListenerIfPresent(btn, 'click', closeHandler));
        }

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
            showToast(error.message, 'error');
            throw error;
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
                datalist.innerHTML = '';
                return;
            }

            timeout = setTimeout(async () => {
                try {
                    const result = await apiRequest('/api/address_suggestions/', 'POST', { query: query });
                    if (result.status === 'success' && result.data && result.data.suggestions) {
                        datalist.innerHTML = '';
                        result.data.suggestions.forEach(suggestion => {
                            const option = document.createElement('option');
                            option.value = suggestion;
                            datalist.appendChild(option);
                        });
                    }
                } catch (error) {
                    console.error('Error fetching address suggestions:', error);
                }
            }, 300);
        });
    }


    // =========================================================================
    // --- PAGE-SPECIFIC LOGIC ---
    // =========================================================================

    // --- Logic for the Index Page (/) ---
    if (window.location.pathname === '/') {
        // Setup each main service modal
        const serviceCards = document.querySelectorAll('.service-card[data-service-target]');
        serviceCards.forEach(card => {
            const targetModalId = card.dataset.serviceTarget;
            const targetModal = document.getElementById(targetModalId);
            if (targetModal) {
                setupGenericModal(card, targetModal, targetModal.querySelectorAll('.close-modal-btn'));
            }
        });

        // Hero Section Rent Checker Form
        addEventListenerIfPresent(DOM.heroRentCheckerForm, 'submit', (e) => {
            e.preventDefault();
            if (DOM.rentCheckerModal) {
                DOM.rentCheckerModal.classList.remove('hidden');
                DOM.rentCheckerModal.classList.add('flex');
                if (DOM.modalPostcode) DOM.modalPostcode.value = DOM.heroModalPostcode.value;
                if (DOM.modalBedrooms) DOM.modalBedrooms.value = DOM.heroModalBedrooms.value;
            }
        });
        setupAddressSuggestions(DOM.heroModalPostcode);

        // Rent Checker Modal Form
        addEventListenerIfPresent(DOM.rentCheckerForm, 'submit', async (e) => {
            e.preventDefault();
            DOM.modalRentResults.classList.add('hidden');
            DOM.modalRentPredictionLoader.classList.remove('hidden');
            
            const formData = new FormData(DOM.rentCheckerForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const result = await apiRequest('/api/predict_rent/', 'POST', data);
                DOM.modalRentPredictionOutput.textContent = result.data.predicted_rent;
                DOM.modalRentPredictionMessage.textContent = result.data.range;
                DOM.amenityImpactOutput.textContent = result.data.amenity_impact;
                DOM.marketTrendOutput.textContent = result.data.market_trend;
                DOM.utilitiesCostOutput.textContent = `£${result.data.cost_breakdown.utilities || 'N/A'}`;
                DOM.councilTaxOutput.textContent = `£${result.data.cost_breakdown.council_tax || 'N/A'}`;
                showToast(result.message, 'success');
            } catch (error) {
                DOM.modalRentPredictionOutput.textContent = 'Error';
                DOM.modalRentPredictionMessage.textContent = error.message || 'Failed to predict rent.';
            } finally {
                DOM.modalRentPredictionLoader.classList.add('hidden');
                DOM.modalRentResults.classList.remove('hidden');
            }
        });
        setupAddressSuggestions(DOM.modalPostcode);

        // Landlord Reviews
        async function fetchRecentReviews() {
            if (!DOM.recentReviewsList) return;
            DOM.recentReviewsList.innerHTML = '<p class="text-center text-gray-500">Loading...</p>';
            try {
                const result = await apiRequest('/api/reviews/');
                DOM.recentReviewsList.innerHTML = '';
                if (result.data.reviews.length > 0) {
                    result.data.reviews.forEach(review => {
                        const item = document.createElement('div');
                        item.className = 'bg-gray-50 p-4 rounded-lg shadow-sm';
                        item.innerHTML = `
                            <p class="font-semibold text-gray-800">${review.landlord_name} - <span class="text-yellow-500">${'★'.repeat(review.rating)}</span></p>
                            <p class="text-sm text-gray-600 mt-1">"${review.comments}"</p>
                            <p class="text-xs text-gray-400 mt-2">By ${review.user__username} on ${new Date(review.reviewed_at).toLocaleDateString()}</p>`;
                        DOM.recentReviewsList.appendChild(item);
                    });
                } else {
                    DOM.recentReviewsList.innerHTML = '<p class="text-center text-gray-500 py-4">No reviews yet.</p>';
                }
            } catch (error) {
                DOM.recentReviewsList.innerHTML = `<p class="text-center text-red-500 py-4">${error.message}</p>`;
            }
        }
        addEventListenerIfPresent(DOM.reviewForm, 'submit', async (e) => {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Submitting...';
            
            const formData = new FormData(DOM.reviewForm);
            const data = Object.fromEntries(formData.entries());
            data.rating = parseInt(data.rating);

            try {
                const result = await apiRequest('/api/submit_review/', 'POST', data);
                showToast(result.message, 'success');
                DOM.reviewForm.reset();
                fetchRecentReviews();
            } catch (error) {
                // Error toast is shown by apiRequest helper
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Submit Review <i class="fas fa-paper-plane ml-2"></i>';
            }
        });
        if (DOM.landlordReviewsModal) {
            const observer = new MutationObserver(() => {
                if (!DOM.landlordReviewsModal.classList.contains('hidden')) {
                    fetchRecentReviews();
                }
            });
            observer.observe(DOM.landlordReviewsModal, { attributes: true, attributeFilter: ['class'] });
        }
        setupAddressSuggestions(DOM.reviewPropertyAddressInput);

        // Complaint Submission
        addEventListenerIfPresent(DOM.complaintForm, 'submit', async (e) => {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Submitting...';
            
            const formData = new FormData(DOM.complaintForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const result = await apiRequest('/api/submit_complaint/', 'POST', data);
                showToast(result.message, 'success');
                DOM.complaintForm.reset();
                if (DOM.refinedTextOutput) DOM.refinedTextOutput.classList.add('hidden');
            } catch (error) {
                 // Error toast is shown by apiRequest helper
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Submit Complaint <i class="fas fa-paper-plane ml-2"></i>';
            }
        });
        addEventListenerIfPresent(DOM.refineComplaintBtn, async () => {
            const originalText = DOM.complaintDescription.value.trim();
            if (originalText.length < 20) {
                showToast('Please write a more detailed description (at least 20 characters).', 'error');
                return;
            }
            DOM.refinedTextOutput.classList.add('hidden');
            DOM.refinedTextLoader.classList.remove('hidden');
            try {
                const result = await apiRequest('/api/refine_text/', 'POST', { text: originalText });
                DOM.refinedTextContent.textContent = result.data.refined_text;
                DOM.refinedTextOutput.classList.remove('hidden');
                showToast('Text refined by AI!', 'success');
            } catch (error) {
                 // Error toast is shown by apiRequest helper
            } finally {
                DOM.refinedTextLoader.classList.add('hidden');
            }
        });
        addEventListenerIfPresent(DOM.useRefinedTextBtn, () => {
            DOM.complaintDescription.value = DOM.refinedTextContent.textContent;
            DOM.refinedTextOutput.classList.add('hidden');
            showToast('Refined text applied!', 'success');
        });
        setupAddressSuggestions(DOM.complaintPropertyAddressInput);

        // Community Forums
        async function fetchRecentForumPosts() {
            if (!DOM.recentForumPostsList) return;
            DOM.recentForumPostsList.innerHTML = '<p class="text-center text-gray-500">Loading...</p>';
            try {
                const result = await apiRequest('/api/forum_posts/');
                DOM.recentForumPostsList.innerHTML = '';
                if (result.data.posts.length > 0) {
                    result.data.posts.forEach(post => {
                        const item = document.createElement('div');
                        item.className = 'bg-gray-50 p-4 rounded-lg shadow-sm';
                        item.innerHTML = `
                            <p class="font-semibold text-gray-800">${post.title} - <span class="text-indigo-600">${post.category}</span></p>
                            <p class="text-sm text-gray-600 mt-1">"${post.content.substring(0, 100)}..."</p>
                            <p class="text-xs text-gray-400 mt-2">By ${post.user__username} on ${new Date(post.created_at).toLocaleDateString()}</p>`;
                        DOM.recentForumPostsList.appendChild(item);
                    });
                } else {
                    DOM.recentForumPostsList.innerHTML = '<p class="text-center text-gray-500 py-4">No posts yet.</p>';
                }
            } catch (error) {
                DOM.recentForumPostsList.innerHTML = `<p class="text-center text-red-500 py-4">${error.message}</p>`;
            }
        }
        setupGenericModal(DOM.createPostBtn, DOM.forumPostModal, DOM.closeForumPostModalBtn, DOM.postTitle);
        addEventListenerIfPresent(DOM.generateForumIdeaBtn, async () => {
            const topic = document.getElementById('post_category').value || 'general tenant advice';
            DOM.forumIdeaOutput.classList.add('hidden');
            DOM.forumIdeaLoader.classList.remove('hidden');
            try {
                const result = await apiRequest('/api/generate_forum_idea/', 'POST', { topic: topic });
                DOM.forumIdeaContent.textContent = result.data.idea_text;
                DOM.forumIdeaOutput.classList.remove('hidden');
                showToast('Forum idea generated!', 'success');
            } catch (error) {
                // Error toast handled by helper
            } finally {
                DOM.forumIdeaLoader.classList.add('hidden');
            }
        });
        addEventListenerIfPresent(DOM.useForumIdeaBtn, () => {
            const ideaText = DOM.forumIdeaContent.textContent || '';
            const lines = ideaText.split('\n').filter(line => line.trim() !== '');
            if (lines.length > 0) {
                DOM.postTitle.value = lines[0].replace(/^(Title:|Question:)\s*/i, '').trim();
                DOM.postContent.value = lines.slice(1).join('\n').trim();
            } else {
                DOM.postContent.value = ideaText;
            }
            DOM.forumIdeaOutput.classList.add('hidden');
            showToast('AI idea applied!', 'success');
        });
        addEventListenerIfPresent(DOM.forumPostForm, 'submit', async (e) => {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Submitting...';
            
            const formData = new FormData(DOM.forumPostForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const result = await apiRequest('/api/submit_forum_post/', 'POST', data);
                showToast(result.message, 'success');
                DOM.forumPostForm.reset();
                DOM.forumIdeaOutput.classList.add('hidden');
                DOM.forumPostModal.classList.add('hidden');
                DOM.forumPostModal.classList.remove('flex');
                fetchRecentForumPosts();
            } catch (error) {
                // Error toast handled by helper
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Submit Post <i class="fas fa-paper-plane ml-2"></i>';
            }
        });
        if (DOM.communityForumsModal) {
             const observer = new MutationObserver(() => {
                if (!DOM.communityForumsModal.classList.contains('hidden')) {
                    fetchRecentForumPosts();
                }
            });
            observer.observe(DOM.communityForumsModal, { attributes: true, attributeFilter: ['class'] });
        }
        
        // Legal AI
        setupGenericModal(DOM.askLegalAiBtn, DOM.legalAiModal, DOM.closeLegalAiModalBtn, DOM.legalQueryInput);
        addEventListenerIfPresent(DOM.submitLegalQueryBtn, async () => {
            const query = DOM.legalQueryInput.value.trim();
            if (query.length < 10) {
                showToast('Please enter a more detailed question.', 'error');
                return;
            }
            DOM.legalAiOutput.classList.add('hidden');
            DOM.legalAiLoader.classList.remove('hidden');
            try {
                const result = await apiRequest('/api/refine_text/', 'POST', { text: `Provide general information on UK rental law for this query: "${query}". Keep it concise and state it's not legal advice.` });
                DOM.legalAiContent.textContent = result.data.refined_text;
                DOM.legalAiOutput.classList.remove('hidden');
                showToast('AI answer generated!', 'success');
            } catch (error) {
                // Error toast handled by helper
            } finally {
                DOM.legalAiLoader.classList.add('hidden');
            }
        });

        // Rental Contract Analyzer
        addEventListenerIfPresent(DOM.rentalContractForm, 'submit', async (e) => {
            e.preventDefault();
            const contractText = DOM.contractTextarea.value.trim();
            if (contractText.length < 100) {
                showToast('Please provide more text for a meaningful analysis (min 100 characters).', 'error');
                return;
            }
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Analyzing...';
            DOM.contractAnalysisOutput.classList.add('hidden');
            DOM.contractAnalysisLoader.classList.remove('hidden');
            
            try {
                const result = await apiRequest('/api/analyze_contract/', 'POST', { contract_text: contractText });
                DOM.analysisContent.innerHTML = result.data.analysis_result.replace(/\n/g, '<br>');
                showToast(result.message, 'success');
            } catch (error) {
                DOM.analysisContent.innerHTML = `<p class="text-red-500">${error.message}</p>`;
            } finally {
                DOM.contractAnalysisLoader.classList.add('hidden');
                DOM.contractAnalysisOutput.classList.remove('hidden');
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Analyze Contract <i class="fas fa-robot ml-2"></i>';
            }
        });
    }


    // --- Logic for the Profile Page (/profile) ---
    if (window.location.pathname.includes('/profile')) {
        // --- Sidebar Navigation Logic ---
        function closeSidebar() {
            if (!DOM.sidebar || !DOM.sidebarOverlay) return;
            DOM.sidebar.classList.add('hidden-mobile');
            DOM.sidebar.classList.remove('open-mobile');
            DOM.sidebarOverlay.classList.add('hidden');
            DOM.sidebarToggle.setAttribute('aria-expanded', 'false');
        }

        function handleResize() {
            if (window.innerWidth > 900) {
                DOM.sidebar.classList.remove('hidden-mobile', 'open-mobile');
                DOM.sidebarOverlay.classList.add('hidden');
                DOM.sidebarToggle.setAttribute('aria-expanded', 'true');
                DOM.mainContent.style.marginLeft = '280px';
            } else {
                DOM.sidebar.classList.add('hidden-mobile');
                DOM.sidebar.classList.remove('open-mobile');
                DOM.sidebarOverlay.classList.add('hidden');
                DOM.sidebarToggle.setAttribute('aria-expanded', 'false');
                DOM.mainContent.style.marginLeft = '0';
            }
        }
        
        addEventListenerIfPresent(DOM.sidebarToggle, 'click', () => {
            DOM.sidebar.classList.remove('hidden-mobile');
            DOM.sidebar.classList.add('open-mobile');
            DOM.sidebarOverlay.classList.remove('hidden');
            DOM.sidebarToggle.setAttribute('aria-expanded', 'true');
            DOM.sidebar.focus();
        });

        addEventListenerIfPresent(DOM.sidebarOverlay, 'click', closeSidebar);
        addEventListenerIfPresent(DOM.sidebar, 'keydown', e => {
            if (e.key === "Escape") closeSidebar();
        });

        window.addEventListener('resize', handleResize);
        handleResize(); // Initial call on load

        const switchTab = (targetId) => {
            if (!targetId) return;
            
            DOM.sidebarNavItems.forEach(nav => nav.classList.remove('active'));
            const newActiveNavItem = document.querySelector(`.sidebar-nav-item[data-content-target="${targetId}"]`);
            if(newActiveNavItem) newActiveNavItem.classList.add('active');

            DOM.contentSections.forEach(section => section.classList.add('hidden'));
            const targetSection = document.getElementById(targetId);
            if (targetSection) targetSection.classList.remove('hidden');

            if (window.innerWidth <= 900) closeSidebar();
        };

        DOM.sidebarNavItems.forEach(item => {
            addEventListenerIfPresent(item, 'click', (e) => {
                e.preventDefault();
                switchTab(item.dataset.contentTarget);
            });
        });

        addEventListenerIfPresent(DOM.myServicesHeaderBtn, 'click', (e) => {
            e.preventDefault();
            switchTab(DOM.myServicesHeaderBtn.dataset.contentTarget);
        });

        // Initialize active section on load
        const initialSectionId = window.location.hash ? window.location.hash.substring(1) : 'dashboard-home';
        switchTab(initialSectionId);


        // --- Roommate Profile Edit Modal Logic ---
        const ALL_LIFESTYLE_PREFERENCES = [
            'Quiet', 'Social', 'Pet-Friendly', 'Clean', 'Messy', 'Early Bird',
            'Night Owl', 'Studious', 'Party-goer', 'Vegetarian', 'Vegan',
            'Cooks Often', 'Rarely Cooks', 'Non-Smoker', 'Smoker', 'Introvert', 'Extrovert'
        ];

        function renderLifestylePreferenceTags(selectedPreferences = []) {
            if (!DOM.lifestylePreferencesTagsContainer) return;
            DOM.lifestylePreferencesTagsContainer.innerHTML = '';
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

        function updateLifestylePreferencesHiddenInput() {
            if (!DOM.lifestylePreferencesTagsContainer || !DOM.lifestylePreferencesHiddenInput) return;
            const selectedTags = Array.from(DOM.lifestylePreferencesTagsContainer.querySelectorAll('.tag.selected')).map(tag => tag.textContent);
            DOM.lifestylePreferencesHiddenInput.value = selectedTags.join(', ');
        }

        const openProfileModal = () => {
            const currentPrefsString = DOM.lifestylePreferencesHiddenInput ? DOM.lifestylePreferencesHiddenInput.value : '';
            const currentPrefsArray = currentPrefsString.split(',').map(item => item.trim()).filter(Boolean);
            renderLifestylePreferenceTags(currentPrefsArray);
        };

        setupGenericModal([DOM.editProfileBtnDashboardHome, DOM.editProfileBtnRoommateSection], DOM.profileModal, [DOM.closeProfileModalBtn, DOM.profileFormCancelBtn]);
        addEventListenerIfPresent(DOM.editProfileBtnDashboardHome, 'click', openProfileModal);
        addEventListenerIfPresent(DOM.editProfileBtnRoommateSection, 'click', openProfileModal);
        
        addEventListenerIfPresent(DOM.roommateProfileForm, 'submit', async (e) => {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Saving...';
            
            const formData = new FormData(DOM.roommateProfileForm);
            const data = Object.fromEntries(formData.entries());
            data.age = data.age ? parseInt(data.age) : null;
            data.budget = data.budget ? parseInt(data.budget) : null;

            try {
                await apiRequest('/api/save_roommate_profile/', 'POST', data);
                showToast('Profile saved successfully!', 'success');
                setTimeout(() => location.reload(), 1500);
            } catch (error) {
                // Error toast handled by helper
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Save Profile';
            }
        });
        setupAddressSuggestions(DOM.profileLocationInput);


        // --- Roommate Match Finder Logic (Swipe UI) ---
        let currentMatches = [];
        let currentMatchIndex = 0;

        function displayCurrentMatch() {
            if (!DOM.roommateMatchCardDisplay || !DOM.roommatePrompt || !DOM.noMoreMatchesPrompt || !DOM.swipeButtonsContainer) return;

            DOM.roommateMatchCardDisplay.innerHTML = '';
            DOM.roommatePrompt.classList.add('hidden');
            DOM.noMoreMatchesPrompt.classList.add('hidden');

            if (currentMatchIndex < currentMatches.length) {
                const match = currentMatches[currentMatchIndex];
                const matchCard = document.createElement('div');
                matchCard.className = 'roommate-match-card glass-card';
                matchCard.innerHTML = `
                    <img src="${match.avatar_url || 'https://placehold.co/110x110/cccccc/ffffff?text=User'}" alt="${match.name || 'User'}" class="mx-auto mb-4 w-28 h-28 rounded-full object-cover border-4 border-blue-400" onerror="this.onerror=null;this.src='https://placehold.co/110x110/cccccc/ffffff?text=User'">
                    <h4 class="text-3xl font-bold text-gray-900">${match.name || 'Unknown'}, ${match.age || 'N/A'}</h4>
                    <p class="text-lg text-gray-600 mb-2">${match.location || 'N/A'}</p>
                    <div class="compatibility-score">${match.compatibility_score || 'N/A'}% Match</div>
                    <p class="text-gray-700 text-base italic leading-relaxed mt-2">${match.bio || 'No bio provided.'}</p>
                    <button class="match-details-btn btn-secondary mt-4 btn-hover-effect" data-match='${JSON.stringify(match)}'>View Details</button>`;
                DOM.roommateMatchCardDisplay.appendChild(matchCard);
                DOM.swipeButtonsContainer.classList.remove('hidden');

                addEventListenerIfPresent(matchCard.querySelector('.match-details-btn'), 'click', () => {
                    displayActivityDetails('Liked Profile', match);
                });
            } else {
                DOM.swipeButtonsContainer.classList.add('hidden');
                DOM.noMoreMatchesPrompt.classList.remove('hidden');
            }
        }

        async function fetchRoommateMatches() {
            DOM.roommatePrompt.classList.add('hidden');
            DOM.noMoreMatchesPrompt.classList.add('hidden');
            DOM.roommateMatchesLoader.classList.remove('hidden');
            DOM.roommateMatchCardDisplay.innerHTML = '';
            DOM.swipeButtonsContainer.classList.add('hidden');

            try {
                const result = await apiRequest('/api/find_roommate_matches/', 'POST', {});
                currentMatches = result.data.matches;
                currentMatchIndex = 0;
                displayCurrentMatch();
            } catch (error) {
                DOM.roommatePrompt.classList.remove('hidden');
            } finally {
                DOM.roommateMatchesLoader.classList.add('hidden');
            }
        }

        async function animateAndAdvance(direction) {
            const currentCard = DOM.roommateMatchCardDisplay.querySelector('.roommate-match-card');
            if (currentCard) {
                if (direction === 'like') {
                    const likedMatchData = currentMatches[currentMatchIndex];
                    const dataToSend = {
                        name: likedMatchData.name || '',
                        age: likedMatchData.age ? parseInt(likedMatchData.age) : null,
                        gender: likedMatchData.gender || '',
                        location: likedMatchData.location || '',
                        budget: likedMatchData.budget ? parseInt(likedMatchData.budget) : null,
                        bio: likedMatchData.bio || '',
                        compatibility_score: likedMatchData.compatibility_score ? parseInt(likedMatchData.compatibility_score) : null,
                        avatar_url: likedMatchData.avatar_url || ''
                    };
                    try {
                        await apiRequest('/api/save_liked_profile/', 'POST', dataToSend);
                        showToast('Profile liked!', 'success');
                    } catch (error) {
                        // Error toast handled by helper, just proceed with animation
                    }
                }
                
                currentCard.classList.add(direction === 'like' ? 'swiping-right' : 'swiping-left');
                currentCard.addEventListener('transitionend', () => {
                    currentMatchIndex++;
                    displayCurrentMatch();
                }, { once: true });
            }
        }

        addEventListenerIfPresent(DOM.findMatchesBtn, fetchRoommateMatches);
        addEventListenerIfPresent(DOM.resetMatchesBtn, fetchRoommateMatches);
        addEventListenerIfPresent(DOM.skipMatchBtn, () => animateAndAdvance('skip'));
        addEventListenerIfPresent(DOM.likeMatchBtn, () => animateAndAdvance('like'));


        // --- Generic Activity/Service Details Modal Logic ---
        setupGenericModal(null, DOM.activityDetailsModal, DOM.closeActivityModalBtn);

        function displayActivityDetails(activityType, details) {
            if (!DOM.activityModalContent || !DOM.activityDetailsModal) return;

            DOM.activityModalContent.innerHTML = '';
            let contentHtml = `<h3 class="text-2xl font-bold text-gray-900 mb-4">${activityType} Details</h3>`;
            const formatDate = (d) => d ? new Date(d).toLocaleString() : 'N/A';
            const formatCurrency = (v) => v ? `£${parseFloat(v).toLocaleString()}` : 'N/A';

            switch (activityType) {
                case 'Liked Profile':
                    contentHtml += `
                        <img src="${details.avatar_url || 'https://placehold.co/112x112/cccccc/ffffff?text=User'}" alt="${details.name}" class="mx-auto mb-4 w-28 h-28 rounded-full object-cover border-4 border-blue-400">
                        <h4 class="text-xl font-bold text-gray-900 mb-2">${details.name}, ${details.age || 'N/A'}</h4>
                        <p class="text-md text-gray-700 mb-4">${details.gender || 'N/A'} | ${details.location || 'N/A'}</p>
                        <div class="text-left space-y-3">
                            <div class="detail-item"><i class="fas fa-money-bill-wave"></i><span>Budget:</span> ${formatCurrency(details.budget)} / month</div>
                            <div class="detail-item"><i class="fas fa-user-friends"></i><span>Compatibility:</span> <span class="compatibility-score-modal">${details.compatibility_score || 'N/A'}%</span></div>
                            <div class="detail-item"><i class="fas fa-info-circle"></i><span>Bio:</span> <p class="whitespace-pre-wrap">${details.bio || 'No bio.'}</p></div>
                        </div>`;
                    break;
                case 'Rent Check':
                     contentHtml += `
                        <div class="text-left space-y-3">
                            <div class="detail-item"><i class="fas fa-map-marker-alt"></i><span>Postcode:</span> ${details.postcode}</div>
                            <div class="detail-item"><i class="fas fa-bed"></i><span>Bedrooms:</span> ${details.bedrooms}</div>
                            <div class="detail-item"><i class="fas fa-gbp-sign"></i><span>Estimated Rent:</span> ${formatCurrency(details.estimated_rent)} / month</div>
                            <div class="detail-item"><i class="fas fa-calendar-alt"></i><span>Checked At:</span> ${formatDate(details.checked_at)}</div>
                        </div>`;
                    break;
                case 'Review':
                    contentHtml += `
                        <div class="text-left space-y-3">
                            <div class="detail-item"><i class="fas fa-user-tie"></i><span>Landlord:</span> ${details.landlord_name}</div>
                            <div class="detail-item"><i class="fas fa-map-marker-alt"></i><span>Property:</span> ${details.property_address}</div>
                            <div class="detail-item"><i class="fas fa-star"></i><span>Rating:</span> ${details.rating} Stars</div>
                            <div class="detail-item"><i class="fas fa-comment-alt"></i><span>Comments:</span> <p class="whitespace-pre-wrap">${details.comments}</p></div>
                            <div class="detail-item"><i class="fas fa-calendar-alt"></i><span>Reviewed At:</span> ${formatDate(details.reviewed_at)}</div>
                        </div>`;
                    break;
                case 'Complaint':
                     contentHtml += `
                        <div class="text-left space-y-3">
                            <div class="detail-item"><i class="fas fa-exclamation-triangle"></i><span>Issue:</span> ${details.issue_type}</div>
                            <div class="detail-item"><i class="fas fa-map-marker-alt"></i><span>Property:</span> ${details.property_address}</div>
                            <div class="detail-item"><i class="fas fa-file-alt"></i><span>Description:</span> <p class="whitespace-pre-wrap">${details.description}</p></div>
                            <div class="detail-item"><i class="fas fa-info-circle"></i><span>Status:</span> ${details.status}</div>
                            <div class="detail-item"><i class="fas fa-calendar-alt"></i><span>Submitted At:</span> ${formatDate(details.submitted_at)}</div>
                        </div>`;
                    break;
                case 'Forum Post':
                     contentHtml += `
                        <div class="text-left space-y-3">
                            <div class="detail-item"><i class="fas fa-heading"></i><span>Title:</span> ${details.title}</div>
                            <div class="detail-item"><i class="fas fa-tags"></i><span>Category:</span> ${details.category}</div>
                            <div class="detail-item"><i class="fas fa-file-alt"></i><span>Content:</span> <p class="whitespace-pre-wrap">${details.content}</p></div>
                            <div class="detail-item"><i class="fas fa-calendar-alt"></i><span>Posted At:</span> ${formatDate(details.created_at)}</div>
                        </div>`;
                    break;
                case 'Contract Analysis':
                    contentHtml += `
                        <div class="text-left space-y-3">
                            <div class="detail-item"><i class="fas fa-calendar-alt"></i><span>Analyzed At:</span> ${formatDate(details.analyzed_at)}</div>
                            <div class="detail-item"><i class="fas fa-file-alt"></i><span>Original Text:</span> <p class="whitespace-pre-wrap text-sm max-h-40 overflow-y-auto border p-2 rounded">${details.original_text}</p></div>
                            <div class="detail-item"><i class="fas fa-robot"></i><span>AI Analysis:</span> <p class="whitespace-pre-wrap text-sm max-h-60 overflow-y-auto border p-2 rounded">${details.analysis_result}</p></div>
                        </div>`;
                    break;
                default:
                    contentHtml += `<p class="text-center text-gray-500">Details not available.</p>`;
            }

            DOM.activityModalContent.innerHTML = contentHtml;
            DOM.activityDetailsModal.classList.remove('hidden');
            DOM.activityDetailsModal.classList.add('flex');
        }

        // Event listener for clicking on Activity/Service items (MERGED LOGIC)
        document.addEventListener('click', (event) => {
            const activityItem = event.target.closest('.activity-item[data-activity-type]');
            const serviceResultCard = event.target.closest('.service-result-card[data-activity-type]');
            const item = activityItem || serviceResultCard;

            if (item) {
                const activityType = item.dataset.activityType;
                let details;
                try {
                    // Try parsing from data attribute first (for service cards)
                    if (item.dataset.activityDetails) {
                        details = JSON.parse(item.dataset.activityDetails);
                    } else {
                        // Fallback to script tag method (for activity feed)
                        const scriptId = item.dataset.activityDetailsId;
                        const scriptTag = document.getElementById(scriptId);
                        if (scriptTag) {
                            details = JSON.parse(scriptTag.textContent);
                        } else {
                            throw new Error(`Details script tag not found for ID: ${scriptId}`);
                        }
                    }
                    displayActivityDetails(activityType, details);
                } catch (e) {
                    console.error('Error loading activity details:', e);
                    showToast('Error loading details.', 'error');
                }
            }
        });

        // Tab switching logic for My Services section
        DOM.mainContentTabButtons.forEach(button => {
            addEventListenerIfPresent(button, 'click', () => {
                const targetTabId = button.dataset.tabId;
                DOM.mainContentTabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                DOM.mainContentTabContents.forEach(content => {
                    content.classList.toggle('hidden', content.id !== targetTabId);
                });
            });
        });
    }
});
