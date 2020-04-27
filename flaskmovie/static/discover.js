$( function() {
    $( "#slider-range" ).slider({
      range: true,
      animate: true,
      min: 1900,
      max: 2020,
      values: [ 1980, 2016 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      }
    });
    //set default values for label
      $( "#amount" ).val($( "#slider-range" ).slider( "values", 0 ) +
               " - " + $( "#slider-range" ).slider( "values", 1 ) );
         });
$( "#button" ).click(function() {
  let gte = $( "#slider-range" ).slider( "values", 0 );
  let lte = $( "#slider-range" ).slider( "values", 1 );
  let email = $('#exampleInputEmail1').val();
  let selected = $('select').val();
  console.log(selected)
  $.ajax({
              url: '/test',
              type: "POST",
              data: { gte : gte,
                      lte : lte,
                        email : email,
                        selected : selected}
            });
});

$(function(){

  $("select").bsMultiSelect();

});