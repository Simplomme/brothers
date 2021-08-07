from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from .forms import LoginForm
from administration.models.users import Users
# Create your views here.
def onLogin(request):
    if request.method=="POST":
        form =LoginForm(request.POST)
        if form.is_valid():
            user =Users.objects.filter(user_name=form.cleaned_data["username"],password=form.cleaned_data["password"])
            if user:
                user =user[0]
                request.session["isAdmin"]=user.is_admin
                return HttpResponseRedirect(reverse('selling:selling'))
            else:
                return render(request,'login/pages/login.html',{'form':form,"error":"Nom d'utilisateur ou mot de passe invalide"})
    else:
        form =LoginForm()
    return render(request,'login/pages/login.html',{'form':form,"error":""})
def logout(request):
    try:
        del request.session["isAdmin"]
        request.session.flush()
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('login:login'))
