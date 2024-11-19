// Load the IFrame Player API asynchronously
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var hccciVideo;
function onYouTubeIframeAPIReady() {
    hccciVideo = new YT.Player('hccciVideo', {
        width: '100%',
        videoId: 'Hs4LRng3u9c',
        playerVars: { 'autoplay': 1, 'playsinline': 1 },
        events: {
            'onReady': onPlayerReady
        }
    });
}

function onPlayerReady(event) {
    event.target.mute();
    event.target.playVideo();   
}

// Set background color on document load and on scroll
document.addEventListener('DOMContentLoaded', function() {
    updateStickyBackground();
    window.onscroll = updateStickyBackground; // Update background color when scrolling
});

document.addEventListener("DOMContentLoaded", () => {
    // Function to animate elements when they enter or leave the viewport
    const animateOnScroll = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Element enters the viewport
                if (entry.target.classList.contains('imageCore')) {
                    entry.target.classList.remove('animate-slide-out-left');
                    entry.target.classList.add('animate-slide-in-left');
                } else if (entry.target.classList.contains('imageCoreRight')) {
                    entry.target.classList.remove('animate-slide-out-right');
                    entry.target.classList.add('animate-slide-in-right');
                } else if (entry.target.classList.contains('fades')) {
                    entry.target.classList.remove('animate-fade-out');
                    entry.target.classList.add('animate-fade');
                } else if (entry.target.classList.contains('slideDown')) {
                    entry.target.classList.remove('animate-slide-down-out');
                    entry.target.classList.add('animate-slide-down-in');  // Slide down on entry
                }
            } else {
                // Element leaves the viewport
                if (entry.target.classList.contains('imageCore')) {
                    entry.target.classList.remove('animate-slide-in-left');
                    entry.target.classList.add('animate-slide-out-left');
                } else if (entry.target.classList.contains('imageCoreRight')) {
                    entry.target.classList.remove('animate-slide-in-right');
                    entry.target.classList.add('animate-slide-out-right');
                } else if (entry.target.classList.contains('fades')) {
                    entry.target.classList.remove('animate-fade');
                    entry.target.classList.add('animate-fade-out');
                } else if (entry.target.classList.contains('slideDown')) {
                    entry.target.classList.remove('animate-slide-down-in');
                    entry.target.classList.add('animate-slide-down-out'); // Slide down on exit
                }
            }
        });
    };

    // Create an Intersection Observer instance
    const observer = new IntersectionObserver(animateOnScroll, {
        threshold: 0.5 // Trigger when 50% of the element is visible
    });

    // Select all the elements you want to animate
    const elementsToAnimate = document.querySelectorAll('.imageCore, .imageCoreRight, .fades, .slideDown');

    // Observe each element
    elementsToAnimate.forEach(element => {
        observer.observe(element);
    });
});
