// Function to handle scroll changes
function updateStickyBackground() {
    const stickyElement = document.querySelector('.sticky');
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 10) {
        navbar.classList.add("bg-white-low-transparency"); // When scrolled down - Low Transparency
        navbar.classList.remove("bg-white");
    } else {
        navbar.classList.add("bg-white"); // When at the top
        navbar.classList.remove("bg-white-low-transparency");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('#demo');
    const paragraphs = document.querySelectorAll('.carousel-paragraph');
    
    // Initialize the first paragraph to be active
    paragraphs[0].classList.add('active');

    carousel.addEventListener('slid.bs.carousel', function (event) {
        const activeIndex = event.to;
        
        // Hide all paragraphs
        paragraphs.forEach(paragraph => {
            paragraph.classList.remove('active', 'hide');
            paragraph.style.transform = 'translateY(100%)'; // Reset to initial position
        });

        // Show the corresponding paragraph by adding the active class
        const currentParagraph = paragraphs[activeIndex];
        currentParagraph.classList.add('active');

        // Hide the previous paragraph by sliding it out to the top
        const prevParagraphIndex = (activeIndex === 0) ? paragraphs.length - 1 : activeIndex - 1;
        paragraphs[prevParagraphIndex].classList.add('hide');
    });
});

// Function to handle scroll changes
function updateStickyBackground() {
    const stickyElement = document.querySelector('.sticky');
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 10) {
        navbar.classList.add("bg-white-low-transparency"); // When scrolled down - Low Transparency
        navbar.classList.remove("bg-white");
    } else {
        navbar.classList.add("bg-white"); // When at the top
        navbar.classList.remove("bg-white-low-transparency");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('#demo');
    const paragraphs = document.querySelectorAll('.carousel-paragraph');
    
    // Initialize the first paragraph to be active
    paragraphs[0].classList.add('active');

    carousel.addEventListener('slid.bs.carousel', function (event) {
        const activeIndex = event.to;
        
        // Hide all paragraphs
        paragraphs.forEach(paragraph => {
            paragraph.classList.remove('active', 'hide');
            paragraph.style.transform = 'translateY(100%)'; // Reset to initial position
        });

        // Show the corresponding paragraph by adding the active class
        const currentParagraph = paragraphs[activeIndex];
        currentParagraph.classList.add('active');

        // Hide the previous paragraph by sliding it out to the top
        const prevParagraphIndex = (activeIndex === 0) ? paragraphs.length - 1 : activeIndex - 1;
        paragraphs[prevParagraphIndex].classList.add('hide');
    });
});
