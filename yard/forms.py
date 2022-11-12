from django.forms import ModelForm
from .models import Part


class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = ["part_code", "description"]
