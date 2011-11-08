from django.db import models
from django import forms
from django.forms.util import ErrorList

IMP_CONTROL = (
    (2, u'Implemented'),
    (1, u'Partly implemented'),
    (0, u'Not implemented'),
    (-1, u'Not applicable'),
)

STAND_REQ = (
    (2, u'Adherent '),
    (1, u'Partially adherent '),
    (0, u'Not adherent '),
)

MAND_REQ = (
    (1, u'Yes - 27001'),
    (2, u'Yes - Scope'),
    (0, u'Not mandatory'),
)

class Section(models.Model):
      description = models.CharField(max_length=100)
      number = models.IntegerField()
      
      def __unicode__(self):
          return '%s - %s' % (self.number, self.description)
          
          
class SubSection(models.Model):
      description = models.CharField(max_length=100)
      number = models.IntegerField()
      section = models.ForeignKey(Section)
      
      def __unicode__(self):
          return '%s - %s' % (self.number_display, self.description)

      @property
      def number_display(self):
          return '%s.%s' % (self.section.number, self.number)
          
class Iso(models.Model):
      number = models.IntegerField()
      control = models.CharField (max_length=100)
      subsection = models.ForeignKey (SubSection)
      mandatory_default = models.IntegerField(choices=MAND_REQ, null=True, blank=True)

      def __unicode__(self):
	  #return u'ISMS numero %s' % self.id
          return '%s %s' % (self.number_display, self.control)

      @property
      def number_display(self):
          return '%s.%s' % (self.subsection.number_display, self.number)
      def form(self):
	  return IsoForm(instance=self, prefix=str(self.id))

    
      class Meta:
	  ordering = ('subsection', 'number')


class IsoEval(models.Model):
      iso = models.ForeignKey('isms.Iso')
      evaluation = models.ForeignKey('isms.Evaluation')
      implemented =  models.IntegerField(choices=IMP_CONTROL, null=True, blank=True)
      standard =  models.IntegerField(choices=STAND_REQ, null=True, blank=True)
      mandatory =  models.IntegerField(choices=MAND_REQ, null=True, blank=True)
      observation = models.CharField(max_length=50, null=True, blank=True)


      def __unicode__(self):
          return '%s - %s' % (self.evaluation, self.iso)

      def form(self):
	  return IsoEvalForm(instance=self, prefix=str(self.id))

      @property
      def maximum(self):
	  if self.mandatory:
	      return 5
          elif self.implemented < 0:
              return -1
          else: return 4

      @property
      def current(self):
          if self.implemented < 0:
             return -1
          if self.implemented < 2:
             return self.implemented
          r = self.implemented+self.standard
	  if r == 4 and self.mandatory: return 5
	  return r

class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)

    def __unicode__(self):
        return '%s' % self.name

class Evaluation(models.Model):
    company = models.ForeignKey('isms.Company')
    date = models.DateField()

    def __unicode__(self):
        return '%s at %s' % (self.company, self.date)

    @property
    def maximum(self):
        m = 0
        for ie in self.isoeval_set.all():
            if ie.maximum> 0: m += ie.maximum

        return m

    @property
    def current(self):
        c = 0
        for ie in self.isoeval_set.all():
            if ie.current > 0: c += ie.current
        return c

    def sections(self):
        return Section.objects.filter(id__in=self.isoeval_set.values_list('iso__subsection__section__id', flat=True).distinct())

    def subsections(self, section):
        return SubSection.objects.filter(id__in=self.isoeval_set.values_list('iso__subsection__id', flat=True).filter(iso__subsection__section__id=section).distinct())

    class Meta:
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'

class IsoForm(forms.ModelForm):
    section = forms.CharField(max_length=10, widget=forms.HiddenInput)
    control = forms.CharField(max_length=100, widget=forms.HiddenInput)
    subsection = forms.ModelChoiceField(queryset=SubSection.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = Iso

class IsoEvalForm(forms.ModelForm):
    iso = forms.ModelChoiceField(queryset=Iso.objects.all(), widget=forms.HiddenInput)
    evaluation = forms.ModelChoiceField(queryset=Evaluation.objects.all(), widget=forms.HiddenInput, label='Assessment')
     
    class Meta:
        model = IsoEval

class HomeForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    evaluation = forms.ModelChoiceField(queryset=Evaluation.objects.none(), required=False, label='Assessment')
    date = forms.DateField(required=False, help_text=u'e.g. 2011-05-23')

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False):

        super(HomeForm, self).__init__(data, files, auto_id, prefix, initial,
                                       error_class, label_suffix, empty_permitted)
	if data:
            company_id = data['company']
            try:
                company = Company.objects.get(id=company_id)
                self.fields['evaluation'].queryset = Evaluation.objects.filter(company=company)
            except:
	        pass

    class Media:
        js = ('js/selects.js',)
