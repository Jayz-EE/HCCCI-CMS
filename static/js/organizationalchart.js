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