function ajax_numero_fmusp() {
    if($("#id_tem_numero_fmusp").is(':checked')) {
        $("#id_numero_fmusp").parent().show();
    }
    else {
	$("#id_numero_fmusp").parent().hide();
    }
}

$(function() {
    ajax_numero_fmusp();
});
