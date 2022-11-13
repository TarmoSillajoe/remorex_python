from django.forms import ModelForm, fields
from .models import Part


# https://docs.djangoproject.com/en/4.1/ref/forms/api/#binding-uploaded-files
class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = [
            "part_code",
            "description",
            "assembly_group",
            "cars",
            "image",
        ]
