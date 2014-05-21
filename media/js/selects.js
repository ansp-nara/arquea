// filters a select by hiding all non-matching items - only works in FF so far.
//
// select          -  the id of the select control to filter
// filter_by_ctrl  -  a reference to an input object with the text to filter by


function abc(select_ctrl, filter_by_ctrl)
{
sel = document.getElementById(select_ctrl);
alert(sel);
}



function filter_select(sel, filter_by)
{
    select_ctrl = document.getElementById(sel);
    filter_by_ctrl = document.getElementById(filter_by);
    filter_text = filter_by_ctrl.options[filter_by_ctrl.selectedIndex].text.replace(/^\s+|\s+$/g,"");
    //if (filter_by_ctrl.value == filter_by_ctrl.old_value) return false;    
    sel_found = false;
    
    for(i=0;i<select_ctrl.options.length;i++)
    {
        txt = select_ctrl.options[i].text;
        do_show = (!filter_text ||
                   select_ctrl.options[i].value=="" ||
                   txt.search(filter_text, "i")!=-1)
        select_ctrl.options[i].style.display = do_show ? ' block':' none';
        // preselect the first item, and try to be smart about it
        if (!sel_found && do_show) {
            if (
                (select_ctrl.options[i].value=="" && !filter_text) ||
                (select_ctrl.options[i].value!="")
               )
            {
                if (!select_ctrl.options[i].selected)
                {
                    select_ctrl.options[i].selected = true;
                    // we need to call a possible onchange manually, because it doesn't
                    // happen by itself. unfortunately, there is also an old but as-of-yet
                    // unfixed bug in firefox that requires the setTimeout() workaround,
                    // see:
                    //  * https://bugzilla.mozilla.org/show_bug.cgi?id=317600
                    //  * https://bugzilla.mozilla.org/show_bug.cgi?id=246518
                    //if (select_ctrl.onchange) window.setTimeout(function(){select_ctrl.onchange()}, 0);
                }
                sel_found = true; 
            }
        }
    }
    // do some work of our own to determine one the value has changed, for
    // performance reaonns, but e.g. we also don't want to change the selection
    // unless the filter changed at least, and definitely not on control keys
    // such as arrow up or arrow down.
    //filter_by_ctrl.old_value = filter_by_ctrl.value;
}



function filter_select2(sel, filter1, filter2)
{
    select_ctrl = document.getElementById(sel);
    filter1_by_ctrl = document.getElementById(filter1);
    filter2_by_ctrl = document.getElementById(filter2);
    filter2_text = filter2_by_ctrl.options[filter2_by_ctrl.selectedIndex].text.replace(/^\s+|\s+$/g,"");
    filter1_text = filter1_by_ctrl.options[filter1_by_ctrl.selectedIndex].text.split(" - ")[0]
    filter1_text = filter1_text.replace(/^\s+|\s+$/g,"");
    for(i=0;i<select_ctrl.options.length;i++)
    {
        txt = select_ctrl.options[i].text;
        do_show = ((!filter1_text && !filter2_text) ||
                   select_ctrl.options[i].value=="" ||
                   (txt.search(filter1_text)!=-1 && txt.search(filter2_text, "i")!=-1))
        select_ctrl.options[i].style.display = do_show ? ' block':' none';
    }
    select_ctrl.options[0].selected = true;
}



/*#function soma_dados(id_dados, id_total)
//{
//   dados = document.getElementById(id_dados);
//    total = document.getElementById(id_total);
//   t = 0.0;
//    for(i=0;i<dados.options.length;i++)
//    {
//        if (dados.options[i].selected)
//        {
//           d = dados.options[i].text.split("-");
//           v = d[d.length-1];
//           t += Number(v);
//        }
//    }
//    total.value = t.toFixed(2);
//}
*/



function ajax_soma_valores(url, objHtmlReturn, select)
{
    desp = select;

    var d=new Array();
    j = 0;

    for(i=0;i<desp.options.length;i++)
    {
        if (desp.options[i].selected)
        {
           d[j++] = desp.options[i].value;
        }
    }

    dados = {'despesas':d};
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+objHtmlReturn).val(retorno);
      },
      error: function(erro) {
        alert('Erro: Sem valor.');
      }
  });
}



