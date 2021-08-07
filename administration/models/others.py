from django.db import models

class Others(models.Model):
    """docstring for Others."""
    description =models.CharField(max_length=250)
    date =models.DateField()
    amount =models.FloatField()

    class Meta:
        db_table ="Others"
