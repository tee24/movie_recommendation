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
  dots: true,
  infinite: false,
  speed: 1000,
  slidesToShow: 6,
  slidesToScroll: 6,
  responsive: [
    {
      breakpoint: 1600,
      settings: {
        slidesToShow: 5,
        slidesToScroll: 5,
        infinite: true,
        dots: true
      }
    },
    {
      breakpoint: 1300,
      settings: {
        slidesToShow: 4,
        slidesToScroll: 4
      }
    },
    {
      breakpoint: 1000,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3
      }
    },
    {
      breakpoint: 700,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2
      }
    },
    {
      breakpoint: 550,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1
      }
    }
  ],
  nextArrow: $('.forward'),
  prevArrow: $('.back')
});