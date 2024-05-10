from django import forms

class AnswerForm(forms.Form):
    detail = forms.CharField(widget=forms.Textarea)