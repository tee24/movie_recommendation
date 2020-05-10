 $(document).ready(function(){
window.addEventListener( "pageshow", function ( event ) {
  var historyTraversal = event.persisted ||
                         ( typeof window.performance != "undefined" &&
                              window.performance.navigation.type === 2 );
  if ( historyTraversal ) {
    // Handle page restore.
    window.location.reload( true );
  }
});
});

let endpoint = 'movie/popular'
 //movies ajax
$(document).ready(function(){
  $("#movies").click(function() {
      endpoint = 'movie/popular'
      req = $.ajax({
              url: '/update',
              type: "POST",
              data: { command : endpoint}
            });

       req.done(function(data){
            $('#movie_tiles').html(data);
            $('title').html('Home - Movies');
       });
  });

});

 //tv ajax
$(document).ready(function(){

  $("#television").click(function() {
      endpoint = 'tv/popular'
      req = $.ajax({
              url: '/update',
              type: "POST",
              data: { command : endpoint,
                      tv : true  }
            });

       req.done(function(data){
            $('#movie_tiles').html(data);
            $('title').html('Home - Television');
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
  arrows: false,
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
  ]
});

$('.forward').click(function(){
  $(this).nextAll('.wrapper').slick('slickNext');
});

$('.back').click(function(){
  $(this).nextAll('.wrapper').slick('slickPrev');
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

//TV EPISODE INFO
$(document).ready(function(){
  let pathname = window.location.pathname;
  let show_id = pathname.substring(pathname.lastIndexOf('/') + 1);
  $(".post-image-season").click(function() {
      let season_number = this.id
      req = $.ajax({
              url: '/update_tv',
              type: "POST",
              data: { season_number : season_number,
                      show_id: show_id}
            });

       req.done(function(data){
            $('#episode-tiles').fadeOut(500, function() {
            $(this).html(data.html).fadeIn(500);
            });

            ratingsChart.data.datasets[0].data = data.chart_info.ratings;
            ratingsChart.data.labels = data.chart_info.names;
            ratingsChart.update();

       });
  });

});

$(document).ready(function(){
    $("#id1").click(); // load first season chart
});

$(document).ready(function(){
    $('.form-control').focus(function(){
        $(this).css('background-color', 'rgb(232, 240, 254)');
    });

     $('.form-control').blur(function(){
        $(this).css('background-color', '');
    });
});

$(document).ready(function(){

 $(".card-rec").hover(function(){
    let imgId = '#card-rec-' + $(this).attr('id');
    let textId = '#card-rec-text' + $(this).attr('id').substring(3);

    $(this).css("border", "2px solid yellow");
    $(this).css("margin", "-2px");

    $(imgId).removeClass('hide-element');
    $(textId).removeClass('hide-element');

    if((! $(this).hasClass('active-small')) && (! $(this).hasClass('active'))){
    $('.active').addClass('hide-element');
    $('.active').removeClass('active');
    $('.active-small').removeClass('active-small');
    $(this).addClass('active-small');

    };



    $(imgId).addClass('active');
    $(textId).addClass('active');

    },

    function(){
    $(this).css("border", "");
  });

});

$(document).ready(function(){

$(".watched-button").click(function() {
      let watchedButton = $(this);
      let add = 1;
      let method = 'episode';

      if (watchedButton.hasClass('season')){
         method = 'season';
      } else if (watchedButton.hasClass('show')){
         method = 'show'
      }


      if (watchedButton.hasClass('watched')){
        add = 0;
      };

      req = $.ajax({
              url: '/mark_watched',
              type: "POST",
              data: { ids : $(this).attr('id'),
                       add: add,
                       method: method}
            });

       req.done(function(){
        if (watchedButton.hasClass('unwatched')){
            watchedButton.removeClass('unwatched');
            watchedButton.addClass('watched');
        } else{
            watchedButton.removeClass('watched');
            watchedButton.addClass('unwatched');
        }
       });
  });

});

$(document).ready(function() {
$('.summernote').summernote({
  toolbar: [
    // [groupName, [list of button]]
    ['style', ['bold', 'italic', 'underline', 'clear']],
    ['font', ['strikethrough', 'superscript', 'subscript']],
    ['fontsize', ['fontsize']],
    ['color', ['color']],
    ['para', ['ul', 'ol', 'paragraph']],
    ['height', ['height']]
  ]
});
});

$(document).ready(function(){
  $(document).on('click', '.page-selector', function() {
      let id = $(this).attr('id');
      req = $.ajax({
              url: '/movie/comments/update',
              type: "POST",
              data: { id : id}
            });

       req.done(function(data){

            $('html, body').animate({
                scrollTop: $("#comment-header").offset().top - 50 // Scroll 50px less
            }, 1000);

            $('#movie-comments').fadeOut(500, function() {
            $(this).html(data.comments_html).fadeIn(500);
            });

            $('#pages').html(data.pages_html);

            });
       });
  });

$(document).ready(function(){

  $(document).on('click', '.edit-comment', function() {
     let postId = $(this).attr('id');
      $('.modal-body form').attr('action', 'update/post/' + postId.substring(3));

$('.editsummernote').summernote({
  toolbar: [
    // [groupName, [list of button]]
    ['style', ['bold', 'italic', 'underline', 'clear']],
    ['font', ['strikethrough', 'superscript', 'subscript']],
    ['fontsize', ['fontsize']],
    ['color', ['color']],
    ['para', ['ul', 'ol', 'paragraph']],
    ['height', ['height']]
  ]
});

$('.editsummernote').summernote('reset');

      req = $.ajax({
              url: '/get/post',
              type: "POST",
              data: { postId : postId}
            });

       req.done(function(data){

            $('.editsummernote').summernote('editor.pasteHTML', data);
       });
  });

});

$(document).ready(function(){
$(document).on('click', '.delete-comment', function() {
    let pathname = window.location.pathname;
    let postId = $(this).attr('id');

      $(document).on('click', '.delete-comment-modal', function() {

      let route = 'delete/post/' + postId.substring(7);

      console.log('hello');
      req = $.ajax({
              url: route,
              type: "POST",
              data: { postId : postId}
            });

       req.done(function(redirect){
            window.location.replace(pathname);

       });
  });
});
});