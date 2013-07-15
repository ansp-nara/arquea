from membro.models import *
import datetime

def teste():
    now = datetime.datetime.now()
    funcionarios = []
    for f in [m for m in Membro.objects.all() if m.funcionario is True]:
        func = {}
        func['nome'] = f.nome
        h = Historico.ativos.get(funcionario=True, membro=f)
        func['admissao'] = h.inicio
        ferias = f.ferias_set.order_by('-inicio')
        if ferias.count() == 0:
            continue
        ferias = ferias[0]
        func['periodo'] = ferias.inicio
        try:
            cf = ferias.controleferias_set.get(oficial=True)
        except:
            continue
        func['inicio'] = cf.inicio
        func['termino'] = cf.termino
        dias = cf.termino - cf.inicio
        func['dias'] = dias.days + 1
        #func['decimo_terceiro'] = ferias.decimo_terceiro

        funcionarios.append(func)


    print funcionarios
