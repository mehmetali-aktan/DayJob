from django.shortcuts import render, redirect
from .models import Kullanici, Calisan, Isletme, Ilan, Basvuru
from django.contrib import messages
from django.utils import timezone

def index(request):
    kullanici_ad = request.session.get('kullanici_ad')
    hesap_turu = request.session.get('hesap_turu')
    arama = request.GET.get('arama')


    Ilan.objects.filter(bitis_tarihi__lt=timezone.now(), aktif_mi=True).update(aktif_mi=False)


    ilanlar = Ilan.objects.filter(aktif_mi=True)

    if arama:
        ilanlar = ilanlar.filter(pozisyon__icontains=arama)
    ilanlar = ilanlar.order_by('-id')

    return render(request, 'index.html', {
        'kullanici_ad': kullanici_ad,
        'hesap_turu': hesap_turu,
        'ilanlar': ilanlar
    })

def kayit(request):

    if request.method == 'POST':

        ad = request.POST.get('ad')

        soyad = request.POST.get('soyad')

        dogum_tarihi = request.POST.get('dogum_tarihi')

        email = request.POST.get('email')
        if Kullanici.objects.filter(email=email).exists():
            return render(request, 'kayit.html', {'hata': 'Bu e-posta zaten kullanımda.'})

        sifre = request.POST.get('sifre')

        telefon = request.POST.get('telefon')

        hesap_turu = request.POST.get('hesap_turu')

        kullanici = Kullanici.objects.create(

            ad=ad,

            soyad=soyad,

            dogum_tarihi=dogum_tarihi,

            email=email,

            sifre=sifre,

            telefon=telefon,

            hesap_turu=hesap_turu

        )

        # ÇALIŞAN

        if hesap_turu == 'calisan':

            boy = request.POST.get('boy')

            kilo = request.POST.get('kilo')

            cinsiyet = request.POST.get('cinsiyet')

            meslekler = request.POST.get('meslekler')

            foto = request.FILES.get('foto')

            Calisan.objects.create(

                kullanici=kullanici,

                boy=boy,

                kilo=kilo,

                cinsiyet=cinsiyet,

                meslekler=meslekler,

                foto=foto

            )

        # İŞLETME

        if hesap_turu == 'isletme':

            isletme_adi = request.POST.get('isletme_adi')

            isletme_adresi = request.POST.get('isletme_adresi')

            isletme_tipi = request.POST.get('isletme_tipi')

            aranan_meslekler = request.POST.get('aranan_meslekler')

            Isletme.objects.create(

                kullanici=kullanici,

                isletme_adi=isletme_adi,

                isletme_adresi=isletme_adresi,

                isletme_tipi=isletme_tipi,

                aranan_meslekler=aranan_meslekler

            )

        return redirect('/giris/')

    return render(request, 'kayit.html')

def login(request):

    hata = ''

    if request.method == 'POST':

        email = request.POST.get('email')
        sifre = request.POST.get('sifre')

        kullanici = Kullanici.objects.filter(
            email=email,
            sifre=sifre
        ).first()

        if kullanici:

            request.session['kullanici_id'] = kullanici.id

            request.session['hesap_turu'] = kullanici.hesap_turu

            request.session['kullanici_ad'] = kullanici.ad

            return redirect('/')

        else:
            hata = 'E-Mail veya şifre yanlış.'

    return render(request, 'login.html', {
        'hata': hata
    })

def cikis(request):

    request.session.flush()

    return redirect('/')

