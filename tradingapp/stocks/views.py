from django.shortcuts import render
import requests, json 
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
    print(stocks)
    return render(request,'home.html',{"api": stocks})

def portfolio(request):
    return render(request,"portfolio.html", {})
