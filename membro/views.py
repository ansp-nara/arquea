# -*- coding: utf-8 -*-

# Create your views here.

import datetime
from models import *
from utils.functions import render_to_pdf

def ferias(context):
    now = datetime.datetime.now()
    funcionarios = []
    for f in [m for m in Membro.objects.all() if m.funcionario is True]:
        func = {}
        func['nome'] = f.nome
        h = Historico.ativos.get(funcionario=True, membro=f)
        func['admissao'] = h.inicio.strftime("%d/%m/%Y")
        ferias = f.ferias_set.order_by('-inicio')
        if ferias.count() == 0:
            continue
        ferias = ferias[0]
        final = ferias.inicio - datetime.timedelta(1)
        final = datetime.date(final.year+1, final.month, final.day)
        func['periodo'] = '%s a %s' % (ferias.inicio.strftime("%d/%m/%Y"), final.strftime("%d/%m/%Y"))
        try:
            cf = ferias.controleferias_set.get(oficial=True)
        except:
            continue
        func['ferias'] = '%s a %s' % (cf.inicio.strftime("%d/%m/%Y"), cf.termino.strftime("%d/%m/%Y"))
        dias = cf.termino - cf.inicio
        func['dias'] = dias.days + 1
        func['decimo_terceiro'] = u'Sim' if ferias.decimo_terceiro else u'Não'

        funcionarios.append(func)

    return render_to_pdf('membro/ferias.pdf', {'funcionarios':funcionarios, 'ano':now.year+1})

