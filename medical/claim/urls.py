from django.urls import path
from . import views

app_name = 'claim'
urlpatterns = [
    path('loginClaims', views.claimsLogin, name='login-claims'),
    path('loginDoctor', views.doctorLogin, name='login-doctor'),
    path('', views.doctorLogin, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('doctor', views.doctorHome, name='doctor'),
    path('doctorClaim/<int:claim_id>', views.doctorHomeUpdate, name='claim-update'),
    path('claims', views.claimsHome, name='claims'),
    path('myclaims', views.myClaims, name='myclaims'),
    path('claimDetail/<int:claim_id>', views.claimDetail, name='detail'),
    path('claimSearch', views.search, name='search'),
    path('addDoctor', views.addDoctor, name='add-doctor'),
    path('doctorsList', views.doctorsList, name='doctors-list'),
    path('doctorUpdate/<int:doctor_id>', views.doctorUpdate, name='doctor-update'),
]
