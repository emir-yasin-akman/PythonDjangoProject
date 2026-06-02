from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "account/login.html", {"error": "Geçersiz kullanıcı adı veya şifre."})
    return render(request, "account/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        repassword = request.POST["repassword"]
        
        if password != repassword:
            return render(request, "account/register.html", {"error": "Şifreler eşleşmiyor."})
        else:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {"error": "Bu kullanıcı adı zaten alınmış."})
            elif User.objects.filter(email=email).exists():
                return render(request, "account/register.html", {"error": "Bu email zaten kayıtlı."})
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect("login")
    return render(request, 'account/register.html')

def logout_view(request):
    logout(request)
    return redirect("home")
