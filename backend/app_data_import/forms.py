from django import forms


class PropertyDataImportForm(forms.Form):
    
    csv_file = forms.FileField(label='Select a CSV file')
