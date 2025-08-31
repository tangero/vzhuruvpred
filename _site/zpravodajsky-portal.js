// Zpravodajský portál - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Aktuální datum a čas
    function updateDateTime() {
        const dateElement = document.getElementById('current-date');
        if (dateElement) {
            const now = new Date();
            const options = { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            };
            dateElement.textContent = now.toLocaleDateString('cs-CZ', options);
        }
    }
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const mainNav = document.getElementById('main-nav');
    
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            
            // Animate hamburger menu
            const spans = menuToggle.querySelectorAll('span');
            if (mainNav.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translateY(8px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
            } else {
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!menuToggle.contains(e.target) && !mainNav.contains(e.target)) {
                mainNav.classList.remove('active');
                const spans = menuToggle.querySelectorAll('span');
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            }
        });
    }

    // Back to top button
    const backToTopBtn = document.getElementById('back-to-top');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });

        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Sticky header effect
    let lastScrollTop = 0;
    const header = document.querySelector('.header');
    
    if (header) {
        window.addEventListener('scroll', function() {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 100) {
                header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            } else {
                header.style.boxShadow = '';
            }
            
            lastScrollTop = scrollTop;
        });
    }

    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('.newsletter-input');
            const email = emailInput.value;
            
            if (email && validateEmail(email)) {
                alert('Děkujeme za přihlášení k odběru novinek! Na email ' + email + ' jsme zaslali potvrzení.');
                emailInput.value = '';
            } else {
                alert('Prosím zadejte platnou emailovou adresu.');
            }
        });
    }

    // Email validation
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Sport tabs
    const sportTabs = document.querySelectorAll('.sport-tab');
    
    sportTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            sportTabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Here you would typically filter the sport content
            // For demo purposes, we'll just log the action
            console.log('Switched to:', this.textContent);
        });
    });

    // Theme toggle (dark/light mode)
    const themeToggle = document.querySelector('.theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    if (themeToggle) {
        // Set initial theme
        document.documentElement.setAttribute('data-theme', currentTheme);
        
        themeToggle.addEventListener('click', function() {
            const theme = document.documentElement.getAttribute('data-theme');
            const newTheme = theme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Animate icon change
            this.style.transform = 'rotate(180deg)';
            setTimeout(() => {
                this.style.transform = '';
            }, 300);
        });
    }

    // Search functionality
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const searchModal = createSearchModal();
            document.body.appendChild(searchModal);
            
            const searchInput = searchModal.querySelector('.search-modal-input');
            searchInput.focus();
            
            // Close modal on escape or click outside
            searchModal.addEventListener('click', function(e) {
                if (e.target === searchModal) {
                    searchModal.remove();
                }
            });
            
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    searchModal.remove();
                }
            });
        });
    }

    // Create search modal
    function createSearchModal() {
        const modal = document.createElement('div');
        modal.className = 'search-modal';
        modal.innerHTML = `
            <div class="search-modal-content">
                <div class="search-modal-header">
                    <input type="text" class="search-modal-input" placeholder="Hledat články, témata, autory...">
                    <button class="search-modal-close">✕</button>
                </div>
                <div class="search-suggestions">
                    <h4>Populární vyhledávání</h4>
                    <div class="suggestion-tags">
                        <span class="suggestion-tag">Politika</span>
                        <span class="suggestion-tag">Ekonomika</span>
                        <span class="suggestion-tag">Sport</span>
                        <span class="suggestion-tag">Kultura</span>
                        <span class="suggestion-tag">Zdraví</span>
                    </div>
                </div>
            </div>
        `;
        
        // Style the modal
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeIn 0.3s;
        `;
        
        const content = modal.querySelector('.search-modal-content');
        content.style.cssText = `
            background: white;
            border-radius: 12px;
            padding: 24px;
            width: 90%;
            max-width: 600px;
            animation: slideUp 0.3s;
        `;
        
        const header = modal.querySelector('.search-modal-header');
        header.style.cssText = `
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
        `;
        
        const input = modal.querySelector('.search-modal-input');
        input.style.cssText = `
            flex: 1;
            padding: 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
        `;
        
        const closeBtn = modal.querySelector('.search-modal-close');
        closeBtn.style.cssText = `
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
            color: #64748b;
        `;
        
        closeBtn.addEventListener('click', () => modal.remove());
        
        // Add animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideUp {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            .suggestion-tags {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                margin-top: 12px;
            }
            .suggestion-tag {
                padding: 6px 12px;
                background: #f1f5f9;
                border-radius: 20px;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .suggestion-tag:hover {
                background: #dc2626;
                color: white;
            }
        `;
        document.head.appendChild(style);
        
        return modal;
    }

    // Lazy loading images
    const images = document.querySelectorAll('img[data-src]');
    
    if (images.length > 0) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }

    // Reading progress bar
    const article = document.querySelector('.article-content');
    
    if (article) {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #dc2626, #ef4444);
            z-index: 1001;
            transition: width 0.2s;
        `;
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset;
            const scrollHeight = article.offsetHeight;
            const clientHeight = window.innerHeight;
            const scrollPercent = (scrollTop / (scrollHeight - clientHeight)) * 100;
            progressBar.style.width = Math.min(scrollPercent, 100) + '%';
        });
    }

    // Share buttons functionality
    const shareButtons = document.querySelectorAll('[data-share]');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const platform = this.dataset.share;
            const url = window.location.href;
            const title = document.title;
            
            let shareUrl = '';
            
            switch(platform) {
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                    break;
                case 'twitter':
                    shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                    break;
                case 'linkedin':
                    shareUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`;
                    break;
                case 'email':
                    shareUrl = `mailto:?subject=${title}&body=${url}`;
                    break;
            }
            
            if (shareUrl) {
                window.open(shareUrl, '_blank', 'width=600,height=400');
            }
        });
    });

    // Auto-refresh for breaking news
    const breakingNews = document.querySelector('.ticker');
    
    if (breakingNews) {
        // Simulate new breaking news every 30 seconds
        setInterval(() => {
            const newsItems = [
                '🔴 Nová zpráva: Vláda oznámila další opatření',
                '🔴 Aktuálně: Dopravní nehoda na D1 způsobila kolony',
                '🔴 Sport: Česká reprezentace vyhrála důležitý zápas',
                '🔴 Ekonomika: Koruna posiluje vůči euru'
            ];
            
            const randomNews = newsItems[Math.floor(Math.random() * newsItems.length)];
            const newItem = document.createElement('span');
            newItem.className = 'ticker-item';
            newItem.textContent = randomNews;
            newItem.style.animation = 'slideInRight 0.5s';
            
            breakingNews.appendChild(newItem);
            
            // Remove old items if too many
            if (breakingNews.children.length > 5) {
                breakingNews.removeChild(breakingNews.firstChild);
            }
        }, 30000);
    }

    // Add animation styles
    const animationStyles = document.createElement('style');
    animationStyles.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(animationStyles);

    console.log('Zpravodajský portál successfully initialized!');
});