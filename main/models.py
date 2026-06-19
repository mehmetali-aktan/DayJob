from django.db import models


# ORTAK KULLANICI

class Kullanici(models.Model):

    HESAP_TURU = (
        ('calisan', 'Çalışan'),
        ('isletme', 'İşletme'),
    )

    ad = models.CharField(max_length=100)

    soyad = models.CharField(max_length=100)

    dogum_tarihi = models.DateField()

    email = models.EmailField(unique=True)

    sifre = models.CharField(max_length=100)

    telefon = models.CharField(max_length=20)

    hesap_turu = models.CharField(
        max_length=20,
        choices=HESAP_TURU
    )

    def __str__(self):
        return self.ad


# ÇALIŞAN

class Calisan(models.Model):

    kullanici = models.OneToOneField(
        Kullanici,
        on_delete=models.CASCADE
    )

    boy = models.IntegerField()

    kilo = models.IntegerField()

    cinsiyet = models.CharField(max_length=50)

    meslekler = models.CharField(max_length=300)
    ortalama_puan = models.FloatField(default=0.0)
    puan_sayisi = models.IntegerField(default=0)

    foto = models.ImageField(
        upload_to='calisanlar/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.kullanici.ad


# İŞLETME

class Isletme(models.Model):

    kullanici = models.OneToOneField(
        Kullanici,
        on_delete=models.CASCADE
    )

    isletme_adi = models.CharField(max_length=200)

    isletme_adresi = models.CharField(max_length=300)

    isletme_tipi = models.CharField(max_length=100)

    aranan_meslekler = models.CharField(max_length=300)
    ortalama_puan = models.FloatField(default=0.0)
    puan_sayisi = models.IntegerField(default=0)

    def __str__(self):
        return self.isletme_adi
    
# İLAN

class Ilan(models.Model):
    
    isletme = models.ForeignKey(
    Isletme,
    on_delete=models.CASCADE,
    null=True
)

    isletme_adi = models.CharField(max_length=200)

    isletme_tipi = models.CharField(max_length=100)

    pozisyon = models.CharField(max_length=150)

    is_tanimi = models.TextField()

    konum = models.CharField(max_length=150)

    yas_araligi = models.CharField(max_length=100)

    deneyim = models.CharField(max_length=150)

    cinsiyet = models.CharField(max_length=50)

    yemek = models.CharField(max_length=20)

    ulasim = models.CharField(max_length=20)

    sigorta = models.CharField(max_length=20)

    kisi_sayisi = models.IntegerField()

    baslangic_tarihi = models.DateTimeField()

    bitis_tarihi = models.DateTimeField()

    ucret = models.IntegerField()
    aktif_mi = models.BooleanField(default=True)

    def __str__(self):
        return self.isletme_adi
    
class Basvuru(models.Model):

    kullanici = models.ForeignKey(
        Kullanici,
        on_delete=models.CASCADE
    )


    ilan = models.ForeignKey(
        Ilan,
        on_delete=models.CASCADE
    )

    basvuru_tarihi = models.DateTimeField(
        auto_now_add=True
    )

    durum = models.CharField(
        max_length=30,
        default='Beklemede'
    )
    isletme_puanladi = models.BooleanField(default=False)
    calisan_puanladi = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.kullanici.ad} - {self.ilan.isletme_adi}"