$(document).ready(function() {
  if (document.URL.indexOf("change") >= 0) {
      alert("ADD!!!!!");
      ajax_filter("/heranca/combo", "id_b", $('#id_a').val(), "campo1");
  }
}); 
