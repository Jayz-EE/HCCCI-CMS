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

$('.show-btn').click(function(){
    $('.lor1').toggle();
    
    let btn1 = $('.show-btn').text()
    if (btn1 == 'Show More') {
        $('.show-btn').text('Show Less').css('color','black').css('background-color','#e3c194');
    }else{
        $('.show-btn').text('Show More').css('color','#f3f3f3').css('background-color','#447996');;
    }
});

$('.show-btn2').click(function(){
    $('.lor2').toggle();
    
    let btn2 = $('.show-btn2').text()
    if (btn2 == 'Show More'){
        $('.show-btn2').text('Show Less').css('color','black').css('background-color','#e3c194');
    }
    else{
        $('.show-btn2').text('Show More').css('color','#f3f3f3').css('background-color','#447996');;
    }
});

$('.show-btn3').click(function(){
    $('.lor3').toggle();
    
    let btn3 = $('.show-btn3').text()
    if (btn3 == 'Show More'){
        $('.show-btn3').text('Show Less').css('color','black').css('background-color','#e3c194');
    }
    else{
        $('.show-btn3').text('Show More').css('color','#f3f3f3').css('background-color','#447996');;
    }
});

$('.show-btn4').click(function(){
    $('.lor4').toggle();
    
    let btn4 = $('.show-btn4').text();
    if (btn4 == 'Show More'){
        $('.show-btn4').text('Show Less').css('color','black').css('background-color','#e3c194');
    }
    else{
        $('.show-btn4').text('Show More').css('color','#f3f3f3').css('background-color','#447996');
    }
});

});