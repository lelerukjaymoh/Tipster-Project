function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    alert("Hey There");
    gapi.client.load('plus', 'v1', function () {
        var request = gapi.client.plus.people.get({
            'userId': 'me'
        });
        //Display the user details
        request.execute(function (resp) {
            var profileHTML = '<div class="profile"><div class="head">Welcome '+resp.name.givenName +
            '! <a href="javascript:void(0);" onclick="signOut();">Sign out</a></div>';
             $("#dummyimage").attr("src",resp.image.url);
             document.getElementByClass('user_name').innerHTML = resp.displayName;
             $("#dummyimage").attr("alt",resp.displayName);
        });
    });
}
function onFailure(error) {
    alert(error);
}
function renderButton() {
    gapi.signin2.render('gSignIn', {
        'scope': 'profile email',
        'width': 240,
        'height': 50,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess': onSuccess,
        'onfailure': onFailure
    });
}
function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}

$('#signin').click(function() {
			$(this).toggleClass('on');
			$('#resize').toggleClass("active");
});
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
$('.sidenav_wrap').on( "swipeleft", function( event ) 
  {
    $(this).removeClass('active2');
  } );
$('#content').on( "swiperight", function( event ) 
{
 $(this).addClass('active2');
} );