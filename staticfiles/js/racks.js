$(function(){

   $("*[rel=tooltip]").hover(function(e){
         $("body").append('<div class="tooltip">'+$(this).attr('title')+'</div>');
         $('.tooltip').css({
                     top : e.pageY - 50,
                     left : e.pageX + 20
                     }).fadeIn();

   }, function(){
      $('.tooltip').remove();
   }).mousemove(function(e){
      $('.tooltip').css({
                     top : e.pageY - 50,
                     left : e.pageX + 20
                     })
   })

});
