import nlpaug.augmenter.word as naw
from dataset import data # Sizin 250 satırlık orijinal veri setiniz
import os

print("--- VERİ ÇOĞALTMA İŞLEMİ BAŞLIYOR ---")
print("BERTürk modeli indiriliyor/yükleniyor (Bu işlem ilk seferde 1-2 dakika sürebilir)...")

# Bağlamsal kelime değişimi (Contextual Word Embedding) için BERTürk modelini kullanıyoruz
# aug_p=0.3 -> Cümledeki kelimelerin %30'unu eş anlamlısı/bağlamdaşı ile değiştirir.
aug = naw.ContextualWordEmbsAug(
    model_path='dbmdz/bert-base-turkish-cased',
    action="substitute",
    aug_p=0.3
)

genisletilmis_veri = []

# Orijinal verileri kaybetmemek için önce onları yeni listeye ekliyoruz
for metin, etiket in data:
    genisletilmis_veri.append((metin, etiket))

    # Nötr (2) etiketli verilerimiz çok az olduğu için onlardan 5 tane,
    # diğerlerinden (0 ve 1) 3'er tane kopya üretiyoruz.
    kac_kopya = 5 if etiket == 2 else 3

    # Yapay zeka orijinal metni okuyup yeni varyasyonlar üretiyor
    uretilen_metinler = aug.augment(metin, n=kac_kopya)

    for yeni_metin in uretilen_metinler:
        # Üretilen metni, orijinal metnin etiketiyle listeye ekle
        genisletilmis_veri.append((yeni_metin, etiket))

print(f"✅ Çoğaltma Tamamlandı! Orijinal {len(data)} satır veri, {len(genisletilmis_veri)} satıra ulaştı.")

# --- YENİ VERİYİ DOSYAYA YAZDIRMA ---
cikis_dosyasi = "dataset_genisletilmis.py"
with open(cikis_dosyasi, "w", encoding="utf-8") as f:
    f.write("data = [\n")
    for metin, etiket in genisletilmis_veri:
        # Metinlerin içindeki olası tırnak işaretlerini temizleyerek yazıyoruz
        temiz_metin = metin.replace('"', "'")
        f.write(f'    ("{temiz_metin}", {etiket}),\n')
    f.write("]\n")

print(f"💾 Yeni veri setiniz '{cikis_dosyasi}' adıyla projeye kaydedildi!")