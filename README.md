# PythonDjangoProject
## Kurulum
1. Repoyu klonlayın

2. .env.example dosyasını kopyalayıp .env olarak yeniden adlandırın

3. .env dosyasını aç ve kendi API key'inizi yazın:
   GROQ_API_KEY=buraya_kendi_key_inizi_yazın
   
4. Groq API key almak için:
   - https://console.groq.com adresine gidin
   - Ücretsiz hesap oluşturun
   - API Keys menüsünden yeni key oluşturun
   - Oluşturulan key'i .env dosyasına yapıştırın

5. Gerekli olan kütüphaneleri kurun:
   - pip install django
   - pip install joblib
   - pip install groq
   - pip install dotenv
   - pip install scikit-learn
   - pip install transformers
   
7. Sunucuyu başlatın:
   - Öncelikle "cd myProject" komutu ile Proje dosyasının içine girin.
   - Ardından "python manage.py runserver" komutu ile sistemi çalıştırın.
   - Onay mesajları geldikten sonra verilen linkten web adresine gidin.
   - Proje çalıştırıldı.
  
