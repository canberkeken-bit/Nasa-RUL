NASA Turbofan Motorlarında Kalan Faydalı Ömür (RUL) Tahmini

English · Türkçe

Uçak motoru sensör verisinden, motorun arızaya kaç çevrim kaldığını (RUL, Remaining Useful Life) basit Python ve scikit-learn ile tahmin eden bir veri analizi / makine öğrenmesi projesi. NASA C-MAPSS veri setinin dört alt kümesi (FD001–FD004) ayrı ayrı işlendi. Bitirme projesi olarak hazırlandı.

Amaç ileri düzey bir model kurmak değil; her adımı açıklanabilir, tekrarlanabilir ve öğrenci seviyesinde okunabilir tutmaktı. Boru hattı (pipeline) yok, her adım ayrı bir hücre.

Etkileşimli sayfalar

GitHub Pages'i docs/ klasöründen açarsan (Settings → Pages → Branch: main, Folder: /docs):

docs/index.html: dokuz grafiğin etkileşimli hâli (dört veri seti, üzerine gelince değerler, alarm eşiği kaydırıcısı)
docs/demo.html: web demo (önceden hesaplanmış Random Forest tahminleri, bakım uyarısı)
Ne yapıldı?
Dosyalar okundu, sütun adları verildi.
Standart sapması 0.01'in altındaki sabit sütunlar atıldı (FD001: 10, FD002: 1, FD003: 9, FD004: 1 sütun).
Train'de RUL = motorun son çevrimi − şu anki çevrim hesaplandı, 125'te sınırlandı.
Sensörler MinMaxScaler ile ölçeklendi (yalnızca train'e fit, veri sızıntısı yok).
Lineer Regresyon (temel model) ve Random Forest (n_estimators=100, max_depth=10, random_state=42) eğitildi.
RMSE, MAE, R² ve NASA skoru hesaplandı.
Bonus: "motor 30 çevrim içinde arızalanacak mı?" lojistik regresyon sınıflandırması, bakım alarm eşiği analizi (30 / 40 / 50).
Canlı demo (Gradio) ve etkileşimli grafikler.

Test setinde her motorun yalnızca son satırı değerlendirildi; gerçek RUL değeri RUL_FDxxx.txt dosyasında yalnızca o an için verilir.

Sonuçlar

Test seti, RUL ≤ 125 sınırıyla.

Veri seti	Koşul / arıza modu	RF RMSE	RF MAE	RF R²	LR RMSE (sınırlı)	LR RMSE (sınırsız)
FD001	1 / 1	17.18	12.18	0.82	20.82	31.95
FD002	6 / 1	18.82	14.28	0.81	21.30	33.94
FD003	1 / 2	20.18	14.86	0.73	20.48	57.32
FD004	6 / 2	20.82	15.31	0.77	24.55	47.77
Random Forest dört veri setinde de en düşük RMSE'yi verdi; FD003'te Lineer Regresyondan farkı çok küçük (20.18 ve 20.48).
RUL'u 125'te sınırlamak en büyük tek iyileşmeyi sağladı. Test gerçek değerleri de sınırlandığı için bu kıyas tam eşit koşulda değildir.
NASA skoru (küçük iyi, Lineer Regresyon / Random Forest): FD001 1251 / 898, FD002 2802 / 3584, FD003 1242 / 1710, FD004 4591 / 5240. Random Forest'ın RMSE'si daha iyi olsa da FD002–FD004'te NASA skorunda Lineer Regresyon önde çıktı: birkaç büyük fazla tahmin skoru şişiriyor. "En iyi model" ölçüte göre değişir.
Sınıflandırma (RUL ≤ 30), precision / recall: FD001 0.95 / 0.72, FD002 0.96 / 0.87, FD003 0.94 / 0.75, FD004 0.92 / 0.68.
Zorluk kolaydan zora: FD001 → FD004. FD003'te eğitim–test RMSE farkı belirgin (12.85 → 20.18): ezberleme eğilimi.

FD001 Random Forest: gerçek ve tahmin

Her veri setinin dokuz Colab grafiği figures/FD001/ … figures/FD004/ klasörlerinde.

Colab'de aç
Veri seti	Challenge	Solution
FD001	Colab	Colab
FD002	Colab	Colab
FD003	Colab	Colab
FD004	Colab	Colab

Canlı Gradio demosu: Colab · Web demo: https://canberkeken-bit.github.io/nasa-rul-turbofan-prediction/demo.html

Depo yapısı
notebooks/
  FD001 … FD004/   Challenge (boşluk doldurmalı) ve Solution (çözümlü) defterler (Colab)
kaggle/            Aynı defterlerin Kaggle'a uyarlanmış hâli (bkz. kaggle/README.md)
  NASA_RUL_Gradio_Canli_Demo.ipynb   Gradio ile canlı model arayüzü
data/              Veri indirme talimatı (ham veri depoda yok)
docs/              Etkileşimli grafikler ve web demo (GitHub Pages)
reports/           Bitirme raporu, ders anlatımı PDF'i, sunum (PPTX ve PDF)
figures/           36 grafiğin hepsi (veri seti başına 9)
space/             Dört veri seti için Hugging Face Space (Gradio): bkz. space/README.md
Nasıl çalıştırılır?
Veriyi indir ve train_FDxxx.txt, test_FDxxx.txt, RUL_FDxxx.txt dosyalarını hazırla (data/README.md).
Defteri Google Colab'da aç (Dosya → Defteri yükle veya GitHub'dan aç). Colab'ın sol tarafındaki Dosyalar paneline üç veri dosyasını sürükle.
Hücreleri sırayla çalıştır. Challenge defteri boşluk doldurarak öğrenmek için, Solution defteri çözümü görmek içindir.
Canlı demo için NASA_RUL_Gradio_Canli_Demo.ipynb defterini çalıştır; son hücre bir gradio.live bağlantısı verir (bağlantı her çalıştırmada değişir).

Yerelde çalıştırmak için: pip install -r requirements.txt ve Jupyter.

Sınırlar
Sonuçlar tek rastgele çekirdek (random_state=42) ve tek eğitim/test ayrımıyla elde edildi; çapraz doğrulama yapılmadı. Küçük farklar kesin üstünlük sayılmamalı.
NASA skoru, 125'te sınırlanmış gerçek RUL'a göre hesaplandı; literatürdeki skorlarla doğrudan kıyaslanamaz.
Web demo tahminleri önceden hesaplanmıştır, model tarayıcıda çalışmaz. Gerçek canlı model Gradio defterindedir.
Resmî istatistiksel hipotez testi yapılmadı; karşılaştırmalar rapordaki "Araştırma soruları ve bulgular" bölümünde açık sorular olarak sunuldu.
Sonraki adımlar

Hiperparametre ayarı, GradientBoosting, sensörler için zaman penceresi özellikleri, bakım maliyetine göre alarm eşiği seçimi, çapraz doğrulama.

Veri ve atıf

Veri: NASA Prognostics Data Repository, Turbofan Engine Degradation Simulation Data Set (C-MAPSS). A. Saxena ve K. Goebel (2008), NASA Ames Prognostics Data Repository. Veri bu depoya dahil edilmemiştir.

Lisans

Kod ve defterler MIT lisansı ile paylaşılmıştır (LICENSE). NASA verisi kendi kullanım koşullarına tabidir.
