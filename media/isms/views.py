# Create your views here.

from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.forms.formsets import formset_factory

@login_required
def atualiza1(request):
    if request.method == 'POST':
        for iso in Iso.objects.all():
            f = IsoForm(request.POST, instance=iso, prefix=str(iso.id))
            f.save()

    ret = []
    for s in Section.objects.all():
        rows = 1
        for sub in s.subsection_set.all():
            rows += 1
	    rows += sub.iso_set.count()
	ret.append({'rows':rows, 'section':s})
    maximo = 0
    atual = 0 
    for iso in Iso.objects.all():
	maximo += iso.maximum
        if iso.current > 0:
		atual += iso.current
	
    return render_to_response('isms/isms.html', {'sections':ret, 'maximum':maximo, 'current':atual})
        
def atualiza(request):
    if request.method == 'POST':
        submit = request.POST.get('submit')
        if submit == 'Add assessment':
            form = HomeForm(request.POST)
            if not form.is_valid():
                return render_to_response('isms/index.html', {'form':form})
            company_id = request.POST.get('company')
            if not company_id: raise Http404
            company = get_object_or_404(Company, pk=company_id)
            date = request.POST.get('date')
            if company.evaluation_set.count() < 1:
                evaluation = Evaluation(company=company, date=date)
                evaluation.save()
                evaluation = get_object_or_404(Evaluation, pk=evaluation.id)
                for iso in Iso.objects.all():
                    isoeval = IsoEval(evaluation=evaluation, iso=iso, mandatory=iso.mandatory_default)
                    isoeval.save()
            else:
                last_eval = company.evaluation_set.order_by('-date')[0]
                evaluation = Evaluation(company=company, date=date)
                evaluation.save()
                evaluation = get_object_or_404(Evaluation, pk=evaluation.id)
                for last_isoeval in last_eval.isoeval_set.all():
                    isoeval = IsoEval(evaluation=evaluation, iso=last_isoeval.iso, mandatory=last_isoeval.mandatory,
                                      implemented=last_isoeval.implemented, standard=last_isoeval.standard)
                    isoeval.save()
        elif submit == 'View/change':
            eval_id = request.POST.get('evaluation')
            if not eval_id: raise Http404
            evaluation = get_object_or_404(Evaluation, pk=eval_id)
        elif submit == 'Save':
            eval_id = request.POST.get('eval')
            evaluation = get_object_or_404(Evaluation, pk=eval_id)
            for isoeval in evaluation.isoeval_set.all():
                f = IsoEvalForm(request.POST, instance=isoeval, prefix=str(isoeval.id))
                f.save()
        else:
	    company_id = request.POST.get('company')
            if not company_id: raise Http404
            company = get_object_or_404(Company, pk=company_id)
            sections = []
            t_max = 0
            t_current = [0 for i in range(company.evaluation_set.count())]
            for s in Section.objects.all():
                evals = []
                maximum = 0
                j = 0
                for e in company.evaluation_set.order_by('date'):
 		    mx = 0
                    c = 0
                    for i in e.isoeval_set.filter(iso__subsection__section=s):
                        if not maximum and i.maximum > 0: mx += i.maximum
                        if i.current > 0: c += i.current
                    if not maximum: maximum = mx
                    t_current[j] += c
                    j += 1
                    evals.append({'eval':e, 'current':c})
                sections.append({'section':s, 'maximum':maximum, 'evals':evals})
                t_max += maximum
            return render_to_response('isms/comparision.html',
                                     {'company':company, 'sections':sections, 'tmax':t_max, 'tcur':t_current,
                                      'total':company.evaluation_set.order_by('date')})
                    
    else:
        eval_id = request.GET.get('evaluation')
        evaluation = get_object_or_404(Evaluation, pk=eval_id)

    ret = []
    for s in evaluation.sections():
        rows = 1
        subs = []
        for sub in evaluation.subsections(s.id):
            rows += 1
            evals = evaluation.isoeval_set.filter(iso__subsection=sub).order_by('iso__number')
	    rows += evals.count()
            subs.append({'sub':sub, 'evals':evals})
	ret.append({'rows':rows, 'section':s, 'subsections':subs})
        
    return render_to_response('isms/eval.html', {'eval':evaluation, 'sections':ret})

def index(request):
    form = HomeForm()

    return render_to_response('isms/index.html', {'form':form})

def evals(request):
    if request.method == 'GET':
        raise Http404

    company_id = request.POST.get('company_id')
    company = get_object_or_404(Company, pk=company_id)

    retorno = []
    for e in company.evaluation_set.all():
        retorno.append({'pk':e.id, 'valor':e.__unicode__()})
    json = simplejson.dumps(retorno)

    return HttpResponse(json, mimetype='application/json')

