import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
from flags import flags_list 

# Skor tutma

skor_dosyasi= "scores.txt"

# Skorları okuma
def skorlari_oku():
    
    skorlar = []
    try:
        with open(skor_dosyasi, "r", encoding="utf-8") as f:
            for satir in f:
                try:
                    isim, skor_puan = satir.strip().split(',')
                    skorlar.append((isim, int(skor_puan)))
                except ValueError:
                    continue
        skorlar.sort(key=lambda x: x[1], reverse=True)
        return skorlar
    except FileNotFoundError:
        return []
    
# Skoru kaydet ve güncelle
def skoru_kaydet(kullanici_adi, skor):
    skor_dict = {}
    try:
        for isim, puan in skorlari_oku():
            skor_dict[isim] = puan
    except Exception:
        pass

    mevcut = skor_dict.get(kullanici_adi)
    if mevcut is None or skor > mevcut:
        skor_dict[kullanici_adi] = skor

    try:
        sirali = sorted(skor_dict.items(), key=lambda x: x[1], reverse=True)
        with open(skor_dosyasi, "w", encoding="utf-8") as f:
            for isim, puan in sirali:
                f.write(f"{isim},{puan}\n")
    except Exception as e:
        print("Skor yazılırken hata:", e)

  
# En yüksek skoru getirme
def en_yuksek_skoru_getir():
    
    mevcut_skorlar = skorlari_oku()
    if not mevcut_skorlar:
        return ("Yok", 0)
    
    
    en_iyi = max(mevcut_skorlar, key=lambda x: x[1])
    return en_iyi 
    
# Menü Oluşturma

