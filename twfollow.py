#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Modülleri İçeri Aktar
import urllib2, mechanize
import os, time
import re, sqlite3

#Sabitler
twitter_giris = "https://mobile.twitter.com/login"
twitter_cikis = "https://mobile.twitter.com/logout"
twitter_tweet = "https://mobile.twitter.com/tweet"
twitter_takipci = "https://mobile.twitter.com/"
twitter_kontrol = "https://twitter.com/settings/account"
sinir_cizgisi1 = "-"*30
sinir_cizgisi2 = "-"*20
proxy_listesi = []
takip_kontrol = []
proxy_listesi_es = ['113.255.61.57:80', '108.58.186.227:3128', '60.251.46.23:3128', '222.188.100.203:8086', '113.215.0.130:82', '125.209.91.190:8080', '202.145.3.242:8080', '179.124.212.139:80', '119.252.174.210:8080', '218.29.111.106:9999', '191.102.115.66:8080', '128.199.164.105:8888', '177.234.0.110:3130', '117.135.241.80:8080', '137.116.91.232:3128', '40.113.124.17:3128', '23.101.69.141:3128', '58.253.238.242:80', '123.59.12.25:80', '104.209.187.151:3128', '60.219.24.125:3128', '177.47.238.18:8080', '58.147.174.167:8080', '104.171.126.86:8089', '211.72.13.116:3128', '117.135.241.80:8080', '125.39.17.91:3128', '177.234.0.110:3130', '219.142.192.196:42969', '185.93.54.194:3128', '181.49.221.6:8080', '192.3.90.124:3128', '195.34.238.154:8080', '123.125.114.167:80', '124.240.187.84:82', '23.101.69.141:3128', '117.136.234.18:81', '218.29.155.198:9999', '83.241.46.175:8080', '212.78.211.173:80', '219.142.192.196:212', '194.154.128.65:8080', '219.142.192.196:42969', '185.93.54.194:3128', '181.49.221.6:8080', '192.3.90.124:3128', '195.34.238.154:8080', '123.125.114.167:80', '124.240.187.84:82', '23.101.69.141:3128', '117.136.234.18:81', '218.29.155.198:9999', '83.241.46.175:8080', '212.78.211.173:80', '219.142.192.196:212', '194.154.128.65:8080', '219.142.192.196:39475', '92.255.174.88:80', '124.240.187.79:80', '112.1.185.108:8123', '162.248.240.137:3127', '80.98.162.102:8080', '112.95.190.144:9999', '122.96.59.105:82', '40.113.124.17:3128', '192.3.90.124:3128', '92.50.188.98:8080', '89.46.233.100:8081', '61.174.10.22:8080', '207.28.38.3:3128']

#Renk Kodları
bold = "\033[1m"
underline = "\033[4m"
green = "\033[92m"
blue = "\033[94m"
yellow = "\033[93m"
red = "\033[91m"
endcolor = "\033[0m"

#Veri Tabanı Bağlantısı
if os.path.exists("esdata.db") == True:
	veritabani = sqlite3.connect("esdata.db")
	imlec = veritabani.cursor()
	print sinir_cizgisi1
	print bold+blue+"[+] Veri Tabanı Bağlantısı Sağlandı"+endcolor
	print sinir_cizgisi1
	time.sleep(2)
else:
	print sinir_cizgisi1
	print bold+red+"[-] Veri Tabanı Bulunamadı"+endcolor
	print "[*] Veri Tabanı Oluşturuluyor"
	time.sleep(2)
	veritabani = sqlite3.connect("esdata.db")
	imlec = veritabani.cursor()
	print bold+blue+"[+] Veri Tabanı Oluşturuldu"+endcolor
	print "[*] Veri Tabanı - Tablolar Oluşturuluyor"
	time.sleep(2)
	imlec.execute("CREATE TABLE hesaplar(hesap_id INTEGER PRIMARY KEY AUTOINCREMENT, hesap_mail TEXT, hesap_sifre TEXT)")
	print bold+blue+"[+] Veri Tabanı Tablolar Oluşturuldu"+endcolor
	print sinir_cizgisi1
	time.sleep(2)

#Tarayıcı Bilgileri
tarayici = mechanize.Browser()
tarayici.set_handle_robots(False)
tarayici.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)')]

#Proxy Güncelleme
def proxy_guncelle():
	print bold+green+"[+] Proxy Listesi Güncelleniyor, Bu İşlem Bir Kaç Dakika Sürebilir..."+endcolor
	try:
		sayac = 0
		while sayac < 5:

			web_site = urllib2.urlopen("http://proxy-list.org/english/index.php?p=1")
			kaynak_kod = web_site.read()
			proxy_adresleri = re.findall('<li class="proxy">(.*?)</li>', kaynak_kod)
			for proxy in proxy_adresleri:
				if proxy == "Proxy":
					continue
				proxy_listesi.append(proxy)
			sayac += 1
			time.sleep(30)
	except:
		print red+bold+"[!] Hata | İnternet Bağlantısı Yok"+endcolor
	print bold+blue+"[+] Proxy Listesi Güncellendi"+endcolor

#Fonksiyonlar
def proxy_goruntule():
	for proxy in proxy_listesi:
		print proxy

def hesap_guncelle(dosya_isim):
	try:
		hesap_dosyasi = open(dosya_isim, "r")
		hesap_listesi = hesap_dosyasi.readlines()
		for hesap in hesap_listesi:
			hesap =  hesap.rsplit()
			hesap = hesap[0]
			sonuclar = hesap.partition(":")
			eposta, nokta, sifre = sonuclar
			imlec.execute("""INSERT INTO hesaplar (hesap_mail, hesap_sifre) VALUES ("{}", "{}")""".format(eposta, sifre))
	except IOError:
		print red+"[!] Hata | "+bold+dosya_isim+endcolor+red+" Dosyası Bulunamadı"+endcolor
	finally:
		veritabani.commit()

