from django import forms
from administration.models.articles import Articles

class SellingForm(forms.Form):
    tuple =(('1','détail'),('2','gros'),)
    #action =forms.CharField(widget=forms.HiddenInput(attrs={'value':"add"}),required=False)
    article_id = forms.ModelChoiceField(queryset=Articles.objects.filter(show=True).exclude(qte_stock=0).order_by('article_name'),label="Article",)
    unity =forms.ChoiceField(label="Type d'achat",choices=tuple)
    article_price = forms.FloatField(label='Prix Unité')
    qte_rest = forms.FloatField(label='Qte restant',required=False,)
    qte_cmd = forms.FloatField(label='Qte vendu',min_value=0,)
    reduction = forms.FloatField(label='Reduction',initial=0,required=False,min_value=0,)
    #hidden_id =forms.CharField(widget=forms.HiddenInput(attrs={'value':""}),required=False)

    def clean_reduction(self):
        if self.cleaned_data["reduction"]<0:
            raise forms.ValidationError("La reduction ne peut être négative.")
        return self.cleaned_data["reduction"]
    def clean_qte_cmd(self):
        if self.cleaned_data["qte_cmd"]<=0:
            raise forms.ValidationError("La quantité vendue ne peut être négative ou nulle")
        return self.cleaned_data["qte_cmd"]
