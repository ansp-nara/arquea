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
    filter_text = filter_by_ctrl.options[filter_by_ctrl.selectedIndex].text.replace(/^\s+|\s+django.jQuery/g,"");
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
    filter2_text = filter2_by_ctrl.options[filter2_by_ctrl.selectedIndex].text.replace(/^\s+|\s+django.jQuery/g,"");
    filter1_text = filter1_by_ctrl.options[filter1_by_ctrl.selectedIndex].text.split(" - ")[0]
    filter1_text = filter1_text.replace(/^\s+|\s+django.jQuery/g,"");
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
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+objHtmlReturn).val(retorno);
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
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+total).val(retorno['total']);
          django.jQuery("#"+descricao).val(retorno['desc']);
      },
      error: function(erro) {
        alert('Erro: Sem valor.');
      }
  });
}



function ajax_gera_despesas_internas(url, objHtmlReturn, pagina, select, auditoria, pag)
{
    dados = {'id':select, 'ai':auditoria, 'pagina':pag};

    django.jQuery("#"+objHtmlReturn).html('<select multiple>');
    django.jQuery("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+objHtmlReturn).empty();
          django.jQuery.each(retorno['fp'], function(i, item){
              django.jQuery("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+pagina).val(retorno['pag']);
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
    });
    django.jQuery("#"+objHtmlReturn).html('</select>');
}



function ajax_gera_despesas_fapesp(url, objHtmlReturn, parcial, pagina, select, auditoria, parc, pag, t)
{
    select_termo = document.getElementById(t);
    termo = select_termo.options[select_termo.selectedIndex].value;

    dados = {'modalidade':select, 'af':auditoria, 'parcial': parc, 'pagina':pag, 'termo':termo};

    django.jQuery("#"+objHtmlReturn).html('<select multiple>');
    django.jQuery("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+objHtmlReturn).empty();
          django.jQuery.each(retorno['fp'], function(i, item){
              django.jQuery("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+parcial).val(retorno['parcial']);
          django.jQuery("#"+pagina).val(retorno['pagina']);
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
    });
    django.jQuery("#"+objHtmlReturn).html('</select>');
}


/*
function ajax_proxima_parcial(url, parcial, pagina, select)
{
    var id=new Array();
    id[0] = select;

    dados = {'fontepagadora': id};
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+parcial).val(retorno['parcial']);
          django.jQuery("#"+pagina).val(retorno['pagina']);
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
//    django.jQuery("#"+objHtmlReturn).html('<option value="0">Carregando...</option>');
    django.jQuery("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+objHtmlReturn).empty();
          django.jQuery("#"+objHtmlReturn).append('<option value="">------------</option>');
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>'); 
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}



function ajax_filter2(url, objHtmlReturn, id, objHtmlPrevious)
{
    previous = django.jQuery("#"+objHtmlPrevious).val();
    dados = {'id':id, 'previous':previous};

//    django.jQuery("#"+objHtmlReturn).html('<option value="0">Carregando...</option>');
    django.jQuery("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+objHtmlReturn).empty();
//          django.jQuery("#"+objHtmlReturn).append('<option value="0">------------</option>'); 
          django.jQuery("#"+objHtmlReturn).append('<option value="">------------</option>');
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>'); 
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

    django.jQuery("#"+objHtmlReturn).html('<option value="">Carregando...</option>');
    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+objHtmlReturn).empty();
          django.jQuery("#"+objHtmlReturn).append('<option value="">------------</option>');
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.valor+'</option>');
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


    previous = django.jQuery("#"+termo).val();
    dados = {'id':id, 'previous':previous};

//    django.jQuery("#"+item_outorga).html('<option value="0">Carregando...</option>');
    django.jQuery("#"+item_outorga).html('<option value="">Carregando...</option>');

    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+item_outorga).empty();
//          django.jQuery("#"+item_outorga).append('<option value="0">------------</option>');
          django.jQuery("#"+item_outorga).append('<option value="">------------</option>');
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#"+item_outorga).append('<option value="'+item.pk+'">'+item.valor+'</option>');
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

    previous = django.jQuery("#"+termo).val();
    dados = {'id':id, 'previous':previous};

//    django.jQuery("#"+item_anterior).html('<option value="0">Carregando...</option>');
//    django.jQuery("#"+natureza).html('<option value="0">Carregando...</option>');
    django.jQuery("#"+item_anterior).html('<option value="">Carregando...</option>');
    django.jQuery("#"+natureza).html('<option value="">Carregando...</option>');

    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+item_anterior).empty();
//          django.jQuery("#"+item_anterior).append('<option value="0">------------</option>');
          django.jQuery("#"+item_anterior).append('<option value="">------------</option>');
          django.jQuery.each(retorno['item'], function(i, item){
              django.jQuery("#"+item_anterior).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+natureza).empty();
//          django.jQuery("#"+natureza).append('<option value="0">------------</option>');
          django.jQuery("#"+natureza).append('<option value="">------------</option>');
          django.jQuery.each(retorno['natureza'], function(i, item){
              django.jQuery("#"+natureza).append('<option value="'+item.pk+'">'+item.valor+'</option>');
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

//    django.jQuery("#"+modalidade).html('<option value="0">Carregando...</option>');
//    django.jQuery("#"+item_anterior).html('<option value="0">Carregando...</option>');
//    django.jQuery("#"+natureza).html('<option value="0">Carregando...</option>');

    django.jQuery("#"+modalidade).html('<option value="">Carregando...</option>');
    django.jQuery("#"+item_anterior).html('<option value="">Carregando...</option>');
    django.jQuery("#"+natureza).html('<option value="">Carregando...</option>');


    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+modalidade).empty();
//          django.jQuery("#"+modalidade).append('<option value="0">------------</option>');
          django.jQuery("#"+modalidade).append('<option value="">------------</option>');
          django.jQuery.each(retorno['modalidade'], function(i, item){
              django.jQuery("#"+modalidade).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+item_anterior).empty();
//          django.jQuery("#"+item_anterior).append('<option value="0">------------</option>');
          django.jQuery("#"+item_anterior).append('<option value="">------------</option>');
          django.jQuery.each(retorno['item'], function(i, item){
              django.jQuery("#"+item_anterior).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+natureza).empty();
//          django.jQuery("#"+natureza).append('<option value="0">------------</option>');
          django.jQuery("#"+natureza).append('<option value="">------------</option>');
          django.jQuery.each(retorno['natureza'], function(i, item){
              django.jQuery("#"+natureza).append('<option value="'+item.pk+'">'+item.valor+'</option>');
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

//    django.jQuery("#"+modalidade).html('<option value="0">Carregando...</option>');
//    django.jQuery("#"+item_outorga).html('<option value="0">Carregando...</option>');

    django.jQuery("#"+modalidade).html('<option value="">Carregando...</option>');
    django.jQuery("#"+item_outorga).html('<option value="">Carregando...</option>');


    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+modalidade).empty();
//          django.jQuery("#"+modalidade).append('<option value="0">------------</option>');
          django.jQuery("#"+modalidade).append('<option value="">------------</option>');
          django.jQuery.each(retorno['modalidade'], function(i, item){
              django.jQuery("#"+modalidade).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+item_outorga).empty();
//          django.jQuery("#"+item_outorga).append('<option value="0">------------</option>');
          django.jQuery("#"+item_outorga).append('<option value="">------------</option>');
          django.jQuery.each(retorno['item'], function(i, item){
              django.jQuery("#"+item_outorga).append('<option value="'+item.pk+'">'+item.valor+'</option>');
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

    django.jQuery("#"+natureza).html('<option value="">Carregando...</option>');

    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+natureza).empty();
          django.jQuery("#"+natureza).append('<option value="">------------</option>');
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#"+natureza).append('<option value="'+item.pk+'">'+item.valor+'</option>');
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
//    django.jQuery("#"+item_pedido).html('<option value="0">Carregando...</option>');
//    django.jQuery("#"+modalidade).html('<option value="0">Carregando...</option>');

    django.jQuery("#"+item_pedido).html('<option value="">Carregando...</option>');
    django.jQuery("#"+modalidade).html('<option value="">Carregando...</option>');

    django.jQuery.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          django.jQuery("#"+item_pedido).empty();
//          django.jQuery("#"+item_pedido).append('<option value="0">------------</option>');
          django.jQuery("#"+item_pedido).append('<option value="">------------</option>');
          django.jQuery.each(retorno['itens'], function(i, item){
              django.jQuery("#"+item_pedido).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+modalidade).empty();
//          django.jQuery("#"+modalidade).append('<option value="0">------------</option>');
          django.jQuery("#"+modalidade).append('<option value="">------------</option>');
          django.jQuery.each(retorno['modalidades'], function(i, item){
              django.jQuery("#"+modalidade).append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });

          django.jQuery("#"+termo).val(retorno['termo']);

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
      django.jQuery(nomes+"protocolo").html('<option value="">Carregando...</option>');
      django.jQuery(nomes+"origem_fapesp").html('<option value="">Carregando...</option>');

      django.jQuery.ajax({
	  type: "POST",
	  url: "/financeiro/pagamento_termo",
	  dataType: "json",
	  data: {'termo_id':termo},
	  success: function(retorno) {
	      django.jQuery(nomes+"protocolo").empty();
	      django.jQuery(nomes+"protocolo").append('<option value="">---------</option>');
	      django.jQuery.each(retorno['protocolos'], function(i, item){
		  django.jQuery(nomes+"protocolo").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	      django.jQuery(nomes+"origem_fapesp").empty();
	      django.jQuery(nomes+"origem_fapesp").append('<option value="">------------</option>');
	      django.jQuery.each(retorno['origens'], function(i, item){
		  django.jQuery(nomes+"origem_fapesp").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	    alert('Erro: Sem retorno da requisição.');
	  }
      });
      if (!django.jQuery("#id_auditoria_set-0-pagina").val()){
       django.jQuery.ajax({
	  type: "POST",
	  url: "/financeiro/parcial_pagina_termo",
	  dataType: "json",
	  data: {'termo_id':termo},
	  success: function(retorno) {
	      django.jQuery("#id_auditoria_set-0-parcial").val(retorno['parcial']);
	      django.jQuery("#id_auditoria_set-0-pagina").val(retorno['pagina']);
	  },
	  error: function(erro) {
	    alert('Erro: Sem retorno da requisição.');
	  }
       });
      }
}

function ajax_filter_protocolo_numero(numero)
{
      django.jQuery("#id_protocolo").html('<option value="">Carregando...</option>');
      termo = django.jQuery("#id_termo").val()

      django.jQuery.ajax({
	  type: "POST",
	  url: "/financeiro/pagamento_numero",
	  dataType: "json",
	  data: {'termo_id':termo, 'numero':numero},
	  success: function(retorno) {
	      django.jQuery("#id_protocolo").empty();
	      django.jQuery("#id_protocolo").append('<option value="">--------</option>');
	      django.jQuery.each(retorno['protocolos'], function(i, item){
		  django.jQuery("#id_protocolo").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	    alert('Erro: Sem retorno da requisição.');
	  }
      });
}

function ajax_filter_cc_cod(codigo)
{
      django.jQuery("#id_conta_corrente").html('<option value="">Carregando...</option>');

      django.jQuery.ajax({
      	  type: "POST",
	  url: "/financeiro/pagamento_cc",
	  dataType: "json",
	  data: {'codigo':codigo},
	  success: function(retorno) {
	      django.jQuery("#id_conta_corrente").empty();
	      django.jQuery("#id_conta_corrente").append('<option value="">--------</option>');
	      django.jQuery.each(retorno['ccs'], function(i, item){
	      	  django.jQuery("#id_conta_corrente").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	     alert('Erro: Sem retorno de requisição.');
	  }
       });
}

function ajax_filter_pagamentos(url, numero)
{
      django.jQuery("#id_pagamento").html('<option value="">Carregando...</option>');
      termo = django.jQuery("#id_termo").val()
      django.jQuery.ajax({
      	  type: "POST",
	  url: url,
	  dataType: "json",
	  data: {'numero':numero, 'termo':termo},
	  success: function(retorno) {
	      django.jQuery("#id_pagamento").empty();
	      django.jQuery("#id_pagamento").append('<option value="">--------</option>');
	      django.jQuery.each(retorno, function(i, item){
	      	  django.jQuery("#id_pagamento").append('<option value="'+item.pk+'">'+item.valor+'</option>');
	      });
	  },
	  error: function(erro) {
	     alert('Erro: Sem retorno de requisição.');
	  }
       });
	
}

function ajax_filter_financeiro(termo_id)
{
       django.jQuery("#id_extrato_financeiro").html('<option value="">Carregando...</option>');
       django.jQuery.ajax({
       	   type: "POST",
	   url: "/financeiro/sel_extrato",
	   dataType: "json",
	   data: {'termo':termo_id},
	   success: function(retorno) {
	   	django.jQuery("#id_extrato_financeiro").empty();
		django.jQuery("#id_extrato_financeiro").append('<option value="">--------</option>');
		django.jQuery.each(retorno, function(i, item){
		    django.jQuery("#id_extrato_financeiro").append('<option value="'+item.pk+'">'+item.valor+'</option>');
		});
	   },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });
}

function ajax_select_endereco(id_field)
{
       
       entidade = django.jQuery("#"+id_field).val();
       partes = id_field.split("-");
       e_id = "#id_historicolocal_set-"+partes[1]+"-endereco";
       django.jQuery(e_id).html('<option value="">Carregando...</option>');
       django.jQuery.ajax({
       	   type: "POST",
	   url: "/patrimonio/escolhe_entidade",
	   dataType: "json",
	   data: {'entidade':entidade},
	   success: function(retorno) {
	        django.jQuery(e_id).empty();
		django.jQuery(e_id).append('<option value="">--------</option>');
		django.jQuery.each(retorno, function(i, item){
		    django.jQuery(e_id).append('<option value="'+item.pk+'">'+item.valor+'</option>');
		});	   
	   },
	   error: function(erro) {
	      alert('Erro: Sem retorno de requisição.');
	   }
       });
}

function ajax_select_endereco2()
{
       entidade = django.jQuery("#id_entidade").val();
       e_id = "#id_endereco";
       django.jQuery(e_id).html('<option value="">Carregando...</option>');
       django.jQuery.ajax({
           type: "POST",
           url: "/identificacao/escolhe_entidade",
           dataType: "json",
           data: {'entidade':entidade},
           success: function(retorno) {
                django.jQuery(e_id).empty();
                django.jQuery(e_id).append('<option value="">--------</option>');
                django.jQuery.each(retorno, function(i, item){
                    django.jQuery(e_id).append('<option value="'+item.pk+'">'+item.valor+'</option>');
                });
           },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });

}


function ajax_patrimonio_existente(pn)
{
       django.jQuery.ajax({
           type: "POST",
	   url: "/patrimonio/patrimonio_existente",
	   dataType: "json",
	   data: {'part_number':pn},
	   success: function(retorno) {
	      if (retorno.marca) {
	         django.jQuery("#id_marca").val(retorno.marca);
	         django.jQuery("#id_modelo").val(retorno.modelo);
	         django.jQuery("#id_descricao").val(retorno.descricao);
	         django.jQuery("#id_procedencia").val(retorno.procedencia);
	      }
	   },
	   error: function(erro) {
	      alert('Erro: Sem retonro de requisição.');
	   }
       });
}


function ajax_filter_enderecos() {
     ent_id = django.jQuery("#id_entidade").val();
     django.jQuery("#id_endereco").html('<option value="">Carregando...</option>');

     django.jQuery.ajax({
       type: "POST",
       url: "/identificacao/escolhe_entidade",
       dataType: "json",
       data: {'entidade': ent_id},
       success: function(retorno){
          django.jQuery("#id_endereco").empty();
          django.jQuery("#id_endereco").append('<option value="">------------</option>');
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#id_endereco").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
       },
     });
} 

function ajax_filter_locais() {
     end_id = django.jQuery("#id_endereco").val();
     django.jQuery("#id_detalhe").html('<option value="">Carregando...</option>');

     django.jQuery.ajax({
       type: "POST",
       url: "/identificacao/escolhe_endereco",
       dataType: "json",
       data: {'endereco': end_id},
       success: function(retorno){
          django.jQuery("#id_detalhe").empty();
          django.jQuery("#id_detalhe").append('<option value="">------------</option>');
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#id_detalhe").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
       },
     });
}

function ajax_filter_pagamentos_memorando(termo)
{
     n = parseInt(django.jQuery("#id_corpo_set-TOTAL_FORMS").val());
     for(j=0;j<n;j++){
        django.jQuery("#id_corpo_set-"+j+"-pagamento_from").empty();
     }
     django.jQuery.ajax({
       type: "POST",
       url: "/memorando/pagamentos",
       dataType: "json",
       data: {'termo':termo},
       success: function(retorno) {
          for(j=0;j<n;j++){
             SelectBox.cache["id_corpo_set-"+j+"-pagamento_from"] = new Array();
          }
          django.jQuery("#id_corpo_set-__prefix__-pagamento_from").empty();
          django.jQuery.each(retorno, function(i, item){
              for(j=0;j<n;j++){
                 var opt = new Object ({value:item.pk, text:item.valor});
                 SelectBox.add_to_cache("id_corpo_set-"+j+"-pagamento_from", opt);
              }
              django.jQuery("#id_corpo_set-__prefix__-pagamento_from").append('<option value="'+item.pk+'">'+item.valor+'</option>');
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
   termo = django.jQuery("#id_termo").val();
   if (termo) {
     django.jQuery.ajax({
       type: "POST",
       url: "/memorando/pagamentos",
       dataType: "json",
       data: {'termo':termo},
       success: function(retorno) {
          django.jQuery("#id_corpo_set-__prefix__-pagamento_from").empty();
          django.jQuery.each(retorno, function(i, item){
              django.jQuery("#id_corpo_set-__prefix__-pagamento_from").append('<option value="'+item.pk+'">'+item.valor+'</option>');
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
   n = parseInt(django.jQuery("#id_corpo_set-TOTAL_FORMS").val());
   for(j=0;j<n;j++){
        django.jQuery("#id_corpo_set-"+j+"-pergunta").empty();
   }

   django.jQuery.ajax({
       type: "POST",
       url: "/memorando/perguntas",
       dataType: "json",
       data: {'memorando':memorando},
       success: function(retorno) {
          django.jQuery.each(retorno, function(i, item){
              for(j=0;j<n;j++){
                django.jQuery("#id_corpo_set-"+j+"-pergunta").append('<option value="'+item.pk+'">'+item.valor+'</option>');
              }
              django.jQuery("#id_corpo_set-__prefix__-pergunta").append('<option value="'+item.pk+'">'+item.valor+'</option>');
          });
       },
       error: function(erro) {
         alert('Erro. Sem retorno da requisicao.');
       }
   });
}

function ajax_select_pergunta(id_field)
{

       pergunta = django.jQuery("#"+id_field).val();
       partes = id_field.split("-");
       e_id = "#id_corpo_set-"+partes[1]+"-perg";
       django.jQuery(e_id).html('Carregando...');
       django.jQuery.ajax({
           type: "POST",
           url: "/memorando/escolhe_pergunta",
           dataType: "json",
           data: {'pergunta':pergunta},
           success: function(retorno) {
                django.jQuery(e_id).empty();
                django.jQuery(e_id).html(retorno);
           },
           error: function(erro) {
              alert('Erro: Sem retorno de requisição.');
           }
       });
}

function ajax_filter_patrimonios()
{
	filtro = django.jQuery("#id_filtra_patrimonio").val();
	django.jQuery.ajax({
		type: "GET",
		url: "/repositorio/seleciona_patrimonios",
		dataType: "json",
		data: {'string':filtro},
		success: function(retorno) {
			django.jQuery("#id_patrimonios").empty();
			django.jQuery.each(retorno, function(i, item) {
				django.jQuery("#id_patrimonios").append('<option value="'+item.pk+'">'+item.fields.ns+' - '+item.fields.descricao+'</option>');
			});
		},
	});
}

django.jQuery(window).load(function () {
    ajax_init_pagamentos();
});	
