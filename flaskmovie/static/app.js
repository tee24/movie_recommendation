$(document).ready(function(){

  $("#topRated").click(function() {

      req = $.ajax({
              url: '/update',
              type: "POST",
              data: { command : 'top_rated'}
            });

       req.done(function(data){
            $('#movie_tiles').html(data);
       });
  });

});

$(document).ready(function(){

  $("#upcoming").click(function() {

      req = $.ajax({
              url: '/update',
              type: "POST",
              data: { command : 'upcoming'}
            });

       req.done(function(data){
            $('#movie_tiles').html(data);
       });
  });

});

$('.wrapper').slick({
  infinite: true,
  slidesToShow: 3,
  slidesToScroll: 3,
  nextArrow: $('.forward'),
  prevArrow: $('.back')
});


         //nextArrow: $('.forward'),
  //prevArrow: $('.back')