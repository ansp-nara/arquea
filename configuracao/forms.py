from .models import ClassesExtra
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.contenttypes.models import ContentType

class ContentTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s/%s' % (obj.app_label, obj.model)

class ClassesExtraForm(forms.ModelForm):
    content_type = ContentTypeChoiceField(queryset=ContentType.objects.order_by('app_label', 'model'))
    help = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ClassesExtra
        fields = '__all__'
