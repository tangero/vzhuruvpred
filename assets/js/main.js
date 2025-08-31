// Zpravodajský portál - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
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
                header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';
            } else {
                header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.3)';
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
                        <span class="suggestion-tag">Události</span>
                        <span class="suggestion-tag">Názory</span>
                        <span class="suggestion-tag">Analýzy</span>
                        <span class="suggestion-tag">Kultura</span>
                        <span class="suggestion-tag">Technologie</span>
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
            border: 2px solid var(--pirate-yellow);
            border-radius: 8px;
            font-size: 16px;
            outline: none;
        `;
        
        const closeBtn = modal.querySelector('.search-modal-close');
        closeBtn.style.cssText = `
            background: var(--pirate-yellow);
            border: none;
            font-size: 24px;
            cursor: pointer;
            padding: 8px 12px;
            color: var(--pirate-black);
            font-weight: 700;
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
            .search-suggestions h4 {
                margin-bottom: 12px;
                font-family: 'Bebas Neue', cursive;
                font-size: 18px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .suggestion-tags {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }
            .suggestion-tag {
                padding: 6px 12px;
                background: var(--pirate-yellow);
                color: var(--pirate-black);
                font-size: 14px;
                cursor: pointer;
                transition: all 0.2s;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .suggestion-tag:hover {
                background: var(--pirate-black);
                color: var(--pirate-yellow);
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

    // Reading progress bar for posts
    const postContent = document.querySelector('.post-content');
    
    if (postContent) {
        const progressBar = document.createElement('div');
        
        progressBar.className = 'reading-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 4px;
            background: #FEC900;
            z-index: 1001;
            transition: width 0.2s;
        `;
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset;
            const scrollHeight = postContent.offsetHeight;
            const clientHeight = window.innerHeight;
            const scrollPercent = (scrollTop / (scrollHeight - clientHeight)) * 100;
            progressBar.style.width = Math.min(scrollPercent, 100) + '%';
        });
    }

    // Share buttons functionality
    const shareButtons = document.querySelectorAll('.share-btn');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = window.location.href;
            const title = document.title;
            
            let shareUrl = '';
            
            if (this.textContent.includes('FB')) {
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
            } else if (this.textContent.includes('TW')) {
                shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
            }
            
            if (shareUrl) {
                window.open(shareUrl, '_blank', 'width=600,height=400');
            }
        });
    });

    console.log('Vzhůru a vpřed portál successfully initialized!');
});