from django.urls import path
from . import views

app_name = 'claim'
urlpatterns = [
    path('loginClaims', views.claimsLogin, name='login-claims'),
    path('loginDoctor', views.doctorLogin, name='login-doctor'),
    path('', views.doctorLogin, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('doctor', views.doctorHome, name='doctor'),
    path('claims', views.claimsHome, name='claims'),

]
