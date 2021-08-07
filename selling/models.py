from django.db import models
from administration.models.articles import Articles
# Create your models here.
class Commande(models.Model):
    """docstring fo Commande."""
    article_id =models.ForeignKey(Articles,on_delete=models.CASCADE)
    unity =models.CharField(max_length=10)
    selling_price =models.FloatField()
    qte =models.FloatField()
    discount =models.FloatField(default=0)

    class Meta:
        db_table ="Commande"

    @property
    def montant(self):
        return self.qte*self.selling_price-self.discount

    @property
    def montant_brut(self):
        return self.qte*self.selling_price

    @property
    def convert_qte(self):
        if self.unity=="détail":
            return self.qte
        elif self.article_id.retail_price==None:
            return self.qte
        else:
            return self.qte*self.article_id.basically_content



class Sortie(models.Model):
    """docstring for Sortie."""
    article_id =models.ForeignKey(Articles,on_delete=models.CASCADE)
    data_exit =models.DateField(auto_now_add=True)
    type_exit =models.CharField(max_length=20)
    unity =models.CharField(max_length=10)
    selling_price =models.FloatField()
    qte =models.FloatField()
    discount =models.FloatField(default=0)
    profit =models.FloatField()
    num =models.CharField(max_length=10,null=True,blank=True)


    class Meta:
        db_table ="Sortie"


    @property
    def montant(self):
        return self.qte*self.selling_price-self.discount

    @property
    def montant_brut(self):
        return self.qte*self.selling_price
