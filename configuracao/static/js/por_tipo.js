function sel_tipo_equip() {
    tipo = document.getElementById('id_tipo')
    estado = document.getElementById('id_estado')
    part_number = document.getElementById('id_partnumber')

    $.ajax({
      type: "GET",
      url: '/patrimonio/filtra_pn_estado',
      dataType: "json",
      data: {'id':$("#id_tipo").val()},
      success: function(retorno){
          $("#id_estado").empty();
          $("#id_estado").append('<option value="0">Todos</option>');
          $.each(retorno['estados'], function(i, item) {
		$("#id_estado").append('<option value="'+item.pk+'">'+item.value+'</option>');
          });
          $("#id_partnumber").empty();
          $("#id_partnumber").append('<option value="0">Todos</option>');
          $.each(retorno['pns'], function(i, item) {
                $("#id_partnumber").append('<option value="'+item.pk+'">'+item.value+'</option>');
          });
      },
      error: function(erro) {
        alert('Erro: Sem valor.');
      }
    });
}
