AOS.init();
// Swiper JS 

$(document).ready(function() {
    function handleResize() {
        if ($(window).width() < 600) {
            $('#footer-cont').removeClass('row');
        } else {
            $('#footer-cont').addClass('row');
        }
    }

    // Run on initial load
    handleResize();

    // Listen to window resize events
    $(window).resize(function() {
        handleResize();
    });
});

let isNavbarShown = false; // Track visibility

function toggleNavbar() {
    const navbar = document.getElementById('mynavbar');
    isNavbarShown = !isNavbarShown; // Toggle the state
    if (isNavbarShown) {
        navbar.classList.add('show'); // Show navbar
    } else {
        navbar.classList.remove('show'); // Hide navbar
    }
}

// Event listener for the toggler
document.getElementById('navbarToggler').addEventListener('click', toggleNavbar);

// Resize event to manage navbar visibility
window.addEventListener('resize', function () {
    const navbar = document.getElementById('mynavbar');
    const screenWidth = window.innerWidth;

    if (screenWidth >= 1015) {
        navbar.classList.remove('show'); // Hide navbar when resizing up
        isNavbarShown = false; // Reset state
    }
});

// Scroll to Top Functionality
const scrollToTopBtn = document.getElementById('scrollToTop');

window.addEventListener('scroll', () => {
    if (window.scrollY > 200) { // Show the button when scrolled down 200px
        scrollToTopBtn.style.display = 'block';
    } else {
        scrollToTopBtn.style.display = 'none';
    }
});

scrollToTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Smooth scrolling to top
    });
});

// // Function to handle scroll changes
// function updateStickyBackground() {
//     const navbar = document.querySelector('#navbar');
//     if (window.scrollY > 10) {
//         navbar.classList.add("bg-white-low-transparency"); // When scrolled down - Low Transparency
//         navbar.classList.remove("bg_white");
//     } else {
//         navbar.classList.add("bg_white"); // When at the top
//         navbar.classList.remove("bg-white-low-transparency");
//     }
// }

// // Set background on document load
// document.addEventListener('DOMContentLoaded', function() {
//     updateStickyBackground(); // Set initial background color when page is loaded
// });

// // Listen to scroll event
// window.onscroll = function() {
//     updateStickyBackground(); // Update background color when scrolling
// };