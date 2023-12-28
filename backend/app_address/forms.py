# app_address/forms.py

from django import forms
from .models import DynamicRelationAreaLocality, Locality

class DynamicRelationAreaLocalityForm(forms.ModelForm):
    class Meta:
        model = DynamicRelationAreaLocality
        fields = '__all__'

    locality = forms.ModelChoiceField(
        queryset=Locality.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'locality_type' in self.data:
            try:
                locality_type_id = int(self.data.get('locality_type'))
                self.fields['locality'].queryset = Locality.objects.filter(locality_type_id=locality_type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance and hasattr(self.instance, 'locality_type'):
            self.fields['locality'].queryset = Locality.objects.filter(locality_type=self.instance.locality_type)