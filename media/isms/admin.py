from django.contrib import admin
from models import *

class IsoEvalInline(admin.TabularInline):
    extra = 5
    
    model = IsoEval

class EvaluationAdmin(admin.ModelAdmin):
    inlines = [IsoEvalInline,]

admin.site.register(Iso)
admin.site.register(Section)
admin.site.register(SubSection)
admin.site.register(Company)
admin.site.register(Evaluation, EvaluationAdmin)