def ilan_ver(request):
    kullanici_id = request.session.get('kullanici_id')

    if not kullanici_id:
        return redirect('/giris/')

    kullanici = Kullanici.objects.get(id=kullanici_id)

    if kullanici.hesap_turu == 'calisan':
        messages.error(request, "Çalışan hesapları ilan veremez!")
        return redirect('/')

    if request.method == 'POST':
        isletme = Isletme.objects.get(kullanici=kullanici)
        # ... geri kalan kodlar aynı şekilde devam edecek ...


    

    if request.method == 'POST':

        kullanici_id = request.session.get('kullanici_id')

        kullanici = Kullanici.objects.get(id=kullanici_id)

        isletme = Isletme.objects.get(kullanici=kullanici)

        isletme_adi = request.POST.get('isletme_adi')

        isletme_tipi = request.POST.get('isletme_tipi')

        pozisyon = request.POST.get('pozisyon')

        is_tanimi = request.POST.get('is_tanimi')

        konum = request.POST.get('konum')

        yas_araligi = request.POST.get('yas_araligi')

        deneyim = request.POST.get('deneyim')

        cinsiyet = request.POST.get('cinsiyet')

        yemek = request.POST.get('yemek')

        ulasim = request.POST.get('ulasim')

        sigorta = request.POST.get('sigorta')

        kisi_sayisi = request.POST.get('kisi_sayisi')

        baslangic_tarihi = request.POST.get('baslangic_tarihi')

        bitis_tarihi = request.POST.get('bitis_tarihi')

        ucret = request.POST.get('ucret')

        Ilan.objects.create(

            isletme=isletme,

            isletme_adi=isletme_adi,

            isletme_tipi=isletme_tipi,

            pozisyon=pozisyon,

            is_tanimi=is_tanimi,

            konum=konum,

            yas_araligi=yas_araligi,

            deneyim=deneyim,

            cinsiyet=cinsiyet,

            yemek=yemek,

            ulasim=ulasim,

            sigorta=sigorta,

            kisi_sayisi=kisi_sayisi,

            baslangic_tarihi=baslangic_tarihi,

            bitis_tarihi=bitis_tarihi,

            ucret=ucret

        )

        return redirect('/')

    return render(request, 'ilan_ver.html')

def ilan_detay(request, ilan_id):

    ilan = Ilan.objects.get(id=ilan_id)

    basvurdu_mu = False

    kullanici_id = request.session.get('kullanici_id')

    if kullanici_id:

        basvurdu_mu = Basvuru.objects.filter(
            kullanici_id=kullanici_id,
            ilan=ilan
        ).exists()

    return render(
        request,
        'ilan_detay.html',
        {
            'ilan': ilan,
            'basvurdu_mu': basvurdu_mu
        }
    )

def basvur(request, ilan_id):

    kullanici_id = request.session.get('kullanici_id')

    if not kullanici_id:
        return redirect('/giris/')

    kullanici = Kullanici.objects.get(
        id=kullanici_id
    )

    if kullanici.hesap_turu == 'isletme':
        messages.error(request, "İşveren hesapları ilanlara başvuru yapamaz!")
        return redirect(f'/ilan/{ilan_id}/')

    ilan = Ilan.objects.get(
        id=ilan_id
    )

    mevcut = Basvuru.objects.filter(
        kullanici=kullanici,
        ilan=ilan
    ).exists()

    if not mevcut:

        Basvuru.objects.create(
            kullanici=kullanici,
            ilan=ilan
        )
        messages.success(request, f"{ilan.pozisyon} ilanına başvurunuz başarıyla alındı! 🎉")

    return redirect('/')

def basvurular(request):
    kullanici_id = request.session.get('kullanici_id')
    if not kullanici_id: 
        return redirect('/giris/')

    kullanici = Kullanici.objects.get(id=kullanici_id)
    if kullanici.hesap_turu != 'isletme': 
        return redirect('/')

    # Henüz işlem yapılmamış aktif başvurular (Beklemede)
    aktif_basvurular = Basvuru.objects.select_related('kullanici', 'ilan').filter(
        ilan__isletme__kullanici=kullanici,
        durum='Beklemede'
    ).order_by('-id')

    # Onaylanmış veya reddedilmiş geçmiş başvurular (Pasif)
    gecmis_basvurular = Basvuru.objects.select_related('kullanici', 'ilan').filter(
        ilan__isletme__kullanici=kullanici
    ).exclude(durum='Beklemede').order_by('-id')

    return render(
        request, 
        'basvurular.html', 
        {
            'aktif_basvurular': aktif_basvurular, 
            'gecmis_basvurular': gecmis_basvurular
        }
    )

