from django.shortcuts import render
from django.urls import reverse
from brothers.views import logeFlag
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse,FileResponse
from datetime import datetime
from brothers.utils import render_to_pdf


from .forms import SellingForm
from administration.models.articles import Articles
from administration.models.entrance import Entrance
from .models import *
# Create your views here.

#############################################################################################
def onSelling(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    if request.method=='POST' and request.is_ajax():
        form = SellingForm(request.POST)
        if form.is_valid():
            article =form.cleaned_data["article_id"]
            cmd =Commande.objects.filter(article_id=article)
            if cmd:
                cmd=cmd[0]
            else:
                cmd =Commande()
                cmd.article_id=article
            try:
                if int(form.cleaned_data["unity"])==1:
                    cmd.unity="détail"
                elif int(form.cleaned_data["unity"])==2:
                    cmd.unity="gros"
                else:
                    return JsonResponse({"error":"L'action à échouée.Certaines donnéés sont invalides."},safe=False,status=400)
            except:
                return JsonResponse({"error":"L'action à échouée.Certaines donnéés sont invalides."},safe=False,status=400)
            if form.cleaned_data["qte_cmd"]>article.convert_qte(int(form.cleaned_data["unity"])):
                return JsonResponse({"error":"La quantité vendu ne peut dépasser la quantité en stock."},safe=False,status=400)
            cmd.selling_price=article.selling_price(int(form.cleaned_data["unity"]))
            cmd.qte=form.cleaned_data["qte_cmd"]
            cmd.discount=form.cleaned_data["reduction"]
            cmd.save()
            return JsonResponse("Ajouter avec succès",safe=False)
        else:
            errors=""
            for key in form.errors:
                errors +=" ".join(form.errors[key])
            return JsonResponse({"error":errors},safe=False,status=400)

    else:
        form =SellingForm()
    return render(request,'selling/pages/selling.html', {'form':form,"isAdmin":isAdmin})

def getData(request):
    id =request.POST["id"]
    try:
        article =Articles.objects.get(pk=int(id))
        unity =int(request.POST["unity"])
    except:
        return JsonResponse({"error":"L'article n'existe pas ou données invalides"},safe=False,status=400)
    result ={}
    result["qte_rest"]=article.convert_qte(unity)
    result["article_price"]=article.selling_price(unity)
    return JsonResponse(result,safe=False)

def getCmd(request):
    cmds =Commande.objects.all()
    html=""
    if cmds:
        total=0
        for cmd in cmds:
            html+="<tr>"
            html +="<td><button type=\"button\" name=\"delete\" data-id=\"{id}\" class=\"delete\"><span class=\"fa fa-trash\" style=\"color:red;\"></span></button></td>".format(id=cmd.id)
            html+="<td>{article}</td>".format(article=cmd.article_id)
            html+="<td>{selling_price}</td>".format(selling_price=cmd.selling_price)
            html+="<td>{qte}</td>".format(qte=cmd.qte)
            html+="<td>{price_brut}</td>".format(price_brut=cmd.montant_brut)
            html+="<td>{discount}</td>".format(discount=cmd.discount)
            html+="<td>{price_net}</td>".format(price_net=cmd.montant)
            html+="</tr>"
            total+=cmd.montant
        html+="<tr><td colspan='5'></td> <td>Total</td> <td>{toto}</td><tr>".format(toto=total)
    else:
        html+="<tr><td colspan='7'>Aucune commande en cours</td></tr>"
    return JsonResponse(html,safe=False)

def deleteCmd(request):
    if request.method=="POST" and request.is_ajax():
        action =request.POST["action"]
        id =request.POST["id"]
        try:
            cmd =Commande.objects.get(pk=int(id))
        except Exception as e:
            return JsonResponse({"error":"Cet article n'est pas disponible"},safe=False,status=400)
        if action=="fetch_data" and cmd:
            return JsonResponse(cmd.article_id.article_name,safe=False)
        elif action=="delete" and cmd:
            cmd.delete()
            return JsonResponse("Supprimer avec succès",safe=False)
    else:
        JsonResponse({"error":"error"},safe=False,status=400)

def save(request):
    if request.method=="POST" and request.is_ajax():
        cmds =Commande.objects.all()
        if cmds:
            num="00{0}".format(Sortie.objects.filter(data_exit=datetime.now()).count()+100)
            for cmd in cmds:
                exit =Sortie()
                exit.article_id=cmd.article_id
                exit.type_exit="Sortie"
                exit.unity=cmd.unity
                exit.selling_price=cmd.selling_price
                exit.qte=cmd.qte
                exit.discount=cmd.discount
                exit.profit=cmd.montant-cmd.convert_qte*cmd.article_id.buying_price
                exit.num =num
                exit.save()
                article =cmd.article_id
                article.qte_stock=article.qte_stock-cmd.convert_qte
                article.save()
            #return JsonResponse("succès",safe=False,)

            print =request.POST["print"]
            if print=='true':
                return JsonResponse({"date":str(datetime.date(datetime.now())),"num":num},safe=False)
            cancel(request)
            return JsonResponse("Enregistrer avec succès.",safe=False,)
        else:
            return JsonResponse({"error":"Aucune commande n'est en cours"},safe=False,status=400)

def cancel(request):
    cmds =Commande.objects.all()
    if cmds:
        cmds.delete()
        return JsonResponse("Commande annulée.",safe=False,)
    else:
        return JsonResponse({"error":"Aucune commande n'est en cours"},safe=False,status=400)
##############################################################################################
def onDailyLog(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]
    sortie =Sortie.objects.filter(data_exit=datetime.now())
    entrance =Entrance.objects.filter(date_entrance=datetime.now())
    return render(request,'selling/pages/dailylog.html',{"isAdmin":isAdmin,"sortie":sortie,"entrance":entrance,"date":datetime.now()})
############################################################################################

def printFiche(request):
    sortie =Sortie.objects.filter(data_exit=datetime.now())
    entrance =Entrance.objects.filter(date_entrance=datetime.now())
    filename ="fiche-journaliere-"+str(datetime.date(datetime.now()))+".pdf"
    pdf =render_to_pdf('selling/pages/fiche_journaliere.html',filename,{'date':datetime.now(),"sortie":sortie,"entrance":entrance})
    return pdf

def printFacture(request):
    date =request.GET.get("date",None)
    num =request.GET.get("num",None)
    try:
        cmds =Sortie.objects.filter(data_exit=date,num=num)
    except :
        result=None
    total =0.0
    for cmd in cmds:
        total +=cmd.montant
    pdf =render_to_pdf("selling/pages/facture.html","reçu.pdf",{"cmds":cmds,"date":datetime.strptime(date,'%Y-%m-%d'),"num":num,"total":total});
    cancel(request)
    return pdf

def showFacture(request):
    if logeFlag(request)==None:
        return HttpResponseRedirect(reverse('login:login'))
    isAdmin =request.session["isAdmin"]

    date =request.GET.get("date",None)
    num =request.GET.get("num",None)
    try:
        result =Sortie.objects.filter(data_exit=date,num=num)
    except :
        result=None
    return render(request,'selling/pages/show_facture.html',{"isAdmin":isAdmin,"date":date,"num":num,"data":result})
