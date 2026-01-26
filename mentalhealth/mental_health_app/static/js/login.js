// Eco Wellness Login Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const passwordToggle = document.getElementById('passwordToggle');
    const passwordInput = document.getElementById('password');
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');
    const harmonyButton = document.querySelector('.harmony-button');
    const successMessage = document.getElementById('successMessage');

    // Password toggle functionality
    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener('click', function() {
            const isVisible = passwordInput.type === 'text';
            passwordInput.type = isVisible ? 'password' : 'text';
            passwordToggle.classList.toggle('toggle-visible');
        });
    }

    // Form validation
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function validatePassword(password) {
        return password.length >= 6; // Basic validation
    }

    function showError(input, errorElement, message) {
        input.closest('.organic-field').classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }

    function hideError(input, errorElement) {
        input.closest('.organic-field').classList.remove('error');
        errorElement.classList.remove('show');
    }

    // Email validation
    if (emailInput && emailError) {
        emailInput.addEventListener('blur', function() {
            if (!validateEmail(emailInput.value)) {
                showError(emailInput, emailError, 'Please enter a valid email address');
            } else {
                hideError(emailInput, emailError);
            }
        });

        emailInput.addEventListener('input', function() {
            if (validateEmail(emailInput.value)) {
                hideError(emailInput, emailError);
            }
        });
    }

    // Password validation
    if (passwordInput && passwordError) {
        passwordInput.addEventListener('blur', function() {
            if (!validatePassword(passwordInput.value)) {
                showError(passwordInput, passwordError, 'Password must be at least 6 characters');
            } else {
                hideError(passwordInput, passwordError);
            }
        });

        passwordInput.addEventListener('input', function() {
            if (validatePassword(passwordInput.value)) {
                hideError(passwordInput, passwordError);
            }
        });
    }

    // Form submission
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            let isValid = true;

            // Validate email
            if (!validateEmail(emailInput.value)) {
                showError(emailInput, emailError, 'Please enter a valid email address');
                isValid = false;
            }

            // Validate password
            if (!validatePassword(passwordInput.value)) {
                showError(passwordInput, passwordError, 'Password must be at least 6 characters');
                isValid = false;
            }

            if (isValid) {
                // Show loading state
                harmonyButton.classList.add('loading');

                // Simulate form submission (replace with actual submission)
                setTimeout(function() {
                    harmonyButton.classList.remove('loading');
                    successMessage.classList.add('show');
                    loginForm.style.display = 'none';
                }, 2000);
            }
        });
    }

    // Social login placeholders
    const socialButtons = document.querySelectorAll('.earth-social');
    socialButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Social login functionality would be implemented here');
        });
    });

    // Checkbox animation
    const checkbox = document.getElementById('remember');
    if (checkbox) {
        checkbox.addEventListener('change', function() {
            // Additional logic for remember me can be added here
        });
    }
});
