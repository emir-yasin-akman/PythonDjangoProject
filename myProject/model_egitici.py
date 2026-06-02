import joblib  # Eğitilen modeli dosyaya kaydetmek ve geri yüklemek için kullanılan kütüphane
<<<<<<< HEAD
from sklearn.feature_extraction.text import CountVectorizer  # Metinleri sayısal verilere dönüştüren araç
from sklearn.naive_bayes import MultinomialNB  # Olasılık tabanlı sınıflandırma algoritması (Yapay Zeka modeli) MultinomialNB 3 sınıfı destekler.
from dataset import data  # Hazırladığımız veri setini içe aktarıyoruz
=======
from sklearn.feature_extraction.text import TfidfVectorizer  # Metinleri sayısal verilere dönüştüren araç
from sklearn.svm import SVC  # Olasılık tabanlı sınıflandırma algoritması (Yapay Zeka modeli) MultinomialNB 3 sınıfı destekler.
from dataset_genisletilmis import data  # Hazırladığımız veri setini içe aktarıyoruz
>>>>>>> ozellik/ai-augmentation

# --- ADIM 1: VERİLERİ ÖN İŞLEME ---
# Dataset içerisindeki cümleleri ve bunlara karşılık gelen etiketleri (1: Pozitif, 0: Negatif, 2:Nötr) ayırıyoruz.
cumleler = [d[0] for d in data]  # Modelin öğreneceği metinler
etiketler = [d[1] for d in data] # Metinlerin duygu karşılıkları (Hedef değişken)

# --- ADIM 2: METİN VEKTÖRLEŞTİRME (Sayısal Dönüşüm) ---
# Bilgisayarlar kelimeleri anlayamaz, bu yüzden her cümleyi bir sayı matrisine çeviriyoruz.
# CountVectorizer: Cümledeki kelimelerin frekansını (geçiş sıklığını) hesaplar.
<<<<<<< HEAD
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(cumleler)  # Cümleleri matematiksel birer vektöre dönüştürdük

# --- ADIM 3: MODEL EĞİTİMİ (Yapay Zeka Süreci) ---
# Multinomial Naive Bayes algoritmasını seçtik çünkü metin sınıflandırma (NLP) işlerinde 
# hızlı ve yüksek doğruluk oranına sahip bir algoritmadır.
model = MultinomialNB()
=======
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X = vectorizer.fit_transform(cumleler)  # Cümleleri matematiksel birer vektöre dönüştürdük

# --- ADIM 3: MODEL EĞİTİMİ (Yapay Zeka Süreci) ---
# kernel='linear' diyerek LinearSVC ile aynı mantıkta çalışmasını sağlıyoruz.
# probability=True diyerek predict_proba() fonksiyonunu aktif ediyoruz!
model = SVC(kernel='linear', probability=True)

>>>>>>> ozellik/ai-augmentation
model.fit(X, etiketler)  # 'fit' komutuyla modelin cümleler ve duygular arasındaki ilişkiyi öğrenmesini sağladık

# --- ADIM 4: MODELİ VE VEKTÖRLEŞTİRİCİYİ PAKETLEME ---
# Eğitim bittikten sonra bu "beyni" dondurup saklamamız gerekiyor. 
# Böylece Django projesinde her seferinde yeniden eğitmek yerine direkt dosyadan okuyabileceğiz.
joblib.dump(model, 'duygu_modeli.pkl')        # Öğrenmiş algoritmayı kaydet
joblib.dump(vectorizer, 'vectorizer.pkl')    # Kelime sözlüğünü (vektörleştiriciyi) kaydet

# --- ADIM 5: BİLGİLENDİRME ---
print("------------------------------------------")
print("BAŞARILI: Yapay Zeka Modeli Eğitildi!")
print(f"Toplam {len(data)} örnek cümle üzerinden öğrenme sağlandı.")
print("Model Dosyaları: 'duygu_modeli.pkl' ve 'vectorizer.pkl' başarıyla oluşturuldu.")
print("------------------------------------------")