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
$(document).ready(function(){
    //  buttons
    $('.lvlbtn1').click(function(){
        $('.lvlbtn2').removeClass('btnactive1');
        $('.lvlbtn3').removeClass('btnactive1');
        $('.lvlbtn1').addClass('btnactive1');
    });
    $('.lvlbtn2').click(function(){
        $('.lvlbtn1').removeClass('btnactive1');
        $('.lvlbtn3').removeClass('btnactive1');
        $('.lvlbtn2').addClass('btnactive1');
    });
    $('.lvlbtn3').click(function(){
        $('.lvlbtn1').removeClass('btnactive1');
        $('.lvlbtn2').removeClass('btnactive1');
        $('.lvlbtn3').addClass('btnactive1');
    });

    // shs start
    $('.btnpolicyshs').click(function(){
        $('.btnreqshs').removeClass('btnactive');
        $('.btnpolicyshs').addClass('btnactive');
        $('.datareqshs').hide();
        $('.datapolicy').show();
    });

    $('.btnreqshs').click(function(){
        $('.btnpolicyshs').removeClass('btnactive');
        $('.btnreqshs').addClass('btnactive');
        $('.datapolicy').hide();
        $('.datareqshs').show();
    });
    // shs End

    // ElemJhs Start
    $('.btnpolicyelem').click(function(){
        $('.btnreqelem').removeClass('btnactive');
        $('.btnpolicyelem').addClass('btnactive');
        $('.datareqelemjhs').hide();
        $('.datapolicy1').show();
    });
    $('.btnreqelem').click(function(){
        $('.btnpolicyelem').removeClass('btnactive');
        $('.btnreqelem').addClass('btnactive');
        $('.datapolicy1').hide();
        $('.datareqelemjhs').show();
    });
    // ElemJhs End

});