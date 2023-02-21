from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path("geonameid=<str:geonameid>/",  views.getinfo, name="geonameidpost"),
    path("page=<int:page>/items=<int:items_on_page>/", views.getinfopage),
    path("<str:namefstcity>or<str:namesndcity>/", views.two_city_north)
]
