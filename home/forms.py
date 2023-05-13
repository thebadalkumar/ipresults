from django import forms
from .models import rsFiles

class EnrollNum(forms.Form):
    query = forms.CharField(max_length=13, required=True,widget=forms.TextInput(attrs={
        'class': 'form-control text-primary text-center col-md-12 col-sm-10 mx-auto font-weight-bold',
        'id': 'enroll',
        'name': 'enroll',
        'placeholder':'Enter Enrollment Number', 
        'autocomplete':'off',
        'title':'Enter Enrollment Number'
        }))
class UploadForm(forms.ModelForm):
    class Meta:
        model = rsFiles
        fields = ('course', 'pdf', 'examination')
        widgets = {
        'course': forms.Select(attrs={'class':'form-control'}),
        'pdf': forms.FileInput(attrs={'class':'custom-file-input'}),
        'examination': forms.Select(attrs={'class':'form-control'}),
        }