class Flagguess:
    
    def __init__(self, ana_pencere):
        self.ana_pencere = ana_pencere
        self.ana_pencere.title("Bayrak Tahmin Oyunu")
        self.ana_pencere.geometry("500x650") 
        
        self.kullanici_adi = ""
        self.skor = 0
        self.soru_index = 0
        self.kalan_sure = 10
        self.sayac_id = None
        self.oyun_verisi = []
        self.toplam_soru = 0
        self.dogru_cevap = ""
        self.ogeler = []
        

        self.kullanici_girisi = None
        self.skor_etiketi = None
        self.sayac_etiketi = None
        self.bayrak_etiketi = None
        self.soru_sayac_etiketi = None
        self.secenek_butonlari = []
        self.bayrak_resmi = None
        
        self.baslangic_ekranini_goster() 

    # Ekranı temizleme fonksiyonu
    def ekrani_temizle(self):
        
        if self.sayac_id:
            self.ana_pencere.after_cancel(self.sayac_id)
            self.sayac_id = None
            
        for oge in self.ogeler:
            oge.destroy()
            
        self.ogeler = []
        self.secenek_butonlari = []
    
    # Başlangıç ekranı fonksiyonu
    def baslangic_ekranini_goster(self):
       
        self.ekrani_temizle()

        try:
            img_path = "img/gorsel.jpeg"
            img = Image.open(img_path)
            img = img.resize((300, 220), Image.LANCZOS)  
            self.gorsel = ImageTk.PhotoImage(img)  # self ile sakla
            label_gorsel = tk.Label(self.ana_pencere, image=self.gorsel)
            self.ogeler.append(label_gorsel)  
        except Exception as e:
            print("Görsel yüklenemedi:", e)
        
        label1 = tk.Label(self.ana_pencere, text="Bayrak Tahmin Oyununa Hoşgeldin!", font=("Arial", 20, "bold"))

        en_isim, en_puan = en_yuksek_skoru_getir()
        if en_puan == 0 and en_isim == "Yok":
            yuksek_text = "Henüz kayıtlı skor yok."
        else:
            yuksek_text = f"En yüksek skor: {en_puan} — {en_isim} \n Bakalım geçebilecek misin?"

        label_yuksek = tk.Label(self.ana_pencere, text=yuksek_text, font=("Arial", 12, "bold"), fg="blue")
        

        kural_metni = "Doğru cevapları ne kadar erken bilirsen,\n o kadar çok puan kazanırsın!\n"
        label2 = tk.Label(self.ana_pencere, text=kural_metni, font=("Arial", 14))
        label3 = tk.Label(self.ana_pencere, text="Kullanıcı Adı:", font=("Arial", 14))
        self.kullanici_girisi = tk.Entry(self.ana_pencere, font=("Arial", 14), width=20)
        baslat_butonu = tk.Button(self.ana_pencere, text="OYUNA BAŞLA", font=("Arial", 16, "bold"),
                                  bg="white", fg="black", command=self.oyuncu_kontrol_ve_basla)
        
        label1.pack(pady=(40, 10))
        label2.pack(pady=10)
        label_yuksek.pack(pady=5)
        label_gorsel.pack(pady=10)
        label3.pack(pady=(40, 5))
        self.kullanici_girisi.pack(pady=5)
        baslat_butonu.pack(pady=20)
        
        self.ogeler.extend([label1, label2, label3, self.kullanici_girisi, baslat_butonu, label_gorsel, label_yuksek])

       
    # Oyuncu kontrol etme
    def oyuncu_kontrol_ve_basla(self):
        isim = self.kullanici_girisi.get().strip()
        if not isim:
            messagebox.showwarning("Uyarı", "Lütfen bir isim girin!")
            return
        
        self.kullanici_adi = isim
        
        # Kullanıcı kontrolü
        mevcut_dict = dict(skorlari_oku())
        
        if isim in mevcut_dict:
            eski_rekor = mevcut_dict[isim]
            messagebox.showinfo("Hoşgeldin!", f"Tekrar hoşgeldin {isim}!\nSenin En Yüksek Skorun: {eski_rekor}")
        else:
            messagebox.showinfo("Hoşgeldin!", f"Aramıza hoşgeldin {isim}!\nİyi şanslar.")

        # Oyun verisini hazırla
        toplam_bayrak = len(flags_list)
        soru_sayisi = min(20, toplam_bayrak)
        self.oyun_verisi = random.sample(flags_list, soru_sayisi) if soru_sayisi > 0 else []
        random.shuffle(self.oyun_verisi)

        self.oyun_ekranini_goster()


    # Oyun ekranını gösterme fonksiyonu
    def oyun_ekranini_goster(self):
        
        self.ekrani_temizle()
        
        self.skor = 0
        self.soru_index = 0
        self.toplam_soru = len(self.oyun_verisi)
        
        self.soru_sayac_etiketi = tk.Label(self.ana_pencere, text=f"Soru: 1 / {self.toplam_soru}", font=("Arial", 16))
        self.soru_sayac_etiketi.pack(pady=(10, 0))

        self.skor_etiketi = tk.Label(self.ana_pencere, text="Skor: 0", font=("Arial", 18))
        self.skor_etiketi.pack(pady=10)
        
        self.sayac_etiketi = tk.Label(self.ana_pencere, text="Süre: 10", font=("Arial", 20, "bold"), fg="red")
        self.sayac_etiketi.pack(pady=10)
        
        self.bayrak_etiketi = tk.Label(self.ana_pencere)
        self.bayrak_etiketi.pack(pady=10) 
        
        self.secenek_butonlari = []
        for i in range(4):
            btn = tk.Button(self.ana_pencere, text="", font=("Arial", 14), width=25) 

            btn.config(command=lambda i=i: self.cevabi_kontrol_et(self.secenek_butonlari[i]['text']))
            
            btn.pack(pady=3) 
            self.secenek_butonlari.append(btn)
        
        self.ogeler.extend([self.soru_sayac_etiketi, self.skor_etiketi, self.sayac_etiketi, self.bayrak_etiketi])
        self.ogeler.extend(self.secenek_butonlari) 
        
        self.sonraki_soru()

    # Sonraki soru fonksiyonu
    def sonraki_soru(self):
    
        if self.sayac_id:
            self.ana_pencere.after_cancel(self.sayac_id)

        if self.soru_index >= self.toplam_soru:
            self.oyunu_bitir() 
            return 
        
        self.soru_sayac_etiketi.config(text=f"Soru: {self.soru_index + 1} / {self.toplam_soru}")
        self.kalan_sure = 10
        self.sayac_etiketi.config(text=f"Süre: {self.kalan_sure}")

        soru_verisi = self.oyun_verisi[self.soru_index]
        self.dogru_cevap = soru_verisi["answer"]

        # Seçenekleri karıştır
        secenekler = soru_verisi["options"][:] 
        random.shuffle(secenekler)

        for i, btn in enumerate(self.secenek_butonlari):
            btn.config(text=secenekler[i], state="normal")

        try:
            resim_yolu = f"img/{soru_verisi['file']}"
            img = Image.open(resim_yolu)
            img = img.resize((300, 200), Image.LANCZOS)
            self.bayrak_resmi = ImageTk.PhotoImage(img) 
            self.bayrak_etiketi.config(image=self.bayrak_resmi)

        except Exception:
            print("Hata")

        self.soru_index += 1
        
        self.kalan_sure = 10
        self.sayac_etiketi.config(text=f"Süre: {self.kalan_sure}")
        self.sayac_id = self.ana_pencere.after(1000, self.sayaci_guncelle)

    # Sayaç fonksiyonu
    def sayaci_guncelle(self):
        
        self.kalan_sure -= 1
        self.sayac_etiketi.config(text=f"Süre: {self.kalan_sure}")

        if self.kalan_sure > 0:
            self.sayac_id = self.ana_pencere.after(1000, self.sayaci_guncelle)
        else:
            self.sayac_etiketi.config(text="Süre Doldu!")
            self.cevabi_kontrol_et(None) 

    # Cevabı Kontrol etme foknsiyonu
    def cevabi_kontrol_et(self, secilen_cevap):

        if self.sayac_id:
            self.ana_pencere.after_cancel(self.sayac_id)
            self.sayac_id = None

        if secilen_cevap == self.dogru_cevap:
            kazanilan_puan = self.kalan_sure * 10
            self.skor += kazanilan_puan
            self.skor_etiketi.config(text=f"Skor: {self.skor}")
            self.sayac_etiketi.config(text=f"+{kazanilan_puan} Puan!", fg="green")
        else:
            self.sayac_etiketi.config(text=f"Yanlış! ({self.dogru_cevap})", fg="orange")
        
        for btn in self.secenek_butonlari:
            btn.config(state="disabled")

        self.ana_pencere.after(1500, self.renkleri_sifirla_ve_gec)

    # Renkleri sıfırla fonksiyonu
    def renkleri_sifirla_ve_gec(self):
       
        self.sayac_etiketi.config(fg="red") 
        self.sonraki_soru() 

    # Skor tablosunu gösterme
    def skor_tablosunu_goster(self):
       
        self.ekrani_temizle()
        
        label_baslik = tk.Label(self.ana_pencere, text="Oyun Bitti!", font=("Arial", 22, "bold",))
        label_baslik.pack(pady=(20,10))
        
        tum_skorlar = skorlari_oku()

        if self.tebrik_mesaji != "":
            label_tebrik = tk.Label(self.ana_pencere, text=self.tebrik_mesaji, font=("Arial", 16), fg="green", wraplength=400, justify="center")
            label_tebrik.pack(pady=(5, 15))
            self.ogeler.append(label_tebrik)
        
        benim_siram = -1
        for i, (isim, skor_puan) in enumerate(tum_skorlar, 1):
            if isim == self.kullanici_adi and skor_puan == self.skor: 
                benim_siram = i
                break 
                
        sira_metni = f"{self.kullanici_adi}, Toplam Skorun: {self.skor}"
        if benim_siram != -1:
            sira_metni += f"\nSıralaman: {benim_siram}"
            
        sira_etiketi = tk.Label(self.ana_pencere, text=sira_metni, font=("Arial", 16, "bold"), fg="blue")
        sira_etiketi.pack(pady=(5, 15))

        label_top10 = tk.Label(self.ana_pencere, text="Yüksek Skorlar (Top 10)", font=("Arial", 18))
        label_top10.pack()
        
        skor_gosterge_alani = tk.Text(self.ana_pencere, width=40, height=10, font=("Courier", 14), state="disabled")
        skor_gosterge_alani.pack(pady=10, padx=10)
        
        tekrar_oyna_btn = tk.Button(self.ana_pencere, text="Yeniden Oyna", font=("Arial", 14),
                                    command=self.baslangic_ekranini_goster)
        tekrar_oyna_btn.pack(pady=(10, 5)) 
        
        cikis_btn = tk.Button(self.ana_pencere, text="Çıkış", font=("Arial", 14),
                              command=self.ana_pencere.quit)
        cikis_btn.pack(pady=5)
     
        self.ogeler.extend([label_baslik, sira_etiketi, label_top10, skor_gosterge_alani, tekrar_oyna_btn, cikis_btn])

        self.skorlari_gostergeye_yukle(skor_gosterge_alani, tum_skorlar)

    # Skorları yükle 
    def skorlari_gostergeye_yukle(self, text_alani, skor_listesi):
    
        text_alani.config(state="normal")
        text_alani.delete('1.0', tk.END)
        
        if not skor_listesi:
            text_alani.insert(tk.END, "Henüz kayıtlı skor yok.")
        else:
            baslik = f"{'Sıra':<5} {'Kullanıcı':<20} {'Skor':>8}\n"
            text_alani.insert(tk.END, baslik)
            text_alani.insert(tk.END, "-"*35 + "\n")
            
            for i, (isim, skor) in enumerate(skor_listesi[:10], 1):
                satir = f"{i:<5} {isim:<20} {skor:>8}\n"
                text_alani.insert(tk.END, satir)
        
        text_alani.config(state="disabled")

    # Oyun bitişi
    
    def oyunu_bitir(self):
        en_isim, en_puan = en_yuksek_skoru_getir()
        skoru_kaydet(self.kullanici_adi, self.skor)

        self.tebrik_mesaji = ""
        if self.skor > en_puan:
            self.tebrik_mesaji = f"Tebrikler {self.kullanici_adi}! Oyunu kazandın ve en yüksek skoru geçtin! 🎉"
        
        self.skor_tablosunu_goster()

# Programı Çalıştır
if __name__ == "__main__":
    root = tk.Tk()  
    app = Flagguess(root) 
    root.mainloop()