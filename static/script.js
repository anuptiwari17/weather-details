document.addEventListener("DOMContentLoaded", () => {
    // Theme toggle functionality
    const themeSwitch = document.getElementById('theme-switch');
    const htmlElement = document.documentElement;
    
    // Check for saved theme preference or use device preference
    const currentTheme = localStorage.getItem('theme') || 
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    // Set initial theme
    htmlElement.setAttribute('data-theme', currentTheme);
    themeSwitch.checked = currentTheme === 'dark';
    
    // Handle theme switch
    themeSwitch.addEventListener('change', function() {
        if (this.checked) {
            htmlElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            htmlElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Form submission animation
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", () => {
            // Add loading state to button
            const button = form.querySelector("button");
            const originalText = button.textContent;
            button.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Loading...';
            button.disabled = true;
            
            // Restore button state if form submission takes too long
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 10000);
        });
    }
    
    // Auto-hide error message after 6 seconds
    const errorMessage = document.querySelector(".error-message");
    if (errorMessage) {
        setTimeout(() => {
            errorMessage.style.opacity = "0";
            setTimeout(() => {
                errorMessage.style.display = "none";
            }, 500);
        }, 6000);
    }
    
    // Add horizontal scroll buttons for forecast cards on desktop
    const forecastCards = document.querySelector('.forecast-cards');
    if (forecastCards && window.innerWidth > 768) {
        // Create navigation buttons
        const scrollLeftBtn = document.createElement('button');
        const scrollRightBtn = document.createElement('button');
        
        scrollLeftBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
        scrollRightBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
        
        scrollLeftBtn.classList.add('scroll-btn', 'scroll-left');
        scrollRightBtn.classList.add('scroll-btn', 'scroll-right');
        
        // Add buttons to DOM
        forecastCards.parentNode.appendChild(scrollLeftBtn);
        forecastCards.parentNode.appendChild(scrollRightBtn);
        
        // Add scroll functionality
        scrollLeftBtn.addEventListener('click', () => {
            forecastCards.scrollBy({ left: -300, behavior: 'smooth' });
        });
        
        scrollRightBtn.addEventListener('click', () => {
            forecastCards.scrollBy({ left: 300, behavior: 'smooth' });
        });
        
        // Append CSS for scroll buttons
        const style = document.createElement('style');
        style.textContent = `
            .scroll-btn {
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: var(--primary-color);
                color: white;
                border: none;
                cursor: pointer;
                box-shadow: 0 3px 6px rgba(0,0,0,0.2);
                z-index: 10;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .scroll-btn:hover {
                background-color: var(--secondary-color);
            }
            .scroll-left {
                left: -15px;
            }
            .scroll-right {
                right: -15px;
            }
            .forecast-cards {
                position: relative;
                padding: 0 20px;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add animation to chart cards
    const chartCards = document.querySelectorAll('.chart-card');
    if (chartCards.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        chartCards.forEach(card => {
            observer.observe(card);
        });
        
        // Add animation CSS
        const animationStyle = document.createElement('style');
        animationStyle.textContent = `
            .chart-card {
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }
            .chart-card.animate-in {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(animationStyle);
    }
});