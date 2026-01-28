// ===== AUTHENTICATION JAVASCRIPT =====
// Login, Register, Forgot Password logic
// IMPORTANT: Only show ONE toast per action

(function() {
    'use strict';

    // Flag to track if toast has been shown for this page load
    let toastAlreadyShown = false;

    // ===== TOAST HANDLER (Single toast per action) =====
    function showToastOnce(type, title, message) {
        if (toastAlreadyShown) return;
        clearAllToasts();
        showToast(type, title, message);
        toastAlreadyShown = true;
    }

    // ===== LOGIN FORM =====
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('id_username').value.trim();
            const password = document.getElementById('id_password').value.trim();

            if (!username || !password) {
                e.preventDefault();
                showToastOnce('error', 'Lỗi', 'Vui lòng nhập đầy đủ thông tin đăng nhập');
                return;
            }

            // Form is valid, submit normally
        });
    }

    // ===== REGISTER FORM =====
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const username = document.getElementById('id_username').value.trim();
            const firstName = document.getElementById('id_first_name').value.trim();
            const email = document.getElementById('id_email').value.trim();
            const password1 = document.getElementById('id_password1').value;
            const password2 = document.getElementById('id_password2').value;

            // Client-side validation
            if (!username || !firstName || !email || !password1 || !password2) {
                e.preventDefault();
                showToastOnce('error', 'Lỗi', 'Vui lòng điền đầy đủ thông tin');
                return;
            }

            if (password1 !== password2) {
                e.preventDefault();
                showToastOnce('error', 'Lỗi', 'Mật khẩu không khớp');
                return;
            }

            if (password1.length < 8) {
                e.preventDefault();
                showToastOnce('error', 'Lỗi', 'Mật khẩu phải có ít nhất 8 ký tự');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showToastOnce('error', 'Lỗi', 'Email không hợp lệ');
                return;
            }

            // Form is valid, submit normally
        });
    }

    // ===== FORGOT PASSWORD FORM =====
    const forgotForm = document.getElementById('forgotForm');
    if (forgotForm) {
        forgotForm.addEventListener('submit', function(e) {
            const email = document.getElementById('id_email').value.trim();

            if (!email) {
                e.preventDefault();
                showToastOnce('error', 'Lỗi', 'Vui lòng nhập email');
                return;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showToastOnce('error', 'Lỗi', 'Email không hợp lệ');
                return;
            }

            // Show loading state
            const submitBtn = forgotForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang xử lý...';
            }

            // Form is valid, submit normally
        });
    }

})();

console.log('Auth JavaScript loaded');
