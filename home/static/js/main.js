function onSuccess(googleUser) {
    var profile = googleUser.getBasicProfile();
    gapi.client.load('plus', 'v1', function () {
        var request = gapi.client.plus.people.get({
            'userId': 'me'
        });
        //Display the user details
        request.execute(function (resp) {
            var profileHTML = '<div class="profile"><div class="head">Welcome '+resp.name.givenName+
            '! <a href="javascript:void(0);" onclick="signOut();">Sign out</a></div>';
             $("#dummyimage").attr("src",resp.image.url);
             document.getElementByClass('user_name').innerHTML =resp.displayName;
             $("#dummyimage").attr("alt",resp.displayName);

            $('#gSignIn').slideUp('slow');
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
        $('.userContent').html('');
        $('#gSignIn').slideDown('slow');
    });
}
$(document).ready(function() {
$(".tabs__tab").each(function(){
$(this).on("click", function(){
   var clicked_tab = $(this);
                $(".tabs__tab").not(clicked_tab).each(function(){
                $(this).removeClass("tabs__tab_active");
                });
                $(this).addClass("tabs__tab_active");
			});
		});
});
