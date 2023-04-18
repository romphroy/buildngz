from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    class Meta:
        labels_suffix = ''
        
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-input'}))
    to = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-input'}))
    comment = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        labels = {
            'name': 'Name',
            'email': 'Email',   
            'body': 'Comment',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
        }
        