//for tabs in navigation bar
$(document).ready(function() {
  $(".tabs__tab").each(function(){
    $(this).on("click", function(){
      var clicked_tab = $(this);
      $(".tabs__tab").not(clicked_tab).each(function(){
        $(this).removeClass("tabs__tab_active");
      });
      $(this).addClass("tabs__tab_active");
      $(this).css("color",'#000');
    });
  });
});

$('#account').click(function() {
  $('.sidenav_wrap').toggleClass('active2');
  $('body').toggleClass("overflow_y");
});

$(function(){
  $('body').swipe( {
    //Single swipe handler for left swipes
    //Generic swipe handler for all directions
    swipe:function(event, direction, distance, duration, fingerCount, fingerData) {
      if(direction =="left"){
        $('.sidenav_wrap').removeClass('active2');
        $('body').removeClass("overflow_y");
      }else if(direction =="right"){
        $("html, body").animate({ scrollTop: 0 }, "slow");
        $('.sidenav_wrap').addClass('active2');
        $('body').addClass("overflow_y");
        return false;
      }
    },
    //
    //Default is 75px, set to 0 for demo so any distance triggers swipe
    threshold: 0
  });
});
