from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Selecciona un archivo CSV o Excel",
        help_text="Solo archivos .csv, .xls o .xlsx"
    )