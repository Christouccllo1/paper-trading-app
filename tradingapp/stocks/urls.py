from django.urls import path
from . import views 



urlpatterns = [
    path("",views.home, name="home"),
    path("add stock", views.add_stock, name = "add_stock"), 
    path("portfolio", views.portfolio, name="portfolio")
]