var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    //
    pagination: {
      el: ".swiper-pagination",
      clickable:true,
    },
  });

$(document).ready(function(){   

    // shrink navbar
    // When the user scrolls down 80px from the top of the document, resize the navbar's padding and the logo's font size
    window.onscroll = function() {myFunction()};

    var navbar = document.getElementById("resizeNav");
    var sticky = navbar.offsetTop;

    function myFunction() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky")
    } else {
        navbar.classList.remove("sticky");
    }
    }

});

// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
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

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.mute();
    event.target.playVideo();
}



