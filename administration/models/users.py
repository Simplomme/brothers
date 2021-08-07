from django.db import models

class Users(models.Model):
    """Users models """
    user_name =models.CharField(unique=True,max_length=50)
    email =models.EmailField(null=True,blank=True)
    contact =models.CharField(max_length=15,null=True,blank=True)
    password =models.CharField(max_length=50,)
    is_admin =models.BooleanField(default=False,)

    class Meta:
        db_table ="Users"


    def __str__(self):
        return self.user_name
    @property
    def display_email(self):
        if self.email !=None:
            return self.email
        else:
            return "Non définie"
    @property
    def display_admin(self):
        if self.is_admin:
            return "Oui"
        else :
            return "Non"
