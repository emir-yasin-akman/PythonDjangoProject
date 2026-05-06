from django.shortcuts import redirect, render, get_object_or_404
from .models import Hedef, SecilenHedef, HedefNot
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, 'myApp/home.html')


def hedef_sec(request):
    hedefler = Hedef.objects.all()
    secilen_hedefler = []
    if request.user.is_authenticated:
        secilen_hedefler = SecilenHedef.objects.filter(user=request.user).values_list('hedef_id', flat=True)
    context = {
        'hedefler': hedefler,
        'secilen_hedefler': secilen_hedefler
    }
    return render(request, 'myApp/hedef_sec.html', context)

@login_required
def hedef_ekle(request, hedef_id):
    hedef = Hedef.objects.get(id=hedef_id)
    SecilenHedef.objects.get_or_create(user=request.user, hedef=hedef)
    return redirect('hedef_sec')

@login_required
def hedef_sil(request, hedef_id):
    SecilenHedef.objects.filter(user=request.user, hedef_id=hedef_id).delete()
    return redirect('hedef_sec')


def hedeflerim(request):
    secilen_hedefler = []
    if request.user.is_authenticated:
        secilen_hedefler = SecilenHedef.objects.filter(user=request.user)
    return render(request, 'myApp/hedeflerim.html', {'secilen_hedefler': secilen_hedefler})

@login_required
def not_ekle(request):
    if request.method == 'POST':
        hedef_id = request.POST.get('secilen_hedef_id')
        metin = request.POST.get('not_metni')
        
        print(f"Gelen ID: {hedef_id}, Gelen Metin: {metin}") # Terminalde bunu kontrol et

        if hedef_id and metin:
            try:
                # Buradaki model ismi models.py ile aynı mı? (GunlukNot mu HedefNot mu?)
                s_hedef = get_object_or_404(SecilenHedef, id=hedef_id, user=request.user)
                HedefNot.objects.create(
                    user=request.user, 
                    secilen_hedef=s_hedef, 
                    not_metni=metin
                )
                messages.success(request, 'Notunuz başarıyla kaydedildi!')  
                return redirect('home')
            except Exception as e:
                print(f"Veritabanı Hatası: {e}") # Terminale hatayı basar
                messages.error(request, f'Hata: {e}')
        else:
            # Eğer buraya düşüyorsa HTML'deki 'name' değerleri yanlıştır
            print("Veriler formdan boş geldi!") 
            messages.error(request, 'Lütfen tüm alanları doldurun.')

    kullanicinin_hedefleri = SecilenHedef.objects.filter(user=request.user)
    return render(request, 'hedeflerim.html', {'secilen_hedefler': kullanicinin_hedefleri})

def analizlerim(request):
    secilen_hedefler = []
    if request.user.is_authenticated:
        secilen_hedefler = SecilenHedef.objects.filter(user=request.user)
    context = {
        'secilen_hedefler': secilen_hedefler
    }
    return render(request, 'myApp/analizlerim.html', context)

