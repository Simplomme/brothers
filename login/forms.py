from django import forms

class LoginForm(forms.Form):
    username =forms.CharField(label='Nom utilisateur',max_length=50,required=True)
    password =forms.CharField(widget=forms.PasswordInput,label='Mot de passe',max_length=50,required=True)
