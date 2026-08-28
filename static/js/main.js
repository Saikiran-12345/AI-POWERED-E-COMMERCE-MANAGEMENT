/* ============================================================
   ShopAI SaaS — Main JavaScript
   ============================================================ */

'use strict';

// ─── Utilities ──────────────────────────────────────────────────────────────

/**
 * Format a number as Indian currency.
 */
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

/**
 * Show a toast notification.
 */
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container') || createToastContainer();
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto"
                    data-bs-dismiss="toast"></button>
        </div>
    `;
    container.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

/**
 * Debounce utility for search inputs.
 */
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// ─── Product Search Autocomplete ────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) {
        const dropdown = createSearchDropdown(searchInput);

        searchInput.addEventListener('input', debounce(async function() {
            const query = this.value.trim();
            if (query.length < 2) {
                dropdown.style.display = 'none';
                return;
            }
            try {
                const response = await fetch(`/products/search/?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                renderSearchResults(dropdown, data.results);
            } catch (err) {
                console.error('Search error:', err);
            }
        }, 300));

        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    }
});

function createSearchDropdown(input) {
    const wrapper = input.closest('.input-group') || input.parentElement;
    wrapper.style.position = 'relative';
    const dropdown = document.createElement('div');
    dropdown.className = 'search-dropdown';
    dropdown.style.cssText = `
        position: absolute; top: 100%; left: 0; right: 0;
        background: white; border: 1px solid #e2e8f0; border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        z-index: 1000; display: none; max-height: 400px; overflow-y: auto;
    `;
    wrapper.appendChild(dropdown);
    return dropdown;
}

function renderSearchResults(dropdown, results) {
    if (!results || results.length === 0) {
        dropdown.style.display = 'none';
        return;
    }
    dropdown.innerHTML = results.map(p => `
        <a href="${p.url}" class="d-flex align-items-center p-3 text-decoration-none text-dark border-bottom hover-bg">
            <div>
                <div class="fw-semibold">${p.name}</div>
                <small class="text-muted">${p.brand || ''} — ${formatCurrency(p.price)}</small>
            </div>
        </a>
    `).join('');
    dropdown.style.display = 'block';
}

// ─── Cart Interactions ──────────────────────────────────────────────────────

/**
 * Quick add-to-cart with AJAX feedback.
 */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.quick-add-cart').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const quantity = 1;

            try {
                const formData = new FormData();
                formData.append('quantity', quantity);
                formData.append('csrfmiddlewaretoken', getCsrfToken());

                const response = await fetch(`/cart/add/${productId}/`, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();

                if (data.status === 'ok') {
                    showToast(data.message, 'success');
                    // Update cart badge
                    const badge = document.querySelector('.navbar .bi-cart3').closest('a').querySelector('.badge');
                    if (badge) badge.textContent = data.cart_count;
                } else {
                    showToast(data.message || 'Error adding to cart', 'danger');
                }
            } catch (err) {
                console.error('Cart error:', err);
            }
        });
    });
});

// ─── Quantity Controls ──────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.qty-minus').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.closest('.quantity-control').querySelector('input');
            const val = parseInt(input.value);
            if (val > 1) input.value = val - 1;
        });
    });

    document.querySelectorAll('.qty-plus').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.closest('.quantity-control').querySelector('input');
            const max = parseInt(input.max) || 999;
            const val = parseInt(input.value);
            if (val < max) input.value = val + 1;
        });
    });
});

// ─── Rating Stars ───────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.star-picker').forEach(picker => {
        const stars = picker.querySelectorAll('.star');
        const input = picker.querySelector('input[type="hidden"]');

        stars.forEach((star, idx) => {
            star.addEventListener('click', function() {
                const rating = idx + 1;
                input.value = rating;
                stars.forEach((s, i) => {
                    s.classList.toggle('active', i < rating);
                });
            });

            star.addEventListener('mouseover', function() {
                stars.forEach((s, i) => s.classList.toggle('hover', i <= idx));
            });
        });

        picker.addEventListener('mouseleave', function() {
            stars.forEach(s => s.classList.remove('hover'));
        });
    });
});

// ─── Charts Helper ──────────────────────────────────────────────────────────

/**
 * Create a line chart.
 */
function createLineChart(canvasId, labels, datasets, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'top' } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                x: { grid: { color: 'rgba(0,0,0,0.05)' } }
            },
            ...options
        }
    });
}

/**
 * Create a bar chart.
 */
function createBarChart(canvasId, labels, datasets, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'top' } },
            scales: { y: { beginAtZero: true } },
            ...options
        }
    });
}

/**
 * Create a doughnut chart.
 */
function createDoughnutChart(canvasId, labels, data, colors = null) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    const bgColors = colors || [
        '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
        '#06b6d4', '#ec4899', '#84cc16', '#f97316', '#6366f1'
    ];
    return new Chart(ctx, {
        type: 'doughnut',
        data: { labels, datasets: [{ data, backgroundColor: bgColors }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'right' } }
        }
    });
}

// ─── CSRF Token Helper ──────────────────────────────────────────────────────

function getCsrfToken() {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1].trim() : '';
}

// ─── Confirm Delete Dialogs ─────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-confirm]').forEach(el => {
        el.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Are you sure?';
            if (!confirm(message)) e.preventDefault();
        });
    });
});

// ─── Auto-dismiss Alerts ────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        document.querySelectorAll('.alert.alert-dismissible').forEach(alert => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        });
    }, 5000);
});

// ─── Price Range Slider ─────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function() {
    const minInput = document.getElementById('id_min_price');
    const maxInput = document.getElementById('id_max_price');

    if (minInput && maxInput) {
        maxInput.addEventListener('change', function() {
            const min = parseFloat(minInput.value) || 0;
            const max = parseFloat(this.value) || Infinity;
            if (min > max) {
                minInput.value = '';
                showToast('Min price cannot exceed max price', 'warning');
            }
        });
    }
});

// ─── Smooth scroll for anchor links ─────────────────────────────────────────

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
