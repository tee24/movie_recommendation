function sliderCreator(sliderId, displayId, min, max, start, end) {
    $(sliderId).slider({
      range: true,
      animate: true,
      min: min,
      max: max,
      values: [ start, end ],
      slide: function( event, ui ) {
        $(displayId).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      }
    });
    //set default values for label
      $(displayId).val($(sliderId).slider( "values", 0 ) +
               " - " + $(sliderId).slider( "values", 1 ) );
         };


sliderCreator('#year-slider', '#year', 1900, 2020, 1970, 2020);
sliderCreator('#rating-slider', '#rating', 0, 10, 6, 10);
sliderCreator('#runtime-slider', '#runtime', 60, 240, 70, 180);


$( "#button" ).click(function() {
  let year_gte = $( "#year-slider" ).slider( "values", 0 );
  let year_lte = $( "#year-slider" ).slider( "values", 1 );
  let rating_gte = $( "#rating-slider" ).slider( "values", 0 );
  let rating_lte = $( "#rating-slider" ).slider( "values", 1 );
  let runtime_gte = $( "#runtime-slider" ).slider( "values", 0 );
  let runtime_lte = $( "#runtime-slider" ).slider( "values", 1 );
  let genres = $('#genres').val();

  req = $.ajax({
              url: '/test',
              type: "POST",
              data: { year_gte : year_gte,
                      year_lte : year_lte,
                      rating_gte : rating_gte,
                      rating_lte : rating_lte,
                      runtime_gte : runtime_gte,
                      runtime_lte : runtime_lte,
                      genres : genres,
                  }
            });
       });

});

$(function(){

  $("select").bsMultiSelect();

});