def panel(request):
    kullanici_id = request.session.get('kullanici_id')
    if not kullanici_id: 
        return redirect('/giris/')

    kullanici = Kullanici.objects.get(id=kullanici_id)
    if kullanici.hesap_turu != 'isletme': 
        return redirect('/')

    isletme = Isletme.objects.get(kullanici=kullanici)


    Ilan.objects.filter(bitis_tarihi__lt=timezone.now(), aktif_mi=True).update(aktif_mi=False)


    ilanlar = Ilan.objects.filter(isletme=isletme, aktif_mi=True)
    gecmis_ilanlar = Ilan.objects.filter(isletme=isletme, aktif_mi=False).order_by('-id')

    toplam_ilan = Ilan.objects.filter(isletme=isletme).count()
    toplam_basvuru = Basvuru.objects.filter(ilan__isletme=isletme).count()

    return render(request, 'panel.html', {
        'isletme': isletme, 
        'ilanlar': ilanlar, 
        'gecmis_ilanlar': gecmis_ilanlar,
        'toplam_ilan': toplam_ilan, 
        'toplam_basvuru': toplam_basvuru
    })

def basvuru_onayla(request, basvuru_id):
    basvuru = Basvuru.objects.get(id=basvuru_id)
    basvuru.durum = 'Onaylandı'
    basvuru.save()


    ilan = basvuru.ilan
    ilan.aktif_mi = False
    ilan.save()

    return redirect('/')


def basvuru_reddet(request, basvuru_id):

    basvuru = Basvuru.objects.get(
        id=basvuru_id
    )

    basvuru.durum = 'Reddedildi'

    basvuru.save()

    return redirect('/basvurular/')

def basvurularim(request):
    kullanici_id = request.session.get('kullanici_id')
    if not kullanici_id: return redirect('/giris/')

    kullanici = Kullanici.objects.get(id=kullanici_id)
    if kullanici.hesap_turu != 'calisan': return redirect('/')

    # BAŞVURULARI İKİYE BÖLDÜK
    aktif_basvurular = Basvuru.objects.filter(kullanici=kullanici, ilan__aktif_mi=True).select_related('ilan').order_by('-id')
    gecmis_basvurular = Basvuru.objects.filter(kullanici=kullanici, ilan__aktif_mi=False).select_related('ilan').order_by('-id')

    return render(request, 'basvurularim.html', {
        'aktif_basvurular': aktif_basvurular, 'gecmis_basvurular': gecmis_basvurular
    })

def profil(request):

    kullanici_id = request.session.get('kullanici_id')

    if not kullanici_id:
        return redirect('/giris/')

    kullanici = Kullanici.objects.get(
        id=kullanici_id
    )

    if kullanici.hesap_turu != 'calisan':
        return redirect('/')
    
    calisan = Calisan.objects.get(
        kullanici=kullanici
    )

    toplam_basvuru = Basvuru.objects.filter(
        kullanici=kullanici
    ).count()

    onaylanan = Basvuru.objects.filter(
        kullanici=kullanici,
        durum='Onaylandı'
    ).count()

    return render(
        request,
        'profil.html',
        {
            'kullanici': kullanici,
            'calisan': calisan,
            'toplam_basvuru': toplam_basvuru,
            'onaylanan': onaylanan
        }
    )

def ilan_sil(request, ilan_id):

    kullanici_id = request.session.get(
        'kullanici_id'
    )

    if not kullanici_id:
        return redirect('/giris/')

    kullanici = Kullanici.objects.get(
        id=kullanici_id
    )

    ilan = Ilan.objects.get(
        id=ilan_id
    )

    if ilan.isletme.kullanici != kullanici:
        return redirect('/')

    ilan.delete()

    return redirect('/panel/')

def ilan_duzenle(request, ilan_id):

    ilan = Ilan.objects.get(
        id=ilan_id
    )

    if request.method == 'POST':

        ilan.pozisyon = request.POST.get(
            'pozisyon'
        )

        ilan.ucret = request.POST.get(
            'ucret'
        )

        ilan.is_tanimi = request.POST.get(
            'is_tanimi'
        )

        ilan.save()

        return redirect('/panel/')

    return render(
        request,
        'ilan_duzenle.html',
        {
            'ilan': ilan
        }
    )

