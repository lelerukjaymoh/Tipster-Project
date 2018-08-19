$( function() {
    $( "#datepicker" ).datepicker();
    $( "#anim" ).on( "change", function() {

      alert("Hey there");
      $( "#datepicker" ).datepicker( "option", "showAnim", $( this ).val() );
    });
  } );