def hesap_goruntule():
	imlec.execute("""SELECT * FROM hesaplar""")
	hesaplar = imlec.fetchall()
	for hesap in hesaplar:
		idno, eposta, sifre = hesap
		print """Hesap ID: {} | Hesap Mail: {} | Hesap Password: {}""".format(idno, eposta, sifre) 

def twitter_takip(kadi, baslangic, bitis):
	sayac = 0
	sayac2 = 0
	sayac3 = 0
	print "Başlangıç Saati: "+time.strftime("%H:%M:%S")
	imlec.execute("""SELECT * FROM hesaplar WHERE hesap_id BETWEEN {} and {}""".format(baslangic, bitis))
	hesaplar = imlec.fetchall()
	devir = (bitis-baslangic)/30
	for hesap in hesaplar:
		sayac += 1
		idno, eposta, sifre = hesap
		if eposta in takip_kontrol:
			pass
		else:
			#Devri Başlat
			#Tarayıcıyı Başlat
			tarayici = mechanize.Browser()
			if sayac3 == devir:
				sayac2 += 1
				sayac3 = 0
			tarayici.set_proxies({"http://":proxy_listesi[sayac2]})
			tarayici.set_handle_robots(False)
			tarayici.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)')]
			tarayici.open(twitter_giris)
			tarayici.select_form(nr=0)
			tarayici['session[username_or_email]'] = eposta
			tarayici['session[password]'] = sifre
			tarayici.submit()
			kaynak = tarayici.open(twitter_kontrol).read()
			if eposta.encode("utf-8") in kaynak:
				tarayici.open(twitter_takipci+kadi)
				tarayici.select_form(nr=0)
				tarayici.submit()
				tarayici.open(twitter_cikis)
				tarayici.select_form(nr=0)
				tarayici.submit()
				print "Devir Saati: "+time.strftime("%H:%M:%S")+" | Kişi Sıralaması: "+str(sayac)
				sayac3 += 1
			else:
				print (red+bold+"[!] Hata | {} ID Hesabına Giriş Yapılamadı"+endcolor).format(idno)
		takip_kontrol.append(eposta)
	print bold+yellow+"Toplam Takipçi: "+endcolor+str(sayac)

print "(1) Proxy Güncelle (2) Mevcut Proxy Listesi Kullan"
secenek = raw_input("Seçenek: ")
if secenek == "1":
	proxy_guncelle()
else:
	proxy_listesi = proxy_listesi_es

#Kullanıcıyı Karşıla
print sinir_cizgisi2
print bold+yellow+"Twitter Takipçi / Tweet Programına Hoş Geldiniz"+endcolor
print sinir_cizgisi2
imlec.execute("""SELECT COUNT(DISTINCT(hesap_mail)) FROM hesaplar""")
sayi = imlec.fetchall()
if sayi == 0:
	print red+bold+"Veri Tabanınızda Hiç Hesap Yok, Lütfen Güncelleyin!"+endcolor
else:
	print (green+bold+"Veri Tabanınızda {} Kullanıcı Mevcut (Tekrarlar Hariç)"+endcolor).format(sayi)

print sinir_cizgisi2
print "Lütfen Yapılacak İşlemi Seçin"
print "\t (1) Takipçi Kasma"
print "\t (2) Friend Feed (De Aktif)"
print "\t (3) Hesap Veri Tabanını Güncelle"
print "\t (4) Hesap Veri Tabanı Görüntüle"
print "\t (5) Proxy Listesi Görüntüle"
print "\t (6) Yardım"
print "\t (q) Çıkış Yap"
islem = raw_input("İşlem: ")
while islem != "q":
	if islem == "1":
		print sinir_cizgisi2
		kadi = raw_input("Takip Ettirilecek Kullanıcı Adı: ")
		baslangic = int(raw_input("ID Başlangıç: "))
		bitis = int(raw_input("ID Bitiş: "))
		twitter_takip(kadi, baslangic, bitis)
		print sinir_cizgisi2
	elif islem == "2":
		print sinir_cizgisi2
		print "[ :( ]Daha Aktif Değil..."
		print sinir_cizgisi2
	elif islem == "3":
		print sinir_cizgisi2
		dosya_isim = raw_input("Açılacak TXT Dosyası: ")
		hesap_guncelle(dosya_isim)
		print sinir_cizgisi2
	elif islem == "4":
		print sinir_cizgisi2
		hesap_goruntule()
		print sinir_cizgisi2
	elif islem == "5":
		print sinir_cizgisi2
		proxy_goruntule()
		print sinir_cizgisi2
	elif islem == "6":
		print sinir_cizgisi2
		print "TWFollow v1.0"
		print "Kodlama: ExitStars - BABAGGANH"
		print "Ekskilikler ve Hatalar Bir Sonra Ki Versiyonda Giderilecektir."
		print "İlk Kurulum İse VeriTabanı Oluşturulacaktır, Lütfen Veri tabanını Güncelleyiniz."
		print sinir_cizgisi2
	else:
		print sinir_cizgisi2
		print red+"[!] Hata | Böyle Bir Komut Yok! "+bold+"Çıkış Yapmak İçin q Giriniz"+endcolor
		print sinir_cizgisi2
	islem = raw_input("İşlem: ")