function ajax_soma_valor_descricao(url, total, descricao, select)
{
    desp = select;

    var d=new Array();
    j = 0;

    for(i=0;i<desp.options.length;i++)
    {
        if (desp.options[i].selected)
        {
           d[j++] = desp.options[i].value;
        }
    }

    dados = {'despesas':d};
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+total).val(retorno['total']);
          $("#"+descricao).val(retorno['desc']);
      },
      error: function(erro) {
        alert('Erro: Sem valor.');
      }
  });
}



function ajax_gera_despesas_internas(url, objHtmlReturn, pagina, select, auditoria, pag)
{
    dados = {'id':select, 'ai':auditoria, 'pagina':pag};

    $("#"+objHtmlReturn).html('<select multiple>');
    $("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+objHtmlReturn).empty();
          $.each(retorno['fp'], function(i, item){
              $("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+pagina).val(retorno['pag']);
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
    });
    $("#"+objHtmlReturn).html('</select>');
}



function ajax_gera_despesas_fapesp(url, objHtmlReturn, parcial, pagina, select, auditoria, parc, pag, t)
{
    select_termo = document.getElementById(t);
    termo = select_termo.options[select_termo.selectedIndex].value;

    dados = {'modalidade':select, 'af':auditoria, 'parcial': parc, 'pagina':pag, 'termo':termo};

    $("#"+objHtmlReturn).html('<select multiple>');
    $("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+objHtmlReturn).empty();
          $.each(retorno['fp'], function(i, item){
              $("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+parcial).val(retorno['parcial']);
          $("#"+pagina).val(retorno['pagina']);
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
    });
    $("#"+objHtmlReturn).html('</select>');
}


/*
function ajax_proxima_parcial(url, parcial, pagina, select)
{
    var id=new Array();
    id[0] = select;

    dados = {'fontepagadora': id};
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+parcial).val(retorno['parcial']);
          $("#"+pagina).val(retorno['pagina']);
      },
      error: function(erro) {
        alert('Erro: Sem valor.');
      }
  });
}
*/


function ajax_filter(url, objHtmlReturn, id)
{
    dados = {'id':id};
//    $("#"+objHtmlReturn).html('<option value="0">Carregando...</option>');
    $("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+objHtmlReturn).empty();
          $("#"+objHtmlReturn).append('<option value="">------------</option>');
          $.each(retorno, function(i, item){
              $("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>'); 
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}



function ajax_filter2(url, objHtmlReturn, id, objHtmlPrevious)
{
    previous = $("#"+objHtmlPrevious).val();
    dados = {'id':id, 'previous':previous};

//    $("#"+objHtmlReturn).html('<option value="0">Carregando...</option>');
    $("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+objHtmlReturn).empty();
//          $("#"+objHtmlReturn).append('<option value="0">------------</option>'); 
          $("#"+objHtmlReturn).append('<option value="">------------</option>');
          $.each(retorno, function(i, item){
              $("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>'); 
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}



function ajax_seleciona_extrato(url, objHtmlReturn, id, previous)
{
    dados = {'id':id, 'previous': previous};
    alert(dados['id']);

    $("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+objHtmlReturn).empty();
          $("#"+objHtmlReturn).append('<option value="">------------</option>');
          $.each(retorno, function(i, item){
              $("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}



function ajax_filter_inline(url, id, name)
{

    n = name.split("modalidade");
    termo = n[0] + 'termo'
    item_outorga = n[0] + 'item_outorga'


    previous = $("#"+termo).val();
    dados = {'id':id, 'previous':previous};

//    $("#"+item_outorga).html('<option value="0">Carregando...</option>');
    $("#"+item_outorga).html('<option value="">Carregando...</option>');

    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+item_outorga).empty();
//          $("#"+item_outorga).append('<option value="0">------------</option>');
          $("#"+item_outorga).append('<option value="">------------</option>');
          $.each(retorno, function(i, item){
              $("#"+item_outorga).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}



function ajax_filter_item_natureza(url, termo, item_anterior, natureza, id, name)
{

    n = name.split("modalidade");

    termo = n[0] + termo
    item_anterior = n[0] + item_anterior
    natureza = n[0] + natureza

    previous = $("#"+termo).val();
    dados = {'id':id, 'previous':previous};

//    $("#"+item_anterior).html('<option value="0">Carregando...</option>');
//    $("#"+natureza).html('<option value="0">Carregando...</option>');
    $("#"+item_anterior).html('<option value="">Carregando...</option>');
    $("#"+natureza).html('<option value="">Carregando...</option>');

    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+item_anterior).empty();
//          $("#"+item_anterior).append('<option value="0">------------</option>');
          $("#"+item_anterior).append('<option value="">------------</option>');
          $.each(retorno['item'], function(i, item){
              $("#"+item_anterior).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+natureza).empty();
//          $("#"+natureza).append('<option value="0">------------</option>');
          $("#"+natureza).append('<option value="">------------</option>');
          $.each(retorno['natureza'], function(i, item){
              $("#"+natureza).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}



function ajax_filter_mod_item_natureza(url, modalidade, item_anterior, natureza, id, name)
{

    dados = {'id':id};

    n = name.split("termo");

    modalidade = n[0] + modalidade
    item_anterior = n[0] + item_anterior
    natureza = n[0] + natureza

//    $("#"+modalidade).html('<option value="0">Carregando...</option>');
//    $("#"+item_anterior).html('<option value="0">Carregando...</option>');
//    $("#"+natureza).html('<option value="0">Carregando...</option>');

    $("#"+modalidade).html('<option value="">Carregando...</option>');
    $("#"+item_anterior).html('<option value="">Carregando...</option>');
    $("#"+natureza).html('<option value="">Carregando...</option>');


    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+modalidade).empty();
//          $("#"+modalidade).append('<option value="0">------------</option>');
          $("#"+modalidade).append('<option value="">------------</option>');
          $.each(retorno['modalidade'], function(i, item){
              $("#"+modalidade).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+item_anterior).empty();
//          $("#"+item_anterior).append('<option value="0">------------</option>');
          $("#"+item_anterior).append('<option value="">------------</option>');
          $.each(retorno['item'], function(i, item){
              $("#"+item_anterior).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+natureza).empty();
//          $("#"+natureza).append('<option value="0">------------</option>');
          $("#"+natureza).append('<option value="">------------</option>');
          $.each(retorno['natureza'], function(i, item){
              $("#"+natureza).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
      },
      
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });

}



function ajax_filter_modalidade_item_inline(url, id, name)
{
    dados = {'id':id};

    n = name.split("termo");

    modalidade = n[0] + 'modalidade'
    item_outorga = n[0] + 'item_outorga' 

//    $("#"+modalidade).html('<option value="0">Carregando...</option>');
//    $("#"+item_outorga).html('<option value="0">Carregando...</option>');

    $("#"+modalidade).html('<option value="">Carregando...</option>');
    $("#"+item_outorga).html('<option value="">Carregando...</option>');


    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+modalidade).empty();
//          $("#"+modalidade).append('<option value="0">------------</option>');
          $("#"+modalidade).append('<option value="">------------</option>');
          $.each(retorno['modalidade'], function(i, item){
              $("#"+modalidade).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+item_outorga).empty();
//          $("#"+item_outorga).append('<option value="0">------------</option>');
          $("#"+item_outorga).append('<option value="">------------</option>');
          $.each(retorno['item'], function(i, item){
              $("#"+item_outorga).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}

function ajax_filter_termo_natureza(url, natureza, id, name)
{

    dados = {'id':id};

    n = name.split("termo");

    natureza = n[0] + natureza

    $("#"+natureza).html('<option value="">Carregando...</option>');

    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+natureza).empty();
          $("#"+natureza).append('<option value="">------------</option>');
          $.each(retorno, function(i, item){
              $("#"+natureza).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
      },
      
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });

}

function ajax_filtra_item(url, item_pedido, modalidade, termo, select)
{

    dados = {'protocolo': select};
//    $("#"+item_pedido).html('<option value="0">Carregando...</option>');
//    $("#"+modalidade).html('<option value="0">Carregando...</option>');

    $("#"+item_pedido).html('<option value="">Carregando...</option>');
    $("#"+modalidade).html('<option value="">Carregando...</option>');

    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+item_pedido).empty();
//          $("#"+item_pedido).append('<option value="0">------------</option>');
          $("#"+item_pedido).append('<option value="">------------</option>');
          $.each(retorno['itens'], function(i, item){
              $("#"+item_pedido).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+modalidade).empty();
//          $("#"+modalidade).append('<option value="0">------------</option>');
          $("#"+modalidade).append('<option value="">------------</option>');
          $.each(retorno['modalidades'], function(i, item){
              $("#"+modalidade).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          $("#"+termo).val(retorno['termo']);

      },
      error: function(erro) {
        alert('Erro: Sem retorno da requisição.');
      }
  });
}

function ajax_filter_origem_protocolo(termo_campo, termo)
{
      dados_campo = termo_campo.split('-');
      if (dados_campo.length > 1) {
	indice = dados_campo[1];
	nomes = "#id_pagamento_set-"+indice+"-";
      }
      else {
	nomes = "#id_";
      }
      $(nomes+"protocolo").html('<option value="">Carregando...</option>');
      $(nomes+"origem_fapesp").html('<option value="">Carregando...</option>');

      $.ajax({
	  type: "POST",
	  url: "/financeiro/pagamento_termo",
	  dataType: "json",
	  data: {'termo_id':termo},
	  success: function(retorno) {
	      $(nomes+"protocolo").empty();
	      $(nomes+"protocolo").append('<option value="">---------</option>');
	      $.each(retorno['protocolos'], function(i, item){
		  $(nomes+"protocolo").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	      $(nomes+"origem_fapesp").empty();
	      $(nomes+"origem_fapesp").append('<option value="">------------</option>');
	      $.each(retorno['origens'], function(i, item){
		  $(nomes+"origem_fapesp").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	    alert('Erro: Sem retorno da requisição.');
	  }
      });
/*      if (!$("#id_auditoria_set-0-pagina").val()){
       $.ajax({
	  type: "POST",
	  url: "/financeiro/parcial_pagina_termo",
	  dataType: "json",
	  data: {'termo_id':termo},
	  success: function(retorno) {
	      $("#id_auditoria_set-0-parcial").val(retorno['parcial']);
	      $("#id_auditoria_set-0-pagina").val(retorno['pagina']);
	  },
	  error: function(erro) {
	    alert('Erro: Sem retorno da requisição.');
	  }
       });
      }*/
}

function ajax_filter_protocolo_numero(numero)
{
      $("#id_protocolo").html('<option value="">Carregando...</option>');
      termo = $("#id_termo").val()

      $.ajax({
	  type: "POST",
	  url: "/financeiro/pagamento_numero",
	  dataType: "json",
	  data: {'termo_id':termo, 'numero':numero},
	  success: function(retorno) {
	      $("#id_protocolo").empty();
	      $("#id_protocolo").append('<option value="">--------</option>');
	      $.each(retorno['protocolos'], function(i, item){
		  $("#id_protocolo").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	    alert('Erro: Sem retorno da requisição.');
	  }
      });
}

function ajax_filter_cc_cod(codigo)
{
      $("#id_conta_corrente").html('<option value="">Carregando...</option>');

      $.ajax({
      	  type: "POST",
	  url: "/financeiro/pagamento_cc",
	  dataType: "json",
	  data: {'codigo':codigo},
	  success: function(retorno) {
	      $("#id_conta_corrente").empty();
	      $("#id_conta_corrente").append('<option value="">--------</option>');
	      $.each(retorno['ccs'], function(i, item){
	      	  $("#id_conta_corrente").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	     alert('Erro: Sem retorno de requisição.');
	  }
       });
}

function ajax_filter_pagamentos(url, numero)
{
      $("#id_pagamento").html('<option value="">Carregando...</option>');
      termo = $("#id_termo").val()
      $.ajax({
      	  type: "POST",
	  url: url,
	  dataType: "json",
	  data: {'numero':numero, 'termo':termo},
	  success: function(retorno) {
	      $("#id_pagamento").empty();
	      $("#id_pagamento").append('<option value="">--------</option>');
	      $.each(retorno, function(i, item){
	      	  $("#id_pagamento").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	     alert('Erro: Sem retorno de requisição.');
	  }
       });
	
}

function ajax_filter_financeiro(termo_id)
{
       $("#id_extrato_financeiro").html('<option value="">Carregando...</option>');
       $.ajax({
       	   type: "POST",
	   url: "/financeiro/sel_extrato",
	   dataType: "json",
	   data: {'termo':termo_id},
	   success: function(retorno) {
	   	$("#id_extrato_financeiro").empty();
		$("#id_extrato_financeiro").append('<option value="">--------</option>');
		$.each(retorno, function(i, item){
		    $("#id_extrato_financeiro").append('<option value="'+item.pk+'">'+item.valor+'</option>');
		});
	   },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });
}

function ajax_select_endereco(id_field)
{
       
       entidade = $("#"+id_field).val();
       partes = id_field.split("-");
       e_id = "#id_historicolocal_set-"+partes[1]+"-endereco";
       $(e_id).html('<option value="">Carregando...</option>');
       $.ajax({
       	   type: "POST",
	   url: "/patrimonio/escolhe_entidade",
	   dataType: "json",
	   data: {'entidade':entidade},
	   success: function(retorno) {
	        $(e_id).empty();
		$(e_id).append('<option value="">--------</option>');
		$.each(retorno, function(i, item){
		    $(e_id).append('<option value="'+item.pk+'">'+item.valor+'</option>');
		});	   
	   },
	   error: function(erro) {
	      alert('Erro: Sem retorno de requisição.');
	   }
       });
}

function ajax_select_endereco2()
{
       entidade = $("#id_entidade").val();
       e_id = "#id_endereco";
       $(e_id).html('<option value="">Carregando...</option>');
       $.ajax({
           type: "POST",
           url: "/identificacao/escolhe_entidade",
           dataType: "json",
           data: {'entidade':entidade},
           success: function(retorno) {
                $(e_id).empty();
                $(e_id).append('<option value="">--------</option>');
                $.each(retorno, function(i, item){
                    $(e_id).append('<option value="'+item.pk+'">'+item.valor+'</option>');
                });
           },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });

}


function ajax_patrimonio_existente(pn)
{
       $.ajax({
           type: "POST",
	   url: "/patrimonio/patrimonio_existente",
	   dataType: "json",
	   data: {'part_number':pn},
	   success: function(retorno) {
	      if (retorno.marca) {
	         $("#id_marca").val(retorno.marca);
	         $("#id_modelo").val(retorno.modelo);
	         $("#id_descricao").val(retorno.descricao);
	         $("#id_procedencia").val(retorno.procedencia);
	      }
	   },
	   error: function(erro) {
	      alert('Erro: Sem retonro de requisição.');
	   }
       });
}


function ajax_filter_enderecos(id_ent) {
     ent_id = $("#"+id_ent).val();
     $("#id_endereco").html('<option value="0">Carregando...</option>');

     $.ajax({
       type: "POST",
       url: "/identificacao/escolhe_entidade_filhos",
       dataType: "json",
       data: {'entidade': ent_id},
       success: function(retorno){
          $("#id_endereco").empty();
          $("#id_endereco").append('<option value="">------------</option>');
          $.each(retorno['enderecos'], function(i, item){
              $("#id_endereco").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
          if (retorno['filhos'].length > 0) {
              $("#id_entidade1").empty();
    	      $("#id_entidade1").append('<option value="">-----------</option>');
              $.each(retorno['filhos'], function(i, item){
	          $("#id_entidade1").append('<option value="'+item.pk+'">'+item.valor+'</option>');
              });
              $("#filhos").show();
          }
          else if (id_ent == 'id_entidade') {
              $("#filhos").hide();
          }
       },
     });
} 

function ajax_filter_locais() {
     end_id = $("#id_endereco").val();
     $("#id_detalhe").html('<option value="0">Carregando...</option>');

     $.ajax({
       type: "POST",
       url: "/identificacao/escolhe_endereco",
       dataType: "json",
       data: {'endereco': end_id},
       success: function(retorno){
          $("#id_detalhe").empty();
          $("#id_detalhe").append('<option value="">------------</option>');
          $.each(retorno, function(i, item){
              $("#id_detalhe").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
       },
     });
}

function ajax_filter_nivel(nivel, ed_id) {
     $("#id_detalhe_"+nivel).html('<option value="0">Carregando</option>');

     $.ajax({
       type: "POST",
       url: "/patrimonio/escolhe_detalhe",
       dataType: "json",
       data: {'detalhe': ed_id},
       success: function(retorno){
          $("#id_detalhe_"+nivel).empty();
          $("#id_detalhe_"+nivel).append('<option value="">------------</option>');
          $.each(retorno, function(i, item){
              $("#id_detalhe_"+nivel).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

       },
     });
}
    
function ajax_filter_pagamentos_memorando(termo)
{
     n = parseInt($("#id_corpo_set-TOTAL_FORMS").val());
     for(j=0;j<n;j++){
        $("#id_corpo_set-"+j+"-pagamento_from").empty();
     }
     $.ajax({
       type: "POST",
       url: "/memorando/pagamentos",
       dataType: "json",
       data: {'termo':termo},
       success: function(retorno) {
          for(j=0;j<n;j++){
             SelectBox.cache["id_corpo_set-"+j+"-pagamento_from"] = new Array();
          }
          $("#id_corpo_set-__prefix__-pagamento_from").empty();
          $.each(retorno, function(i, item){
              for(j=0;j<n;j++){
                 var opt = new Object ({value:item.pk, text:item.valor});
                 SelectBox.add_to_cache("id_corpo_set-"+j+"-pagamento_from", opt);
              }
              $("#id_corpo_set-__prefix__-pagamento_from").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
          for(j=0;j<n;j++){
             SelectBox.redisplay("id_corpo_set-"+j+"-pagamento_from");
          }
       },
       error: function(erro) {
         alert('Erro. Sem retorno da requisicao.');
       }
     });
}

function ajax_init_pagamentos()
{
   termo = $("#id_termo").val();
   if (termo) {
     $.ajax({
       type: "POST",
       url: "/memorando/pagamentos",
       dataType: "json",
       data: {'termo':termo},
       success: function(retorno) {
          $("#id_corpo_set-__prefix__-pagamento_from").empty();
          $.each(retorno, function(i, item){
              $("#id_corpo_set-__prefix__-pagamento_from").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
       },
       error: function(erro) {
         alert('Erro. Sem retorno da requisicao.');
       }
     });
  }
}

function ajax_filter_perguntas(memorando)
{
   n = parseInt($("#id_corpo_set-TOTAL_FORMS").val());
   for(j=0;j<n;j++){
        $("#id_corpo_set-"+j+"-pergunta").empty();
   }

   $.ajax({
       type: "POST",
       url: "/memorando/perguntas",
       dataType: "json",
       data: {'memorando':memorando},
       success: function(retorno) {
          $.each(retorno, function(i, item){
              for(j=0;j<n;j++){
                $("#id_corpo_set-"+j+"-pergunta").append('<option value="'+item.pk+'">'+item.valor+'</option>');
              }
              $("#id_corpo_set-__prefix__-pergunta").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
       },
       error: function(erro) {
         alert('Erro. Sem retorno da requisicao.');
       }
   });
}

function ajax_select_pergunta(id_field)
{

       pergunta = $("#"+id_field).val();
       partes = id_field.split("-");
       e_id = "#id_corpo_set-"+partes[1]+"-perg";
       $(e_id).html('Carregando...');
       $.ajax({
           type: "POST",
           url: "/memorando/escolhe_pergunta",
           dataType: "json",
           data: {'pergunta':pergunta},
           success: function(retorno) {
                $(e_id).empty();
                $(e_id).html(retorno);
           },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });
}

$(window).load(function () {
    ajax_init_pagamentos();
});	

function ajax_filter_pagamentos2(url)
{
      termo = $("#id_termo").val()
      $.ajax({
          type: "POST",
          url: url,
          dataType: "json",
          data: {'termo':termo},
          success: function(retorno) {
              $("#id_pagamento").empty();
              $("#id_pagamento").append('<option value="">-----</option>');
              $.each(retorno, function(i, item){
                  $("#id_pagamento").append('<option value="'+item.pk+'">'+item.valor+'</option>');
              });
          },
          error: function(erro) {
             alert('Erro: Sem retorno de requisição.');
          }
       });

}
function ajax_filter_equipamento(num_doc, id_patrimonio, id_equipamento)
{
       p_id = "#id_equipamento";
       $(p_id).html('Carregando...');
       $.ajax({
           type: "POST",
           url: "/patrimonio/escolhe_equipamento",
           dataType: "json",
           data: {'num_doc':num_doc, 'id_patrimonio':id_patrimonio, 'id_equipamento':id_equipamento},
           success: function(retorno) {
              $(p_id).empty();
              $(p_id).append('<option value="">-----</option>');
              $.each(retorno, function(i, item){
            	  if (item.selected) {
                      $(p_id).append('<option value="'+item.pk+'" selected>'+ item.valor+'</option>');
            	  } else {
            		  $(p_id).append('<option value="'+item.pk+'">'+item.valor+'</option>');
            	  }
              });
           },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });
}

function ajax_filter_patrimonio(num_doc)
{
       p_id = "#id_patrimonio";
       $(p_id).html('Carregando...');
       $.ajax({
           type: "POST",
           url: "/patrimonio/escolhe_patrimonio",
           dataType: "json",
           data: {'num_doc':num_doc},
           success: function(retorno) {
              $(p_id).empty();
              $(p_id).append('<option value="">-----</option>');
              $.each(retorno, function(i, item){
                  $(p_id).append('<option value="'+item.pk+'">'+item.valor+'</option>');
              });
           },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });
}

function ajax_prox_audit(origem)
{
      if (!$("#id_auditoria_set-0-pagina").val()){
       $.ajax({
          type: "POST",
          url: "/financeiro/parcial_pagina_termo",
          dataType: "json",
          data: {'orig_id':origem},
          success: function(retorno) {
              $("#id_auditoria_set-0-parcial").val(retorno['parcial']);
              $("#id_auditoria_set-0-pagina").val(retorno['pagina']);
          },
          error: function(erro) {
            alert('Erro: Sem retorno da requisição.');
          }
       });
      }
}

function ajax_nova_pagina(parcial)
{
    $.ajax({
       type:"POST",
       url:"/financeiro/nova_pagina",
       dataType:"json",
       data: {'orig_id':$("#id_origem_fapesp").val(), 'parcial':parcial.value},
       success: function(retorno){
           numero = parcial.id.split("-")[1];
           $("#id_auditoria_set-"+numero+"-pagina").val(retorno);
       }
    });
}

function ajax_select_ano_proj()
{
       anoproj = $("#id_anoproj").val();
       partes = anoproj.split("/");
       ano = partes[0];
       proj_id = partes[1];
       $("#id_os").html('Carregando...');
       $.ajax({
           type: "POST",
           url: "/rede/planeja_contrato",
           dataType: "json",
           data: {'ano':ano, 'proj_id':proj_id},
           success: function(retorno) {
                $("#id_os").html('<option value="">Nenhum</option>');
	            $.each(retorno.oss, function(i, item){
                     $("#id_os").append('<option value="'+item.pk+'">'+item.valor+'</option>');
 	            });
	   },
	   error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });

}


function ajax_patrimonio_historico(patr_id)
{
	django.jQuery.ajax({
		type: "GET",
		url: "/patrimonio/patrimonio_historico",
		dataType: "json",
		data: {'id':patr_id},
		success: function(retorno) {
			// N. total de forms de historicos historicolocal_set-TOTAL_FORMS
			// O form vazio deve ser o de indice = total - 1
			var total_forms = $('#id_historicolocal_set-TOTAL_FORMS').val();

			form_index = total_forms - 1;

			// Entidade
			if (retorno.entidade_id != '') { 
					$("#id_historicolocal_set-"+form_index+"-entidade option[value='"+retorno.entidade_id+"']").attr("selected","selected");
			} else {
				$("#id_historicolocal_set-"+form_index+"-entidade option")[0].selected = true;
			}
			
			// Endereco
			// É necessário limpar o select, pois ele é recarregado sempre que se muda a entidade
			$("#id_historicolocal_set-"+form_index+"-endereco").empty();
			$("#id_historicolocal_set-"+form_index+"-endereco")
	    		.append('<option value="'+ retorno.localizacao_id +'">'+ retorno.localizacao_desc +'</option>');
			
			// Estado
			if (retorno.estado_id != '') { 
				$("#id_historicolocal_set-"+form_index+"-estado option[value='"+ retorno.estado_id +"']").attr("selected","selected");
			} else {
				$("#id_historicolocal_set-"+form_index+"-estado option")[0].selected = true;
			}
			
			// Memorando
			if (retorno.memorando_id && retorno.memorando_id != '') { 
				$("#id_historicolocal_set-"+form_index+"-memorando option[value='"+ retorno.memorando_id +"']").attr("selected","selected");
			} else {
				$("#id_historicolocal_set-"+form_index+"-memorando option")[0].selected = true;
			}
			
			// Campos textos: posição, descrição e data
			$("#id_historicolocal_set-"+form_index+"-posicao").val(retorno.posicao);
			$("#id_historicolocal_set-"+form_index+"-descricao").val(retorno.descricao);
			$("#id_historicolocal_set-"+form_index+"-data").val(retorno.data);
		},
	});
}


function ajax_patr_form_get_equipamento(id_equipamento)
{
       p_id = "#id_equipamento";
       $.ajax({
           type: "POST",
           url: "/patrimonio/ajax_get_equipamento",
           dataType: "json",
           data: {'id_equipamento':id_equipamento},
           success: function(retorno) {
        	   $('#id_modelo').html(retorno.modelo);
        	   $('#id_part_number').text(retorno.part_number);
        	   $('#id_ean').text(retorno.ean);
           },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });
}

