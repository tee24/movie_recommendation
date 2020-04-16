$(document).ready(function(){

  $("#page2").click(function() {

      req = $.ajax({
              url: '/update',
              type: "POST",
              data: { foo : 'PAGE2'}
            });

       req.done(function(data){
            $('#movie_tiles').replaceWith(data);
       });
  });

});