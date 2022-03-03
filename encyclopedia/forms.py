from django import forms 


class CreateForm(forms.Form):
    title = forms.CharField(label='Title', min_length=1, max_length=50)
    content = forms.CharField(label='Content', min_length=1, widget=forms.Textarea())


