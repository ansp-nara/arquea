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

   /**
    * Eventos para abrir ou esconder a tabela de conflito de equipamentos
    */
   $(".conflitos-title").click(function(){
	   $(this).siblings(".conflitos-content").toggle(); 
   });
   
   /**
    * Exibe ou esconde as imagens dos stencils dos equipamentos
    * Os disparos ocorrem no checkbox e no label do checkbox
    */
   $("#chk_stencil").change(function(e){
	   $(".interno a img").toggle();
	   
	   var showOrHide = ($('#chk_stencil').prop('checked'));
	   var newUrl = updateQueryString('chk_stencil', showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   });
   $("#chk_stencil + span").click(function(e){
	   var showOrHide = !($('#chk_stencil').prop('checked'));
	   
	   $(".interno a img").toggle(showOrHide);
	   $('#chk_stencil').prop('checked', showOrHide);
	   
	   var newUrl = updateQueryString('chk_stencil', showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   });
   
   /**
    * Exibe ou esconde as legendas dos equipamentos.
    * Os disparos ocorrem no checkbox e no label do checkbox
    */
   $("#chk_legenda").click(function(e){
	   $(".equip div div:nth-child(1)").toggle();
	   
	   var showOrHide = ($('#chk_legenda').prop('checked'));
	   var newUrl = updateQueryString('chk_legenda', showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   });
   $("#chk_legenda + span").click(function(e){
	   var showOrHide = !($('#chk_legenda').prop('checked'));
	   
	   $(".equip div div:nth-child(1)").toggle(showOrHide);
	   $('#chk_legenda').prop('checked', showOrHide);
	   
	   var newUrl = updateQueryString('chk_legenda', showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   });
   
   /**
    * Exibe ou esconde as legendas dos equipamentos.
    * Os disparos ocorrem no checkbox e no label do checkbox
    */
   $("#chk_legenda_desc").click(function(e){
	   $(".equip div div:nth-child(2)").toggle();
	   
	   var showOrHide = ($('#chk_legenda_desc').prop('checked'));
	   var newUrl = updateQueryString('chk_legenda_desc', showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   });
   $("#chk_legenda_desc + span").click(function(e){
	   var showOrHide = !($('#chk_legenda_desc').prop('checked'));
	   
	   $(".equip div div:nth-child(2)").toggle(showOrHide);
	   $('#chk_legenda_desc').prop('checked', showOrHide);
	   
	   var newUrl = updateQueryString('chk_legenda_desc', showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   });
   
   /**
    * Function para alterar a queryString de um parametro href
    */
   function updateQueryString(key, value, url) {
	    if (!url) url = window.location.href;
	    var re = new RegExp("([?|&])" + key + "=.*?(&|#|$)(.*)", "gi");

	    if (re.test(url)) {
	        if (typeof value !== 'undefined' && value !== null)
	            return url.replace(re, '$1' + key + "=" + value + '$2$3');
	        else {
	            var hash = url.split('#');
	            url = hash[0].replace(re, '$1$3').replace(/(&|\?)$/, '');
	            if (typeof hash[1] !== 'undefined' && hash[1] !== null) 
	                url += '#' + hash[1];
	            return url;
	        }
	    }
	    else {
	        if (typeof value !== 'undefined' && value !== null) {
	            var separator = url.indexOf('?') !== -1 ? '&' : '?',
	                hash = url.split('#');
	            url = hash[0] + separator + key + '=' + value;
	            if (typeof hash[1] !== 'undefined' && hash[1] !== null) 
	                url += '#' + hash[1];
	            return url;
	        }
	        else
	            return url;
	    }
	}
   
});
