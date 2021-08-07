from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models.articles import Articles
from .models.others import Others


def validate_value(value):
    if value<=0:
        raise ValidationError("Les valeurs négatives ne sont pas permises.")


class UserForm(forms.Form):
    user_name =forms.CharField(label="Nom utilisateur",max_length=50)
    email =forms.EmailField(label="Email",required=False)
    contact =forms.CharField(label="Contact",max_length=15,widget=forms.NumberInput())
    password =forms.CharField(label="Mot de passe",max_length=50,widget=forms.PasswordInput())
    new_password =forms.CharField(label="Nouveau mot de passe",max_length=50,widget=forms.PasswordInput(),required=False)
    confirmation =forms.CharField(label="Confirmation",max_length=50,widget=forms.PasswordInput(),required=False)
    is_admin =forms.BooleanField(label="Admin",required=False,)
    action =forms.CharField(widget=forms.HiddenInput(attrs={'value':"add"}),required=False)
    hidden_id =forms.CharField(widget=forms.HiddenInput(attrs={'value':""}),required=False)


class ArticleForm(forms.Form):
    """docstring fs ArticleForm."""
    action =forms.CharField(widget=forms.HiddenInput(attrs={'value':"add"}),required=False)
    article_name =forms.CharField(label="Article",max_length=50)
    buying_price =forms.FloatField(label="Prix d'achat", min_value=0,validators=[validate_value])
    retail_price =forms.FloatField(label="Prix vente détaille",required=False,min_value=0,validators=[validate_value])
    wholesale_price =forms.FloatField(label="Prix vente gros",required=False,min_value=0,validators=[validate_value])
    basically_content =forms.FloatField(label="Gros ==> Détaille",required=False,min_value=0,validators=[validate_value])
    qte_stock =forms.FloatField(label="Stock",min_value=0,validators=[validate_value])
    qte_min =forms.FloatField(label="Qte min",initial=5,min_value=0,validators=[validate_value])
    hidden_id =forms.CharField(widget=forms.HiddenInput(attrs={'value':""}),required=False)

class EntranceForm(forms.Form):
    """docstring for EntranceForm."""
    article_id =forms.ModelChoiceField(queryset=Articles.objects.filter(show=True).order_by('article_name'),label="Article",)
    buying_price =forms.FloatField(label="Prix d'achat",min_value=0,validators=[validate_value])
    retail_price =forms.FloatField(label="Prix vente détaille",required=False,min_value=0,validators=[validate_value])
    wholesale_price =forms.FloatField(label="Prix vente gros",required=False,min_value=0,validators=[validate_value])
    basically_content =forms.FloatField(label="Gros ==> Détaille",required=False,min_value=0,validators=[validate_value])
    qte =forms.FloatField(label="Qte",min_value=0,validators=[validate_value])


class OthersForm(forms.ModelForm):
    """docstring for OthersForm."""

    class Meta:
        model =Others
        exclude =["id"]
        widgets ={"date":forms.TextInput(attrs={"type":"date"})}
        labels  ={"amount":"Montant"}
