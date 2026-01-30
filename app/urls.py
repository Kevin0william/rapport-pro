from django.urls import path
from . import views

urlpatterns = [
    path("",views.inscription,name="inscription"),
    path("connexion/",views.connexion,name="connexion"),
    path("deconnexion/",views.deconnexion,name="deconnexion"),
    path("accueil/",views.accueil,name="accueil"),
    path("userlist/",views.userlist,name="userlist"),
    path("users/<int:user_id>/rapport",views.userrapport,name="userrapport"),
]