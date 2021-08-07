from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.db.models import F,Q,Sum,Count
from administration.models import *
from selling.models import Sortie
from django.urls import reverse
from brothers.views import logeFlag
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
from brothers.utils import render_to_pdf

# Create your views here.

def onDashboard(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    stock =Articles.objects.aggregate(vol=Sum('qte_stock'),
    val =Sum(F('qte_stock')*F('buying_price')),
    actif =Count('id',filter=Q(show=True)),
    critique =Count('id',filter=Q(qte_stock__lte=F('qte_min'))))
    achat =Entrance.objects.aggregate(achat=Sum(F('qte')*F('buying_price'),filter=Q(date_entrance=datetime.now())))
    vente =Sortie.objects.filter(data_exit=datetime.now()).exclude(type_exit="Ajustement").aggregate(vente=Sum(F('qte')*F('selling_price')-F('discount')))
    profit =Sortie.objects.filter(data_exit=datetime.now()).exclude(type_exit="Ajustement").aggregate(profit=Sum('profit'))
    perte =Sortie.objects.filter(data_exit=datetime.now(),type_exit="Ajustement").aggregate(perte=Sum(F('profit')))
    depence =Others.objects.filter(date=datetime.now()).aggregate(depence=Sum(F('amount')))
    if profit['profit']==None and depence['depence']==None:
        benefice =0.0
    elif profit['profit']==None:
        benefice =-depence['depence']
    elif depence['depence']==None:
        benefice=profit['profit']
    else:
        benefice =profit['profit']-depence['depence']
    return render(request,'dashboard/pages/dashboard.html',{"isAdmin":isAdmin,"date":datetime.now(),"stock":stock,"achat":achat,
    "vente":vente,"profit":profit,"perte":perte,"benefice":benefice})


def actualiseData(request):
    if request.method=="POST" and request.is_ajax():
        start =request.POST["start"]
        end  =request.POST["end"]
        result={}
        result["achat"]=Entrance.objects.filter(date_entrance__gte=start).exclude(date_entrance__gt=end).aggregate(achat=Sum(F('qte')*F('buying_price')))
        result["vente"]=Sortie.objects.filter(data_exit__gte=start,type_exit="Sortie").exclude(data_exit__gt=end,).aggregate(vente=Sum(F('qte')*F('selling_price')-F('discount')))
        result["profit"]=Sortie.objects.filter(data_exit__gte=start,type_exit="Sortie").exclude(data_exit__gt=end).aggregate(profit=Sum(F('profit')))
        result["perte"]=Sortie.objects.filter(data_exit__gte=start,type_exit="Ajustement").exclude(data_exit__gt=end).aggregate(perte=Sum(F('profit')))
        depence=Others.objects.filter(date__gte=start,).exclude(date__gt=end).aggregate(depence=Sum(F('amount')))
        result["benefice"]=result["profit"]["profit"]-depence['depence']

        return JsonResponse(result,safe=False)
    else:
        return JsonResponse({"error":"error"},safe=False,status=400)


def vol_stock(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    stock =Articles.objects.filter(show=True)
    return render(request,"dashboard/pages/vol_stock.html",{"isAdmin":isAdmin,"stock":stock})


def critique(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    list =Articles.objects.filter(qte_stock__lte=F('qte_min'))
    return render(request,"dashboard/pages/critiques.html",{"isAdmin":isAdmin,"list":list})


def purchase(request,):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    start=request.GET["start"]
    end =request.GET["end"]
    try:
        start =datetime.strptime(start,'%Y-%m-%d')
        end =datetime.strptime(end,'%Y-%m-%d')
    except:
        return HttpResponse("""<center style="color:red;">Erreur du format date. La date doit être au format YYYY-mm-dd.<br/>
        Exemple: 2021-07-24.
        </center>""")
    result =Entrance.objects.filter(date_entrance__gte=start,date_entrance__lte=end).order_by('-date_entrance','article_id')
    return render(request,"dashboard/pages/purchase.html",{"isAdmin":isAdmin,"start":start,"end":end,"articles":result})

def sell(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    start=request.GET["start"]
    end =request.GET["end"]
    try:
        start =datetime.strptime(start,'%Y-%m-%d')
        end =datetime.strptime(end,'%Y-%m-%d')
    except:
        return HttpResponse("""<center style="color:red;">Erreur du format date. La date doit être au format YYYY-mm-dd.<br/>
        Exemple: 2021-07-24.
        </center>""")
    result =Sortie.objects.filter(data_exit__gte=start,data_exit__lte=end).exclude(type_exit='Ajustement').order_by('-data_exit','-num','article_id')
    return render(request,"dashboard/pages/sell.html",{"isAdmin":isAdmin,"start":start,"end":end,"articles":result})

def perte(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    start=request.GET["start"]
    end =request.GET["end"]
    try:
        start =datetime.strptime(start,'%Y-%m-%d')
        end =datetime.strptime(end,'%Y-%m-%d')
    except:
        return HttpResponse("""<center style="color:red;">Erreur du format date. La date doit être au format YYYY-mm-dd.<br/>
        Exemple: 2021-07-24.
        </center>""")
    result =Sortie.objects.filter(data_exit__gte=start,data_exit__lte=end).exclude(type_exit='Sortie').order_by('-data_exit','article_id')
    return render(request,"dashboard/pages/perte.html",{"isAdmin":isAdmin,"start":start,"end":end,"articles":result})

################################################################################

def printSell(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    start=request.GET["start"]
    end =request.GET["end"]
    try:
        start =datetime.strptime(start,'%Y-%m-%d')
        end =datetime.strptime(end,'%Y-%m-%d')
    except:
        return HttpResponse("""<center style="color:red;">Erreur du format date. La date doit être au format YYYY-mm-dd.<br/>
        Exemple: 2021-07-24.
        </center>""")
    result =Sortie.objects.filter(data_exit__gte=start,data_exit__lte=end).exclude(type_exit='Ajustement').order_by('-data_exit','article_id')
    filename ="ventes-du-"+str(datetime.date(start))+"-au-"+str(datetime.date(end))+".pdf"
    pdf =render_to_pdf("dashboard/pages/printPDF.html",filename,{"title":"Ventes","start":start,"end":end,"sorties":result,"entrances":None,"pertes":None})
    return pdf

def printPerte(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    start=request.GET["start"]
    end =request.GET["end"]
    try:
        start =datetime.strptime(start,'%Y-%m-%d')
        end =datetime.strptime(end,'%Y-%m-%d')
    except:
        return HttpResponse("""<center style="color:red;">Erreur du format date. La date doit être au format YYYY-mm-dd.<br/>
        Exemple: 2021-07-24.
        </center>""")
    result =Sortie.objects.filter(data_exit__gte=start,data_exit__lte=end).exclude(type_exit='Sortie').order_by('-data_exit','article_id')
    filename ="pertes-du-"+str(datetime.date(start))+"-au-"+str(datetime.date(end))+".pdf"
    pdf =render_to_pdf("dashboard/pages/printPDF.html",filename,{"title":"Pertes","start":start,"end":end,"sorties":None,"entrances":None,"pertes":result})
    return pdf

def printPurchase(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    start=request.GET["start"]
    end =request.GET["end"]
    try:
        start =datetime.strptime(start,'%Y-%m-%d')
        end =datetime.strptime(end,'%Y-%m-%d')
    except:
        return HttpResponse("""<center style="color:red;">Erreur du format date. La date doit être au format YYYY-mm-dd.<br/>
        Exemple: 2021-07-24.
        </center>""")
    result =Entrance.objects.filter(date_entrance__gte=start,date_entrance__lte=end).order_by('-date_entrance','article_id')
    filename ="achat-du-"+str(datetime.date(start))+"-au-"+str(datetime.date(end))+".pdf"
    pdf =render_to_pdf("dashboard/pages/printPDF.html",filename,{"title":"Achats","start":start,"end":end,"sorties":None,"entrances":result,"pertes":None})
    return pdf
