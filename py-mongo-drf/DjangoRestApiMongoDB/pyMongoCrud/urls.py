from django.conf.urls import url 
from pyMongoCrud import views 
from django.contrib import admin
from django.urls import path

 
urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/emps', views.getAllEmps),
    path('api/emp', views.createNewEmployee), 
    path('api/emps/<str:pk>', views.getEmpById)
]