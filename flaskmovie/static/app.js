$(document).ready(function(){

  $("#topRated").click(function() {

      req = $.ajax({
              url: '/update',
              type: "POST",
              data: { foo: 'blahblahblah'}
            });

       req.done(function(data){
            $('#testText').text(data.result);
       });
  });

});