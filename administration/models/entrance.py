from django.db import models
from .articles import Articles

class Entrance(models.Model):
	article_id =models.ForeignKey(Articles,on_delete=models.CASCADE)
	date_entrance =models.DateField(auto_now_add=True)
	type_entrance =models.CharField(max_length=20)
	buying_price =models.FloatField()
	qte =models.FloatField()

	class Meta:
		db_table ="Entrance"

	@property
	def montant(self):
		return self.qte*self.buying_price
