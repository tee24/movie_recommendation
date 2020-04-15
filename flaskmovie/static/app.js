$(document).ready(function(){
  $("#topRated").click(function() {
      $.ajax({
      url: '/update',
      type: "GET",
      data: { foo: 'blahblahblah'}
});
  });
});