from pyexpat.errors import messages
from tkinter import E
from django.shortcuts import render, redirect
import requests, json 
from .forms import StockForm
from django.contrib import messages
from .models import Stock 
# Create your views here.
def home(request):
    #pk_4c68895f25a94a97ba943173f0aa9638
    return render(request,'home.html',{})

def home(request):
    
    stocks = []
    api_req = requests.get(
        "https://cloud.iexapis.com/stable/stock/market/list/mostactive?token=pk_4c68895f25a94a97ba943173f0aa9638")
    try:
        res = json.loads(api_req.content)
        stocks = res
    except Exception as e:
        res = "Error"
    
    return render(request,'home.html',{"api": stocks})

def add_stock(request):
    if request.method=="POST":
        form = StockForm(request.POST or None)
        if(form.is_valid()):
            form.save()
            messages.success(request, "stock is added to portfolio")
    return redirect("home")


def portfolio(request):
    ticker=Stock.objects.all()
    stocks=[]
    for tick in ticker:
        api_req=requests.get("https://cloud.iexapis.com/stable/stock/"+ str(tick) + "/quote?token=pk_4c68895f25a94a97ba943173f0aa9638");
        try:
            dict={}
            res=json.loads(api_req.content)
            dict.update({"id":tick.id,"ticker":res})
            stocks.append(dict)
        except Exception as e:
            res = e
        
    return render(request,"portfolio.html", {"stocks":stocks})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "stock is removed")
    return redirect("portfolio")