# PythonDjangoProject
## Kurulum
1. Masaüstündeyken CMD terminalini açın ve ardından `git clone https://github.com/emir-yasin-akman/PythonDjangoProject.git` komutunu çalıştırın.

2. Ardından `cd PythonDjangoProject` komutunu çalıştırın.

3. Ardından `cd myProject` komutu ile ana proje klasörüne giriş yapın.

4. Daha sonra `python -m venv sanal_ortam` komutu ile sanal ortamınızı oluşturun.

5. Devamında `sanal_ortam\Scripts\activate.bat` komutu ile sanal ortamınızı aktif edin.

6. Sanal ortamın aktif olduğunu anlamak için cmp terminalinde satırın en başında parantez içinde yazan (sanal_ortam) ibaresini görürseniz sanal ortamınız aktif demektir.

7. Ardından gerekli kütüphaneleri kurmak için `pip install -r requirements.txt` komutunu çalıştırın. Bu komut sayesinde projenin gerektirdiği tüm kütüphaneler sanal ortamınızın içerisine kurulacaktır.

8. `.env.example` dosyasını `.env` olarak yeniden adlandırın.

9. `.env` dosyasını açın ve kendi API key'inizi yazın:

   Dosya içerisinde yer alan `GROQ_API_KEY=buraya_kendi_key_inizi_yazın` alanı kendi API key'iniz ile değiştirin.

   ÖNEMLİ NOT : Eğer bu alanı uygulamazsanız proje sorunsuz olarak çalışır ancak yapay zeka sistemi bizim eğittiğimiz şekilde mesajlar vermek yerine otomatik ayarladığımız mesajları gönderir o yüzden bu alan çok kritiktir. API keyi nasıl alacağınız bir sonraki adımda detaylıca anlatılmıştır.
   
10. Groq API key almak için:
   - https://console.groq.com adresine gidin
   - Ücretsiz hesap oluşturun
   - API Keys menüsünden yeni key oluşturun
   - Oluşturulan key'i `.env` dosyasına bir önceki adımda anlatıldığı şekilde yapıştırın
   
11. Sunucuyu başlatın:

   - `python manage.py runserver` komutu ile projeyi ayağa kaldırın.
   - Onay mesajı geldikten sonra verilen adrese gittiğinizde projeyi başarılı bir şekilde çalıştırmış olacaksınız.

