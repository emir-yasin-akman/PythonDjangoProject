# PythonDjangoProject
## Kurulum
1. Repoyu klonlayın

2. .env.example dosyasını .env olarak yeniden adlandırın

3. .env dosyasını açın ve kendi API key'inizi yazın:
   GROQ_API_KEY=buraya_kendi_key_inizi_yazın

   ÖNEMLİ NOT : Eğer bu alanı uygulamazsanız proje sorunsuz olarak çalışır ancak yapay zeka sistemi bizim eğittiğimiz şekilde mesajlar vermek yerine otomatik ayarladığımız mesajları gönderir o yüzden bu alan çok kritiktir. API keyi nasıl alacağınız bir sonraki adımda detaylıca anlatılmıştır.
   
5. Groq API key almak için:
   - https://console.groq.com adresine gidin
   - Ücretsiz hesap oluşturun
   - API Keys menüsünden yeni key oluşturun
   - Oluşturulan key'i .env dosyasına yapıştırın

6. Gerekli olan kütüphaneleri kurun (Tavsiye Edilen : Bir sonraki adımda sanal ortam içerisinde kurulum yapmanız daha sağlıklıdır.):
   - pip install django
   - pip install joblib
   - pip install groq
   - pip install dotenv
   - pip install scikit-learn
   - pip install transformers

7. Kütüphaneleri kurmadan sanal ortam içerisinde kurulum yapmak için:
   - Proje klasörünün içindeyken "python -m venv sanal_ortam" komutu ile sanal ortam oluşturun.
   - Ardından cmd kullanıyorsanız "sanal_ortam\Scripts\activate.bat" komutu ile sanal ortamınızı aktif edin.
   - Daha sonra "pip install -r requirements.txt" komutu ile projede kullanılan tüm kütüphaneleri kurun.
   - Onay mesajınız geldikten sonra gerekli olan tüm kütüphaneleri kurdunuz demektir.
   
8. Sunucuyu başlatın:
   - Öncelikle myProject klasörü içindeyken "manage.py" dosyasıyla aynı dizinde olduğunuza emin olun.
   - Ardından "python manage.py runserver" komutu ile sistemi çalıştırın.
   - Onay mesajları geldikten sonra verilen linkten web adresine gidin.
   - Proje çalıştırıldı.
  
