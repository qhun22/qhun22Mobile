/**
 * ===== TOAST NOTIFICATION SYSTEM - PREMIUM DESIGN =====
 * Premium toast notifications with smooth animations and modern UI
 */

const ToastType = {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info'
};

// SVG Icons for each toast type
const ToastIcons = {
    success: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
    </svg>`,
    error: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="15" y1="9" x2="9" y2="15"></line>
        <line x1="9" y1="9" x2="15" y2="15"></line>
    </svg>`,
    warning: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
    </svg>`,
    info: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
    </svg>`
};

// Toast display durations (milliseconds)
const ToastDurations = {
    success: 3500,
    error: 4500,
    warning: 4000,
    info: 3500
};

// Track active toasts
let activeToasts = new Map();

/**
 * Create and show a toast notification
 * @param {string} type - Toast type (success, error, warning, info)
 * @param {string} title - Toast title
 * @param {string} message - Toast message
 */
function showToast(type, title, message) {
    const container = document.getElementById('toast-container');
    if (!container) {
        console.error('Toast container not found');
        return;
    }

    const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const iconSvg = ToastIcons[type] || ToastIcons.info;
    const duration = ToastDurations[type] || 3500;

    // Create toast element
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');

    toast.innerHTML = `
        <div class="toast-icon-wrapper">
            ${iconSvg}
        </div>
        <div class="toast-body">
            <div class="toast-title">${escapeHtml(title)}</div>
            <div class="toast-message">${escapeHtml(message)}</div>
        </div>
        <button class="toast-close" onclick="closeToast('${toastId}')" aria-label="Close">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
        <div class="toast-progress">
            <div class="toast-progress-bar" style="animation-duration: ${duration}ms;"></div>
        </div>
    `;

    container.appendChild(toast);

    // Store timeout ID for cleanup
    const timeoutId = setTimeout(() => {
        closeToast(toastId);
    }, duration);

    activeToasts.set(toastId, { element: toast, timeoutId });

    // Remove from active toasts when closed
    toast.addEventListener('removed', () => {
        activeToasts.delete(toastId);
    });
}

/**
 * Close a specific toast with animation
 * @param {string} toastId - The ID of the toast to close
 */
function closeToast(toastId) {
    const toastData = activeToasts.get(toastId);
    if (!toastData) return;

    const toast = toastData.element;
    const timeoutId = toastData.timeoutId;

    // Clear the timeout
    clearTimeout(timeoutId);

    // Add exit animation
    toast.classList.add('toast-exit');

    // Remove after animation completes
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
        toast.dispatchEvent(new Event('removed'));
    }, 300);
}

/**
 * Close all active toasts
 */
function closeAllToasts() {
    activeToasts.forEach((toastData, toastId) => {
        closeToast(toastId);
    });
}

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== CONVENIENCE FUNCTIONS =====

/**
 * Show success toast
 */
function showSuccess(title, message) {
    showToast(ToastType.SUCCESS, title, message);
}

/**
 * Show error toast
 */
function showError(title, message) {
    showToast(ToastType.ERROR, title, message);
}

/**
 * Show warning toast
 */
function showWarning(title, message) {
    showToast(ToastType.WARNING, title, message);
}

/**
 * Show info toast
 */
function showInfo(title, message) {
    showToast(ToastType.INFO, title, message);
}

// ===== EXPOSE TO GLOBAL SCOPE =====

window.showToast = showToast;
window.closeToast = closeToast;
window.closeAllToasts = closeAllToasts;
window.showSuccess = showSuccess;
window.showError = showError;
window.showWarning = showWarning;
window.showInfo = showInfo;

// Console log for debugging
console.log('✅ Toast notification system loaded successfully');
