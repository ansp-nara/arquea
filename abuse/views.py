# Create your views here.
import datetime
from models import *
from django.template.response import TemplateResponse
from django.db.models import Count

def tabela(request, ano=None, mes=None):
    hoje = datetime.datetime.now()
    ano = hoje.year if not ano else int(ano)
    mes = hoje.month if not mes else int(mes)
   
    mensagens_filtradas = Mensagem.objects.filter(data__year=ano, data__month=mes) 
    tipos = list(Tipo.objects.values_list('nome', flat=True))
    instituicoes_incidentes = mensagens_filtradas.values('instituicao__display').annotate(total=Count('instituicao')).order_by('-total')
    inst = [i['instituicao__display'] for i in instituicoes_incidentes]
    totais = [i['total'] for i in instituicoes_incidentes] 

    tabela = [['-' for i in range(len(tipos))] for j in range(len(inst))]

    for c in mensagens_filtradas.values('tipo__nome', 'instituicao__display').annotate(total = Count('tipo')):
        i = inst.index(c['instituicao__display'])
        j = tipos.index(c['tipo__nome'])
        tabela[i][j] = c['total']

    for i in range(len(inst)):
        tabela[i].insert(0, totais[i])
        tabela[i].insert(0,inst[i])
    tabela.insert(0,tipos)
    tabela.append(['TOTAL', mensagens_filtradas.count()] + [mensagens_filtradas.filter(tipo__nome=t).count() or '-' for t in tipos])

    return TemplateResponse(request, 'abuse/tabela.html', {'tabela':tabela, 'data':datetime.date(ano,mes,1)})

def grafico(request):
        somas = []
        tipos = []
        for ano in range(2007,datetime.datetime.now().year+1):
                somas.append({'ano':ano, 'total':Mensagem.objects.filter(data__year=ano).count()})
                for tipo in Tipo.objects.all():
                        total = tipo.mensagem_set.filter(data__year=ano).count()
                        tipos.append({'ano':ano, 'tipo':tipo.nome, 'total':total})
        return TemplateResponse(request, 'abuse/grafico.html',{'soma':somas,'tipo':tipos, 'hoje':datetime.datetime.now()})

