from django import forms

class ContactForm(forms.Form):
	fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Name"}))
	email    = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Email"}))
	message  = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"message"}))