from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from .utils import render_to_pdf

def index(request):
    return render(request,'pages/index.html')

def logeFlag(request):
    if 'isAdmin' in request.session:
        return request.session["isAdmin"]
    else:
        return None

def print(request):
    pdf =render_to_pdf("pages/pdf.html")

    return pdf
