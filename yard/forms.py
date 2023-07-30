from django import forms

from .models import Part
from django.utils.translation import gettext_lazy


# https://docs.djangoproject.com/en/4.1/ref/forms/api/#binding-uploaded-files
class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            "part_code",
            "description",
            "assembly_group",
            "cars",
            "image",
        ]


class QueryForm(forms.Form):
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20, label=gettext_lazy("your phone"))
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
