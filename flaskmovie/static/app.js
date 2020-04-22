let endpoint = 'popular'

 //top rated ajax
$(document).ready(function(){
  $("#topRated").click(function() {
      endpoint = 'top_rated'
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

 //upcoming ajax
$(document).ready(function(){

  $("#upcoming").click(function() {
      endpoint = 'upcoming'
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

 //slick functionality
$('.wrapper').slick({
  lazyLoad: 'ondemand',
  speed: 700,
  draggable: true,
  slidesToShow: 6,
  slidesToScroll: 6,
  responsive: [
    {
      breakpoint: 1600,
      settings: {
        slidesToShow: 5,
        slidesToScroll: 5,
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

//infinite loading
$(document).ready(function() {
    let callAllowed = true;
    let page = 2
    if (top.location.pathname === '/'){
        $(window).scroll(function () {
          if ($(window).scrollTop() > $('#movie_tiles').height() / 2) {
              if (callAllowed){
                callAllowed = false;
                console.log('past halfway');
                req = $.ajax({
                          url: '/load',
                          type: "POST",
                          data: { page : page,
                                  endpoint: endpoint}
                        });
                 req.done(function(html){
                        $(html).appendTo('#movie_tiles');
                        callAllowed = true;
                        page++;
                   });
                   }
          }
        });
    }
});