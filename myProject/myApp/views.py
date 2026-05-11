from django.shortcuts import redirect, render, get_object_or_404
from .models import Hedef, SecilenHedef, HedefNot
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone  # Notun ne zaman yazıldığını kontrol etmek için
from datetime import timedelta     # Son 7 günü hesaplayabilmek için
import joblib  # Yapay zekayı (pkl dosyalarını) yüklemek için gerekli
import os # Dosya yollarını güvenli şekilde bulmak için gerekli
from groq import Groq  # Groq AI bağlantısı için
from dotenv import load_dotenv       # API anahtarını güvenli okumak için
from pathlib import Path

# --- .env YAPILANDIRMASI ---
load_dotenv(Path(__file__).resolve().parent.parent / '.env')
 
 
# --- YAPAY ZEKA MODELİNİN SİSTEME YÜKLENMESİ ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # BASE_DIR, projenin ana klasörünü (myProject) temsil eder.
model_path = os.path.join(BASE_DIR, 'duygu_modeli.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'vectorizer.pkl')
 
try:   # Eğitilen 'beyin' ve 'sözlük' dosyaları belleğe alınıyor
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("Yapay Zeka Modeli Başarıyla Yüklendi!")
except Exception as e:
    print(f"HATA: Yapay zeka dosyaları yüklenemedi: {e}")
 
 
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
    print("--- DEBUG: not_ekle FONKSİYONUNA GİRİLDİ! ---")
    if request.method == 'POST':
        hedef_id = request.POST.get('secilen_hedef_id')
        metin = request.POST.get('not_metni')
        print(f"--- [VERİ] Gelen ID: {hedef_id}, Metin: {metin[:20]}...")
        
        if hedef_id and metin:
            try:
                # --- 1. DUYGU ANALİZİ VE 5 ÜZERİNDEN PUANLAMA ---
                vektor = vectorizer.transform([metin])  # Kullanıcının yazdığı notu yapay zekanın anlayacağı sayısal vektöre çeviriyoruz
                tahmin = model.predict(vektor)[0]   # Modelin tahminini (0: Negatif, 1: Pozitif, 2:Nötr) alıyoruz
                olasiliklar = model.predict_proba(vektor)[0]  # Modelin 'olasılık' değerlerini alıyoruz (0.0 ile 1.0 arası bir güven oranı)
                poz_oran = olasiliklar[1]  # Pozitif olma ihtimali
 
                # SKORLAMA MANTIĞI (Neden bu sayıları seçtik?):
                # Amacımız 5 üzerinden bir ölçek oluşturmak. 3.0 puanı 'Nötr' kabul ettik.
                # GERÇEKÇİ VE HASSAS PUANLAMA SİSTEMİ
 
                if tahmin == 1:  # Pozitif tahmin
                    if poz_oran < 0.85:  # Model pozitif diyor ama pek emin değilse (Eh işte durumları)
                        duygu_skoru = round(2.0 + (poz_oran * 1.5), 1)  # 2.8 - 3.4 arası puan verir
                    else:  # Gerçekten pozitifse 3.5'ten başla ve 5.0'a doğru genişlet
                        duygu_skoru = round(3.0 + (poz_oran * 2.0), 1)
                elif tahmin == 0:  # Negatif tahmin
                    duygu_skoru = round(0.5 + (poz_oran * 4.5), 1)   # Negatifliği daha derin hissettir
                else:   # Nötr
                    duygu_skoru = 3.0
 
                final_skor = max(1.0, min(duygu_skoru, 5.0))   # 1.0 ile 5.0 arası sınır kontrolü
                print(f"--- [SKOR] Hesaplanan Skor: {final_skor}")
 
                s_hedef = get_object_or_404(SecilenHedef, id=hedef_id, user=request.user)
 
                # --- 2. HAFTALIK DEVAMLILIK HESAPLAMA ---
                # Hedef: Son 7 günde kaç gün not girildiğini bulmak.
                yedi_gun_once = timezone.now() - timedelta(days=7)
 
                # Veritabanında son 7 günü filtreliyoruz.
                # .dates('tarih', 'day') -> Aynı gün girilen 10 notu tek bir gün sayar.
                # .distinct() -> Farklı günleri netleştirir.
                haftalik_gun_sayisi = HedefNot.objects.filter(
                    user=request.user,
                    secilen_hedef=s_hedef,
                    tarih__gte=yedi_gun_once
                ).dates('tarih', 'day').distinct().count() + 1  # +1 bugünkü giriş için
 
                # --- 3. GROQ AI KOÇLUK MESAJI ---
                # Skora göre yedek mesajlar — AI çalışmazsa bunlar devreye girer
                if final_skor >= 4.0:
                    ai_mesajı = "Harika bir gün geçirdin, bu enerjiyi koru! 🔥"
                elif final_skor >= 3.0:
                    ai_mesajı = "İyi iş çıkardın, yarın daha da iyisini yapabilirsin! 💪"
                elif final_skor >= 2.0:
                    ai_mesajı = "Zor bir gündü ama yine de denedin, bu önemli! 🌱"
                else:
                    ai_mesajı = "Her gün yeni bir fırsat, yarın tekrar dene! ❤️"
 
                try:
                    print(">>> GROQ: Bağlantı kuruluyor...")
                    # API anahtarı .env dosyasından okunuyor
                    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
                    # AI'ya sadece duygu skorunu ve devamlılığı veriyoruz (notun içeriğini gizliyoruz)
                    prompt = f"""Sen samimi ve sıcak bir yaşam koçusun. Kullanıcıya kısa bir motivasyon mesajı yaz.

                    Bilgiler:
                    - Bugünkü başarı skoru: {final_skor}/5
                    - Bu hafta kaç gün devam etti: {haftalik_gun_sayisi} gün

                    Kurallar:
                    - Skoru veya gün sayısını mesajda DOĞRUDAN tekrar etme
                    - Samimi ve insan gibi konuş, robot gibi değil
                    - Maksimum 10 kelime
                    - Türkçe yaz
                    - Sadece mesajı yaz, tırnak işareti veya açıklama ekleme"""

                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=100,
                    )
 
                    ai_mesajı = completion.choices[0].message.content.strip()
                    print(">>> GROQ: Kişiselleştirilmiş mesaj alındı!")
 
                except Exception as ai_e:
                    print(f">>> GROQ HATASI: {ai_e}")
                    print(">>> GROQ: Yedek mesaj kullanılıyor.")
 
                # --- 4. VERİTABANINA KAYIT ---
                HedefNot.objects.create(
                    user=request.user,
                    secilen_hedef=s_hedef,
                    not_metni=metin,
                    duygu_skoru=final_skor,  # Hesapladığımız puanı veritabanına gönderiyoruz!
                    ai_motivasyon_notu=ai_mesajı  # AI'dan gelen mesajı buraya kaydediyoruz
                )
 
                print(f"KAYIT YAPILIYOR: Skor: {final_skor}, Devamlılık: {haftalik_gun_sayisi}")
                messages.success(request, f'Notunuz kaydedildi! Bugünlük Enerji Puanınız: {final_skor}/5')
                return redirect('analizlerim')
 
            except Exception as e:
                print(f"Hata Oluştu: {e}")
                messages.error(request, f'Bir teknik hata oluştu: {e}')
        else:
            messages.error(request, 'Lütfen not alanını boş bırakmayın.')
 
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