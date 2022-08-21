from pyexpat.errors import messages

from django.shortcuts import render, redirect
import requests, json 
from .forms import StockForm
from django.contrib import messages
from .models import Stock 
# Create your views here.

    #pk_4c68895f25a94a97ba943173f0aa9638
    

def home(request):
    if(request.method == 'POST'):
        ticker = request.POST['ticker']

        api_req = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker + "/quote?token=pk_4c68895f25a94a97ba943173f0aa9638");
        try:
            res = json.loads(api_req.content)
        except Exception as e:
            res = "Error"
        return render(request, 'Ticker.html', {'api':res})
    else:
    
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
    ticks_count = {}
    for tick in ticker:
        if(str(tick) in ticks_count.keys()):
            ticks_count[str(tick)] = [ticks_count[str(tick)][0] + 1 , ticks_count[str(tick)][1]]
        else:
            ticks_count.update({str(tick): [1, tick.id]})
            
    
    for t,c in ticks_count.items():
        
            
        api_req=requests.get("https://cloud.iexapis.com/stable/stock/"+ str(t) + "/quote?token=pk_4c68895f25a94a97ba943173f0aa9638");
        try:
            dict={}
            res=json.loads(api_req.content)
            dict.update({"id":c[1],"ticker":res, "quantity": c[0]})
            stocks.append(dict)
        except Exception as e:
            res = e
        
    return render(request,"portfolio.html", {"stocks":stocks})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "stock is removed")
    return redirect("portfolio")