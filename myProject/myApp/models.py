from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hedef(models.Model):
    baslik = models.CharField(max_length=100)
    ikon = models.CharField(max_length=100)
    aciklama = models.TextField()

    def __str__(self):
        return self.baslik
    
    class Meta:
        verbose_name = "Hedef"
        verbose_name_plural = "Hedefler"
        
class SecilenHedef(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hedef = models.ForeignKey(Hedef, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.hedef.baslik}"
    
    class Meta:
        verbose_name = "Seçilen Hedef"
        verbose_name_plural = "Seçilen Hedefler"
        
class HedefNot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secilen_hedef = models.ForeignKey(SecilenHedef, on_delete=models.CASCADE)
    not_metni = models.TextField()
    duygu_skoru = models.FloatField(null=True, blank=True) # BURAYI AI DOLDURACAK
    ai_motivasyon_notu = models.TextField(null=True, blank=True) # BURAYI AI DOLDURACAK
    tarih = models.DateTimeField(auto_now_add=True) # Ai motivasyon notunu duygu skoru ve devamlılığa bakarak ürettiğimiz için tarih eklendi.
    
    def __str__(self):
        return f"{self.user.username} - {self.secilen_hedef} için not"
    
    class Meta:
        verbose_name = "Hedef Notu"
        verbose_name_plural = "Hedef Notları"
