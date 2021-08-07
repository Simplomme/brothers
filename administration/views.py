from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,FileResponse
from datetime import datetime
from django.urls import reverse
from brothers.views import logeFlag
from django.http import HttpResponseRedirect
from brothers.utils import render_to_pdf

from  .models import *
from selling.models import Sortie
from .forms import *

# Create your views here.
###################################ARTICCLES VIEWS##############################################

def onArticle(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    if isAdmin==False:
        return HttpResponse("<center><h1 style=\"color:red;\">Accès refusé</h1></center>")

    if request.method=="POST" and request.is_ajax():
        form =ArticleForm(request.POST)
        if form.is_valid():
            action =form.cleaned_data["action"]
            if action=="add":
                article =Articles()
                article.article_name=form.cleaned_data["article_name"]
                article.buying_price=form.cleaned_data["buying_price"]
                article.retail_price=form.cleaned_data["retail_price"]
                article.wholesale_price=form.cleaned_data["wholesale_price"]
                article.basically_content=form.cleaned_data["basically_content"]
                article.qte_stock=form.cleaned_data["qte_stock"]
                article.qte_min=form.cleaned_data["qte_min"]
                try:
                    article.save()
                except:
                    article =Articles.objects.get(article_name=form.cleaned_data["article_name"])
                    if article.show==True:
                        return JsonResponse({"error":"Cet article existe déja."},safe=False,status=400)
                    article.buying_price=form.cleaned_data["buying_price"]
                    article.retail_price=form.cleaned_data["retail_price"]
                    article.wholesale_price=form.cleaned_data["wholesale_price"]
                    article.basically_content=form.cleaned_data["basically_content"]
                    article.qte_stock=form.cleaned_data["qte_stock"]
                    article.qte_min=form.cleaned_data["qte_min"]
                    article.show =True

                    article.save()
                entrance =Entrance()
                entrance.type_entrance="Stock initial"
                entrance.buying_price =article.buying_price
                entrance.qte =article.qte_stock
                entrance.article_id =article
                entrance.save()
                return JsonResponse("Ajouter avec succès",safe=False)
            elif action=="edit":
                id =form.cleaned_data["hidden_id"]
                try:
                    article =Articles.objects.get(pk=int(id))
                except :
                    return JsonResponse({"error":"Cet article n'existe pas"},safe=False,status=400)
                article.article_name=form.cleaned_data["article_name"]
                article.retail_price=form.cleaned_data["retail_price"]
                article.wholesale_price=form.cleaned_data["wholesale_price"]
                article.basically_content=form.cleaned_data["basically_content"]
                article.qte_min=form.cleaned_data["qte_min"]

                try:
                    article.save()
                    return JsonResponse("Modifier avec succès",safe=False,)
                except:
                    return JsonResponse({"error":"Ce nom d'article exite déja"},safe=False,status=400)
            else:
                return JsonResponse({"error":"Action non pris en compte"},safe=False,status=400)
        else:
            errors =""
            for key in form.errors:
                errors +=" ".join(form.errors[key])
            return JsonResponse({"error":errors},safe=False,status=400)
    else:
        form =ArticleForm()
    return render(request,'administration/pages/articles.html',{"isAdmin":isAdmin,'form':form})

def articlesListe(request):
    articles =Articles.objects.filter(show=True).order_by('article_name');
    html =""
    if articles :
        for article in articles:
            html+="<tr>"
            html+="<td>{article}</td>".format(article=article.article_name)
            html+="<td>{buying_price}</td>".format(buying_price=article.buying_price)
            html+="<td>{retail_price}</td>".format(retail_price=article.display_retail_price)
            html+="<td>{wholesale_price}</td>".format(wholesale_price=article.display_wholesale_price)
            html+="<td>{basically_content}</td>".format(basically_content=article.display_basically_content)
            html+="<td>{qte_stock}</td>".format(qte_stock=article.qte_stock)
            html+="<td>{qte_min}</td>".format(qte_min=article.qte_min)
            html +="<td><button type=\"button\" name=\"edit\" data-id=\"{id}\" class=\"edit\"><span class=\"fas fa-edit\" style=\"color:blue;\"></span></button></td>".format(id=article.id)
            html +="<td><button type=\"button\" name=\"delete\" data-id=\"{id}\" class=\"delete\"><span class=\"fa fa-trash\" style=\"color:red;\"></span></button></td>".format(id=article.id)
            html+="</tr>"
    else:
        html+="<tr><td colspan='9'>Aucun article trouvé</td></tr>"
    return JsonResponse(html,safe=False)

def getArticle(request):
    id =request.POST["id"]
    try:
        article =Articles.objects.get(pk=int(id))
    except :
        return JsonResponse({"error":"Cet article n'existe pas"},safe=False,status=400)
    result ={
    "article_name":article.article_name,
    "buying_price":article.buying_price,
    "retail_price":article.retail_price,
    "wholesale_price":article.wholesale_price,
    "basically_content":article.basically_content,
    "qte_stock":article.qte_stock,
    "qte_min":article.qte_min,
    }

    return JsonResponse(result,safe=False)

def deleteArticle(request):
    id =request.POST["id"]
    try:
        article =Articles.objects.get(pk=int(id))
    except :
        return JsonResponse({"error":"Cet article n'existe pas"},safe=False,status=400)
    article.qte_stock=0
    article.show=False
    article.save()
    return JsonResponse("Supprimer avec succès",safe=False)
######################################STOCK VIEWS############################################

def onStock(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    if isAdmin==False:
        return HttpResponse("<center><h1 style=\"color:red;\">Accès refusé</h1></center>")

    if request.method=="POST" and request.is_ajax():
        form =EntranceForm(request.POST)
        if form.is_valid():
            entrance =Entrance()
            entrance.article_id=form.cleaned_data["article_id"]
            entrance.type_entrance="Entrée"
            entrance.buying_price=form.cleaned_data["buying_price"]
            entrance.qte=form.cleaned_data["qte"]
            entrance.save()

            article =form.cleaned_data["article_id"]
            article.retail_price =form.cleaned_data["retail_price"]
            article.wholesale_price =form.cleaned_data["wholesale_price"]
            article.basically_content =form.cleaned_data["basically_content"]
            article.qte_stock =article.qte_stock+form.cleaned_data["qte"]
            article.buying_price =form.cleaned_data["buying_price"]
            article.show =True
            article.save()
            return JsonResponse("Enregistrer avec succès",safe=False)
        else:
            errors =""
            for key in form.errors:
                errors +=" ".join(form.errors[key])
            return JsonResponse({"error":errors},safe=False,status=400)
    else:
        form =EntranceForm()
    return render(request,'administration/pages/stock.html',{"isAdmin":isAdmin,"form":form})

def getDayEntrance(request):
    entrances =Entrance.objects.filter(date_entrance=datetime.now())
    html=""
    if entrances:
        for entrance in entrances:
            html+="<tr>"
            html+="<td>{article}</td>".format(article=entrance.article_id)
            html+="<td>{type}</td>".format(type=entrance.type_entrance)
            html+="<td>{buying_price}</td>".format(buying_price=entrance.buying_price)
            html+="<td>{qte}</td>".format(qte=entrance.qte)
            html+="<td>{montant}</td>".format(montant=entrance.montant)
            #html +="<td><button type=\"button\" name=\"edit\" data-id=\"{id}\" class=\"edit\"><span class=\"fas fa-edit\" style=\"color:blue;\"></span></button></td>".format(id=entrances.id)
            #html +="<td><button type=\"button\" name=\"delete\" data-id=\"{id}\" class=\"delete\"><span class=\"fa fa-trash\" style=\"color:red;\"></span></button></td>".format(id=entrances.id)
            html+="</tr>"
    else:
        html="<tr><td colspan='4'>Aucun Approvisionnement</td></tr>"
    return JsonResponse(html,safe=False)

############## USERS VIEWS ##########################################

def newUsers(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    if isAdmin==False:
        return HttpResponse("<center><h1 style=\"color:red;\">Accès refusé</h1></center>")

    if request.method=='POST' and request.is_ajax():
        form =UserForm(request.POST)
        if form.is_valid():
            action =form.cleaned_data["action"]

            if action=="add" :
                user =Users()
                user.user_name=form.cleaned_data["user_name"]
                user.password=form.cleaned_data["password"]
                user.contact=form.cleaned_data["contact"]
                user.email=form.cleaned_data["email"]
                user.is_admin=form.cleaned_data["is_admin"]

                try:
                    user.save()
                except:
                    return JsonResponse({"error":"Ce nom d'utilisateur est déja pris"},safe=False,status=400)
                return JsonResponse("Ajouter avec succès",safe=False)
            elif action=="edit" :
                id =form.cleaned_data["hidden_id"]
                try:
                    user =Users.objects.get(pk=int(id))
                except:
                    return JsonResponse({"error":"Cet utilisateur n'existe pas"},safe=False,status=400)
                if user.password!=form.cleaned_data["password"]:
                    return JsonResponse({"error":"Erreure d'identification"},safe=False,status=400)
                else:
                    user.user_name=form.cleaned_data["user_name"]
                    if form.cleaned_data["new_password"]!="":
                        user.password=form.cleaned_data["new_password"]
                    user.contact=form.cleaned_data["contact"]
                    user.email=form.cleaned_data["email"]
                    user.is_admin=form.cleaned_data["is_admin"]
                    try:
                        user.save()
                    except:
                        return JsonResponse({"error":"Ce nom d'utilisateur est déja pris"},safe=False,status=400)
                return JsonResponse("Modifier avec succès",safe=False)
            else:
                return("<h1>Erreure.</h1> Action non reconnue")
    else:
        form =UserForm()
    return render(request,'administration/pages/users.html',{"isAdmin":isAdmin,'form':form})

def usersList(request):
    users =Users.objects.all().order_by("user_name")
    html =""

    if users :
        for user in users:
            html +="<tr>"
            html +="<td>{user_name}</td>".format(user_name=user.user_name)
            html +="<td>{email}</td>".format(email=user.display_email)
            html +="<td>{contact}</td>".format(contact=user.contact)
            html +="<td>{is_admin}</td>".format(is_admin=user.display_admin)
            html +="<td><button type=\"button\" name=\"edit\" data-id=\"{id}\" class=\"edit\"><span class=\"fas fa-edit\" style=\"color:blue;\"></span></button></td>".format(id=user.id)
            html +="<td><button type=\"button\" name=\"delete\" data-id=\"{id}\" class=\"delete\"><span class=\"fa fa-trash\" style=\"color:red;\"></span></button></td>".format(id=user.id)
            html +="</tr>"
    else:
        html ="""
        <tr>
        <td colspan="6">Aucun utilisateur trouvé</td>
        </tr>
        """
    return JsonResponse(html,safe=False)

def getUser(request):
    id =request.POST["id"]
    try:
        user =Users.objects.get(pk=int(id))
    except:
        return JsonResponse({"error":"Cet utilisateur n'existe pas"},safe=False,status=400)
    result ={
    "user_name":user.user_name,
    "email":user.email,
    "contact":user.contact,
    "is_admin":user.is_admin,
    }
    return JsonResponse(result,safe=False)

def deleteUser(request):
    id =request.POST["id"]
    try:
        user =Users.objects.get(pk=int(id))
    except:
        return JsonResponse({"error":"Cet utilisateur n'existe pas"},safe=False,status=400)
    user.delete()
    return JsonResponse("Supprimer avec succès",safe=False)

def printPDF(request):
    data =Articles.objects.all().order_by('article_name')
    filename="fiche-inventaire-"+str(datetime.date(datetime.now()))+".pdf"
    pdf =render_to_pdf("administration/pages/fiche_inventaire.html",filename,{"data":data,"date":datetime.now()})
    return pdf

#######################################################################################################################

def ajuster(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    if isAdmin==False:
        return HttpResponse("<center><h1 style=\"color:red;\">Accès refusé</h1></center>")
    data =Articles.objects.all().order_by('article_name')
    return render(request,"administration/pages/ajustement.html",{"isAdmin":isAdmin,"articles":data})


def execAjuster(request):
    list =""
    for key in request.POST:
        try:
            id =int(key)
            value =int(request.POST[key])
            article =Articles.objects.get(pk=id)
            if article.qte_stock>value:
                exit =Sortie()
                exit.article_id=article
                exit.type_exit="Ajustement"
                exit.unity=article.getUnity()
                exit.selling_price=article.buying_price
                exit.qte=article.qte_stock-value
                exit.discount=0.0
                exit.profit=exit.qte*article.buying_price
                exit.save()
                article.qte_stock=value
                article.save()

            elif article.qte_stock<value:
                entrance =Entrance()
                entrance.article_id =article
                entrance.type_entrance="Ajustement"
                entrance.buying_price =article.buying_price
                entrance.qte =value -article.qte_stock
                entrance.save()
                article.qte_stock =value
                article.save()
        except :
            pass
    return HttpResponseRedirect(reverse('selling:dailylog'))

####################################################################################################################

def others(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    if isAdmin==False:
        return HttpResponse("<center><h1 style=\"color:red;\">Accès refusé</h1></center>")
    if request.method=="POST" and request.is_ajax():
        form =OthersForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse("Enregistrer avec succès",safe=False)
        else:
            return JsonResponse({"error":"Echec d'enregistrement"},safe=False,status=400)
    else:
        form =OthersForm()
    return render(request,"administration/pages/others.html",{"isAdmin":isAdmin,"form":form})


def othersList(request):
    others =Others.objects.all().order_by("-date","-id");
    html =""

    if others :
        for other in others:
            html +="<tr>"
            html +="<td>{0}</td>".format(other.description)
            html +="<td>{0}</td>".format(other.date)
            html +="<td>{0}</td>".format(other.amount)
            html +="</tr>"
    else:
        html ="""
        <tr>
        <td colspan="3">Aucune dépense trouvée.</td>
        </tr>
        """
    return JsonResponse(html,safe=False)
