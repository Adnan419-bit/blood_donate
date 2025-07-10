// BloodConnect JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeAnimations();
    initializeFormValidation();
    initializeSearchFilters();
    initializeEmergencyFeatures();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
});

// Animation on scroll
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards and feature elements
    const animatedElements = document.querySelectorAll('.feature-card, .blood-type-card, .donor-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Show custom error messages
                const invalidInputs = form.querySelectorAll(':invalid');
                invalidInputs.forEach(input => {
                    showFieldError(input);
                });
            } else {
                // Show loading state
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                    submitBtn.disabled = true;
                    
                    // Re-enable after 3 seconds (in case of error)
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }, 3000);
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(input);
            });
        });
    });
}

function validateField(field) {
    if (!field.checkValidity()) {
        showFieldError(field);
    } else {
        clearFieldError(field);
    }
}

function showFieldError(field) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = getErrorMessage(field);
    
    field.parentNode.appendChild(errorDiv);
    field.classList.add('is-invalid');
}

function clearFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
    field.classList.remove('is-invalid');
}

function getErrorMessage(field) {
    if (field.validity.valueMissing) {
        return `${field.getAttribute('placeholder') || 'This field'} is required.`;
    }
    if (field.validity.typeMismatch) {
        return 'Please enter a valid format.';
    }
    if (field.validity.patternMismatch) {
        return 'Please match the requested format.';
    }
    if (field.validity.tooShort) {
        return `Minimum ${field.minLength} characters required.`;
    }
    if (field.validity.rangeUnderflow) {
        return `Minimum value is ${field.min}.`;
    }
    if (field.validity.rangeOverflow) {
        return `Maximum value is ${field.max}.`;
    }
    return 'Please enter a valid value.';
}

// Search filters
function initializeSearchFilters() {
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        const bloodTypeSelect = searchForm.querySelector('select[name="blood_type"]');
        const cityInput = searchForm.querySelector('input[name="city"]');
        
        if (bloodTypeSelect) {
            bloodTypeSelect.addEventListener('change', function() {
                updateCompatibilityInfo(this.value);
            });
        }
        
        if (cityInput) {
            // Auto-complete for cities (basic implementation)
            const cities = ['Dhaka', 'Chittagong', 'Sylhet', 'Rajshahi', 'Khulna', 'Barisal', 'Rangpur', 'Mymensingh'];
            
            cityInput.addEventListener('input', function() {
                const value = this.value.toLowerCase();
                const suggestions = cities.filter(city => 
                    city.toLowerCase().includes(value)
                );
                
                showCitySuggestions(this, suggestions);
            });
        }
    }
}

function updateCompatibilityInfo(bloodType) {
    const compatibility = {
        'A+': ['A+', 'A-', 'O+', 'O-'],
        'A-': ['A-', 'O-'],
        'B+': ['B+', 'B-', 'O+', 'O-'],
        'B-': ['B-', 'O-'],
        'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'AB-': ['A-', 'B-', 'AB-', 'O-'],
        'O+': ['O+', 'O-'],
        'O-': ['O-']
    };
    
    const compatibleTypes = compatibility[bloodType];
    if (compatibleTypes) {
        showCompatibilityTooltip(bloodType, compatibleTypes);
    }
}

function showCompatibilityTooltip(bloodType, compatibleTypes) {
    const tooltip = document.createElement('div');
    tooltip.className = 'alert alert-info mt-2';
    tooltip.innerHTML = `
        <strong>${bloodType}</strong> recipients can receive blood from: 
        <span class="fw-bold text-danger">${compatibleTypes.join(', ')}</span>
    `;
    
    const existingTooltip = document.querySelector('.compatibility-tooltip');
    if (existingTooltip) {
        existingTooltip.remove();
    }
    
    tooltip.classList.add('compatibility-tooltip');
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.appendChild(tooltip);
    }
}

function showCitySuggestions(input, suggestions) {
    // Remove existing suggestions
    const existingSuggestions = document.querySelector('.city-suggestions');
    if (existingSuggestions) {
        existingSuggestions.remove();
    }
    
    if (suggestions.length === 0 || input.value.length < 2) {
        return;
    }
    
    const suggestionDiv = document.createElement('div');
    suggestionDiv.className = 'city-suggestions list-group position-absolute w-100';
    suggestionDiv.style.zIndex = '1000';
    
    suggestions.forEach(city => {
        const item = document.createElement('button');
        item.className = 'list-group-item list-group-item-action';
        item.textContent = city;
        item.type = 'button';
        
        item.addEventListener('click', function() {
            input.value = city;
            suggestionDiv.remove();
        });
        
        suggestionDiv.appendChild(item);
    });
    
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(suggestionDiv);
}

// Emergency features
function initializeEmergencyFeatures() {
    const emergencyBtn = document.querySelector('.emergency-btn');
    if (emergencyBtn) {
        emergencyBtn.addEventListener('click', function() {
            if (confirm('This will create an emergency blood request. Continue?')) {
                // Add urgency indicator
                this.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>EMERGENCY REQUEST';
                this.classList.add('btn-danger');
                this.classList.remove('btn-warning');
            }
        });
    }
    
    // Emergency contact buttons
    const emergencyContacts = document.querySelectorAll('.emergency-contact');
    emergencyContacts.forEach(contact => {
        contact.addEventListener('click', function() {
            const phone = this.dataset.phone;
            if (phone) {
                window.location.href = `tel:${phone}`;
            }
        });
    });
}

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }).catch(function() {
        showNotification('Failed to copy to clipboard', 'danger');
    });
}

// Blood type compatibility checker
function checkCompatibility(donorType, recipientType) {
    const compatibility = {
        'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'A-': ['A-', 'A+', 'AB-', 'AB+'],
        'A+': ['A+', 'AB+'],
        'B-': ['B-', 'B+', 'AB-', 'AB+'],
        'B+': ['B+', 'AB+'],
        'AB-': ['AB-', 'AB+'],
        'AB+': ['AB+']
    };
    
    return compatibility[donorType]?.includes(recipientType) || false;
}

// Geolocation for finding nearby donors
function findNearbyDonors() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            // In a real app, you would send this to your backend
            console.log(`User location: ${lat}, ${lon}`);
            showNotification('Location detected! Searching for nearby donors...', 'info');
            
            // Simulate search delay
            setTimeout(() => {
                showNotification('Found 5 donors within 10km radius!', 'success');
            }, 2000);
        }, function(error) {
            showNotification('Location access denied. Please enter your city manually.', 'warning');
        });
    } else {
        showNotification('Geolocation is not supported by this browser.', 'warning');
    }
}

// Share functionality
function shareBloodRequest(requestId) {
    if (navigator.share) {
        navigator.share({
            title: 'Urgent Blood Needed',
            text: 'Help save a life by donating blood!',
            url: window.location.href
        }).then(() => {
            showNotification('Shared successfully!', 'success');
        }).catch(() => {
            showNotification('Sharing failed', 'danger');
        });
    } else {
        // Fallback to copying URL
        copyToClipboard(window.location.href);
    }
}

// Dark mode toggle (bonus feature)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    
    const icon = document.querySelector('.dark-mode-toggle i');
    if (icon) {
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Print functionality for donor cards
function printDonorCard(donorId) {
    const donorCard = document.querySelector(`[data-donor-id="${donorId}"]`);
    if (donorCard) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>Donor Information</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; }
                        .donor-card { border: 1px solid #ddd; padding: 20px; border-radius: 10px; }
                    </style>
                </head>
                <body>
                    ${donorCard.outerHTML}
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}
