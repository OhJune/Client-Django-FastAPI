from django import forms
from main_site.models import board 


class boardForm(forms.ModelForm):
    class Meta:
        model = board
        fields = ['subject', 'content']
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
        }  