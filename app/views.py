from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.utils import timezone
from .models import Rapport
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone

# Create your views here.

def inscription(request):
    if request.method == 'POST': 
        username = request.POST.get('nom')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        if password == confirm :
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username,password=password)
                return redirect('connexion')
            else:
                messages.error(request,"Nom d'utilisateur deja pris !")
        else:
            messages.error(request,"Les deux mot de passe ne correspondent pas")        
    return render(request,"app/inscription.html")

def connexion(request):
    if request.method == 'POST': 
        username = request.POST.get('nom')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, "Le nom ou le mot de passe est invalide")
    return render(request,"app/connexion.html")

def deconnexion(request):
    logout(request)
    return redirect("connexion")

def accueil(request):
    now = timezone.now()
    days_since_friday = (now.weekday() - 4) % 7

    start_week = now - timedelta(days=days_since_friday)
    start_week = start_week.replace(hour=0,minute=0,second=0)

    end_week = start_week + timedelta(days=6,hours=23,minutes=59,seconds=59)

    somme_vente = Rapport.objects.filter(
        user=request.user,
        create_at__range=(start_week, end_week)
    ).aggregate(total=Sum('prix'))['total'] or 0

    date = timezone.now()
    context = {
        'date':date,
        'start_week':start_week,
        'end_week':end_week,
        'somme_vente':somme_vente
    }
    if request.method == "POST":
        prix = request.POST.get("prix")
        probleme = request.POST.get("probleme")
        contact = request.POST.get("contact")
        rapport = Rapport.objects.create(
            user=request.user,
            prix=prix,
            probleme=probleme,
            contact=contact
        )
        return redirect("accueil")
    return render(request,"app/accueil.html",context)

def userlist(request):
    users = User.objects.all()
    return render(request,'app/userlist.html',{'users':users})

def userrapport(request, user_id):
    user = get_object_or_404(User,id=user_id)
    rapports = Rapport.objects.filter(user=user).order_by('-create_at')
    now = timezone.now()
    days_since_friday = (now.weekday() - 4) % 7

    start_week = now - timedelta(days=days_since_friday)
    start_week = start_week.replace(hour=0,minute=0,second=0)

    end_week = start_week + timedelta(days=6,hours=23,minutes=59,seconds=59)

    somme_vente = Rapport.objects.filter(
        user=user,
        create_at__range=(start_week, end_week)
    ).aggregate(total=Sum('prix'))['total'] or 0
    return render(request,'app/userrapport.html',{
        'user':user,
        'rapports':rapports,
        'start_week':start_week,
        'end_week':end_week,
        'somme_vente':somme_vente
    })
