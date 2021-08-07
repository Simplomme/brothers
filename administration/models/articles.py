from django.db import models


class Articles(models.Model):
    article_name =models.CharField(unique=True,max_length=50)
    buying_price =models.FloatField()
    retail_price =models.FloatField(null=True,blank=True)
    wholesale_price =models.FloatField(null=True,blank=True)
    basically_content =models.FloatField(null=True,blank=True)
    qte_stock =models.FloatField()
    qte_min =models.FloatField(default=5)
    show =models.BooleanField(default=True)

    class Meta:
        db_table ="Articles"


    def __str__(self):
        return self.article_name
    @property
    def display_retail_price(self):
        if self.retail_price !=None:
            return self.retail_price
        else:
            return "Non définie"
    @property
    def display_wholesale_price(self):
        if self.wholesale_price !=None:
            return self.wholesale_price
        else:
            return "Non définie"
    @property
    def display_basically_content(self):
        if self.basically_content !=None:
            return self.basically_content
        else:
            return "Non définie"

    def convert_qte(self,unity):
        if unity==1:
            if self.retail_price==None:
                return None
            else:
                return self.qte_stock
        elif unity==2:
            if self.retail_price==None:
                return self.qte_stock
            elif self.basically_content !=None:
                return self.qte_stock/self.basically_content
            else:
                return None
        else:
            return None

    def selling_price(self,unity):
        if unity==1:
            return self.retail_price
        elif unity==2:
            return self.wholesale_price
        else:
            return None

    def getUnity(self):
        if self.retail_price!=None:
            return "détail"
        else:
            return "gros"