def calisan_detay(request, kullanici_id):

    kullanici = Kullanici.objects.get(
        id=kullanici_id
    )

    calisan = Calisan.objects.get(
        kullanici=kullanici
    )

    toplam_basvuru = Basvuru.objects.filter(
        kullanici=kullanici
    ).count()

    onaylanan = Basvuru.objects.filter(
        kullanici=kullanici,
        durum='Onaylandı'
    ).count()

    return render(
        request,
        'calisan_detay.html',
        {
            'kullanici': kullanici,
            'calisan': calisan,
            'toplam_basvuru': toplam_basvuru,
            'onaylanan': onaylanan
        }
    )

def basvuru_sil(request, basvuru_id):

    kullanici_id = request.session.get('kullanici_id')

    basvuru = Basvuru.objects.get(id=basvuru_id)

    if basvuru.kullanici.id == kullanici_id:

        basvuru.delete()

    return redirect('/basvurularim/')

def puanla_sayfasi(request):
    kullanici_id = request.session.get('kullanici_id')
    if not kullanici_id:
        return redirect('/giris/')
        
    kullanici = Kullanici.objects.get(id=kullanici_id)
    simdi = timezone.now()
    
    if kullanici.hesap_turu == 'isletme':
        # İşletmenin onayladığı, zamanı geçmiş ve henüz puanlamadığı başvurular
        bekleyen_puanlamalar = Basvuru.objects.filter(
            ilan__isletme__kullanici=kullanici,
            durum='Onaylandı',
            ilan__bitis_tarihi__lt=simdi,
            isletme_puanladi=False
        ).order_by('-id')
    else:
        # Çalışanın onaylandığı, zamanı geçmiş ve henüz puanlamadığı işletmeler
        bekleyen_puanlamalar = Basvuru.objects.filter(
            kullanici=kullanici,
            durum='Onaylandı',
            ilan__bitis_tarihi__lt=simdi,
            calisan_puanladi=False
        ).order_by('-id')
        
    return render(request, 'puanla.html', {
        'bekleyen_puanlamalar': bekleyen_puanlamalar,
        'kullanici': kullanici
    })

def puan_ver(request, basvuru_id):
    if request.method == 'POST':
        kullanici_id = request.session.get('kullanici_id')
        if not kullanici_id: return redirect('/giris/')
        
        kullanici = Kullanici.objects.get(id=kullanici_id)
        basvuru = Basvuru.objects.get(id=basvuru_id)
        verilen_puan = int(request.POST.get('puan', 0))
        
        if 1 <= verilen_puan <= 5:
            # İŞLETME -> ÇALIŞANI PUANLIYOR
            if kullanici.hesap_turu == 'isletme' and basvuru.ilan.isletme.kullanici == kullanici and not basvuru.isletme_puanladi:
                calisan = basvuru.kullanici.calisan
                toplam = (calisan.ortalama_puan * calisan.puan_sayisi) + verilen_puan
                calisan.puan_sayisi += 1
                calisan.ortalama_puan = toplam / calisan.puan_sayisi
                calisan.save()
                
                basvuru.isletme_puanladi = True
                basvuru.save()
                messages.success(request, f"{calisan.kullanici.ad} kullanıcısını başarıyla puanladınız!")
                
            # ÇALIŞAN -> İŞLETMEYİ PUANLIYOR
            elif kullanici.hesap_turu == 'calisan' and basvuru.kullanici == kullanici and not basvuru.calisan_puanladi:
                isletme = basvuru.ilan.isletme
                toplam = (isletme.ortalama_puan * isletme.puan_sayisi) + verilen_puan
                isletme.puan_sayisi += 1
                isletme.ortalama_puan = toplam / isletme.puan_sayisi
                isletme.save()
                
                basvuru.calisan_puanladi = True
                basvuru.save()
                messages.success(request, f"{isletme.isletme_adi} işletmesini başarıyla puanladınız!")
                
    return redirect('/') # Puanlama bitince otomatik anasayfaya atar