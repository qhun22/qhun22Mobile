// ===== MAIN JAVASCRIPT =====
// General UI logic - sliders, dropdowns, search, etc.
// Load this AFTER toast.js

document.addEventListener('DOMContentLoaded', function() {
    // ===== DROPDOWN MENU =====
    (function() {
        const categoryBtn = document.getElementById('categoryBtn');
        const categoryDropdown = document.getElementById('categoryDropdown');

        if (categoryBtn && categoryDropdown) {
            categoryBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                categoryDropdown.classList.toggle('show');
                this.querySelector('.fa-chevron-down').classList.toggle('rotate-180');
            });

            document.addEventListener('click', function(e) {
                if (!categoryBtn.contains(e.target) && !categoryDropdown.contains(e.target)) {
                    categoryDropdown.classList.remove('show');
                    categoryBtn.querySelector('.fa-chevron-down').classList.remove('rotate-180');
                }
            });
        }
    })();

    // ===== MAIN BANNER SLIDER =====
    (function() {
        const slides = document.querySelectorAll('.banner-slide');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const dots = document.querySelectorAll('.dot-btn');

        if (slides.length === 0) return;

        let currentSlide = 0;
        const totalSlides = slides.length;
        let autoSlideInterval;

        function showSlide(index) {
            slides.forEach(slide => {
                slide.classList.remove('opacity-100');
                slide.classList.add('opacity-0');
            });

            dots.forEach(dot => {
                dot.classList.remove('bg-white', 'w-6');
                dot.classList.add('bg-white/40', 'w-3');
            });

            slides[index].classList.remove('opacity-0');
            slides[index].classList.add('opacity-100');

            dots[index].classList.remove('bg-white/40', 'w-3');
            dots[index].classList.add('bg-white', 'w-6');

            currentSlide = index;
        }

        function nextSlide() {
            showSlide((currentSlide + 1) % totalSlides);
        }

        function prevSlide() {
            showSlide((currentSlide - 1 + totalSlides) % totalSlides);
        }

        function startAutoSlide() {
            autoSlideInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoSlide() {
            clearInterval(autoSlideInterval);
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                stopAutoSlide();
                nextSlide();
                startAutoSlide();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function() {
                stopAutoSlide();
                prevSlide();
                startAutoSlide();
            });
        }

        dots.forEach(dot => {
            dot.addEventListener('click', function() {
                stopAutoSlide();
                const slideIndex = parseInt(this.dataset.slide);
                showSlide(slideIndex);
                startAutoSlide();
            });
        });

        const mainSlider = document.getElementById('mainSlider');
        if (mainSlider) {
            mainSlider.addEventListener('mouseenter', stopAutoSlide);
            mainSlider.addEventListener('mouseleave', startAutoSlide);
        }

        startAutoSlide();
    })();

    // ===== AUTO SLIDER - SECONDARY BANNER =====
    (function() {
        const autoSliderTrack = document.getElementById('autoSliderTrack');
        if (!autoSliderTrack) return;

        let autoCurrentIndex = 0;
        const autoTotalSlides = 4;
        let autoInterval;

        function autoSlideNext() {
            autoCurrentIndex++;
            const translateValue = -(autoCurrentIndex * 50);
            autoSliderTrack.style.transform = `translateX(${translateValue}%)`;

            if (autoCurrentIndex === autoTotalSlides) {
                setTimeout(() => {
                    autoSliderTrack.style.transition = 'none';
                    autoCurrentIndex = 0;
                    autoSliderTrack.style.transform = 'translateX(0)';

                    setTimeout(() => {
                        autoSliderTrack.style.transition = 'transform 0.6s ease-in-out';
                    }, 50);
                }, 600);
            }
        }

        function startAutoSlider() {
            autoInterval = setInterval(autoSlideNext, 3500);
        }

        function stopAutoSlider() {
            clearInterval(autoInterval);
        }

        const autoSliderContainer = document.querySelector('.auto-slider-container');
        if (autoSliderContainer) {
            autoSliderContainer.addEventListener('mouseenter', stopAutoSlider);
            autoSliderContainer.addEventListener('mouseleave', startAutoSlider);
        }

        startAutoSlider();
    })();

    // ===== BRAND SCROLL =====
    (function() {
        const brandScroll = document.getElementById('brandScroll');
        const scrollLeftBtn = document.getElementById('scrollLeftBtn');
        const scrollRightBtn = document.getElementById('scrollRightBtn');

        if (!brandScroll || !scrollLeftBtn || !scrollRightBtn) return;

        const scrollAmount = 220;

        scrollLeftBtn.addEventListener('click', function() {
            brandScroll.scrollBy({
                left: -scrollAmount,
                behavior: 'smooth'
            });
        });

        scrollRightBtn.addEventListener('click', function() {
            brandScroll.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        });

        function updateButtonVisibility() {
            const scrollLeft = brandScroll.scrollLeft;
            const maxScroll = brandScroll.scrollWidth - brandScroll.clientWidth;

            if (scrollLeft > 0) {
                scrollLeftBtn.classList.remove('disabled');
            } else {
                scrollLeftBtn.classList.add('disabled');
            }

            if (scrollLeft < maxScroll - 1) {
                scrollRightBtn.classList.remove('disabled');
            } else {
                scrollRightBtn.classList.add('disabled');
            }
        }

        brandScroll.addEventListener('scroll', updateButtonVisibility);
        updateButtonVisibility();
    })();

    // ===== SEARCH BOX =====
    (function() {
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');

        if (searchBtn && searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchBtn.click();
                }
            });
        }
    })();

    // ===== HEADER SCROLL EFFECT =====
    (function() {
        const header = document.querySelector('header');
        if (!header) return;

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 50) {
                header.classList.add('shadow-lg');
            } else {
                header.classList.remove('shadow-lg');
            }
        });
    })();

    // ===== PRODUCT GRID FILTER (if exists) =====
    (function() {
        const productGrid = document.getElementById('productGrid');
        const filterForm = document.getElementById('productFilterForm');
        
        if (!productGrid || !filterForm) return;

        // For Django-powered grids, the form submits normally
        filterForm.addEventListener('change', function() {
            // Could add AJAX filtering here if needed
        });
    })();
});

console.log('Main JavaScript loaded');



