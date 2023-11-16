# CRM
![App Screenshot](https://github.com/firengizz099/CRM/blob/main/CRM.png?raw=true)

# RFM metic

![App Screenshot](https://github.com/firengizz099/CRM/blob/main/Rfm.png?raw=true)

# Cltv.py  CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)

# RFM.py
Bu kod, RFM (Recency, Frequency, Monetary) analizi kullanarak müşteri segmentasyonu gerçekleştiren bir süreci içermektedir. Aşağıda kodun yapmış olduğu işlemlerin özetini bulabilirsiniz:

Verinin yüklenmesi: CSV dosyası olarak veri okunur.
Veri anlama: Veri seti hakkında temel bilgiler elde edilir, eksik değerler kontrol edilir ve bazı istatistikler hesaplanır.
Veri hazırlama: İptal edilen işlemler ve eksik değerler veri setinden çıkarılır.
RFM metriklerinin hesaplanması: Recency, Frequency ve Monetary metrikleri hesaplanır.
RFM skorlarının hesaplanması: RFM metriklerine dayanarak RFM skorları oluşturulur.
RFM segmentlerinin oluşturulması ve analiz edilmesi: RFM skorlarına göre müşteriler segmentlere ayrılır ve segmentlere özgü istatistikler elde edilir.
**Sonuçların kaydedilmesi: Oluşturulan RFM segmentleri ve yeni müşterilerin kimlikleri CSV dosyalarına kaydedilir.**
**Kod, müşteri segmentasyonu yapmak için RFM analizinin temel adımlarını içermektedir. İlgili veri setine ve segmentasyon kriterlerine göre sonuçları analiz edebilir ve işletme için değerli bilgiler elde edebilirsiniz.**

# cltv.py 
**müşteri yaşam boyu değerini tahmin etmek ve müşterileri segmentlere ayırmak için kullanılan bir müşteri değerlendirme modeli olan CLTV (Customer Lifetime Value) analizini gerçekleştirir. Fonksiyon, bir veri çerçevesini ve opsiyonel olarak kar marjını girdi olarak alır.**
**Fonksiyon adımları şu şekildedir:**
Veri Hazırlama: İptal edilen işlemleri (Invoice sütunu içinde "C" içeren satırları) ve negatif miktarları (Quantity sütunu içinde 0'dan küçük olanları) filtreler ve eksik verileri kaldırır. Ardından, her müşteri için toplam işlem sayısını, toplam birimi ve toplam fiyatı hesaplar.

**Ortalama Sipariş Değeri (avg_order_value) Hesaplama: Müşterinin toplam fiyatını toplam işlem sayısına bölerek ortalama sipariş değerini hesaplar.**
**Satın Alma Sıklığı (purchase_frequency) Hesaplama: Müşterinin toplam işlem sayısını müşteri sayısına bölerek satın alma sıklığını hesaplar.**

**Tekrar Oranı ve Kayıp Oranı Hesaplama: Birden fazla işlemi olan müşterilerin oranını toplam müşteri sayısına böler ve tekrar oranını hesaplar. Buna karşılık, kayıp oranını da hesaplar.**

**Kar Marjı Hesaplama: Toplam fiyatı kar marjı ile çarparak kar marjını hesaplar.**
**Müşteri Değeri (customer_value) Hesaplama: Ortalama sipariş değerini satın alma sıklığı ile çarparak müşteri değerini hesaplar.**

**Müşteri Yaşam Boyu Değeri (cltv) Hesaplama: Müşteri değerini kayıp oranına böler ve kar marjı ile çarparak müşteri yaşam boyu değerini hesaplar.**

**Segmentleme: CLTV'ye göre müşterileri dört farklı segmente ayırır (A, B, C, D).**

**Son olarak, hesaplanan değerleri içeren ve segment sütunu eklenmiş olan CLTV çerçevesini döndürür.
müşteri değerini anlamak, müşterileri segmentlere ayırmak ve pazarlama stratejilerini yönlendirmek için kullanılabilir. Örneğin, en yüksek CLTV'ye sahip müşteriler (A segmenti) daha fazla odaklanılabilir ve sadakat programları veya kişiselleştirilmiş teklifler gibi stratejilerle müşteri bağlılığı artırılabilir.**

# cltv.predict.py
**Bu kod, müşteri yaşam süresi değerini tahmin etmek ve müşterileri segmentlere ayırmak için kullanılan bir müşteri değeri tahmin modeli olan CLTV (Customer Lifetime Value) modelini oluşturmak için kullanılır.**

**Kodun işleyişini adım adım açıklayalım:**

**Veri Ön İşleme:**
**NaN değerleri içeren satırlar düşürülür.**
**"Invoice" sütununda "C" harfi içeren (iptal edilen) işlemler çıkarılır.**
**"Quantity" sütununda 0'dan küçük değerlere sahip satırlar çıkarılır.**
**"Price" sütununda 0'dan küçük değerlere sahip satırlar çıkarılır.**
**"Quantity" sütunundaki aykırı değerler, belirlenen eşik değerlerle değiştirilir.**
"Price" sütunundaki aykırı değerler, belirlenen eşik değerlerle değiştirilir.
"TotalPrice" adında yeni bir sütun oluşturulur ve "Quantity" ile "Price" sütunlarının çarpımıyla hesaplanır.
Bugünün tarihini temsil eden bir değişken tanımlanır.

**BG-NBD Modelinin Kurulması:**
**BetaGeoFitter sınıfı kullanılarak BG-NBD modeli kurulur.**
Model, frekans, recency ve T değerleri kullanılarak eğitilir.
Model üzerinden 1 haftalık, 1 aylık ve 3 aylık beklenen satın alma değerleri hesaplanır.
GAMMA-GAMMA Modelinin Kurulması:

GammaGammaFitter sınıfı kullanılarak GG modeli kurulur.
**Model, frekans ve monetary değerleri kullanılarak eğitilir.**
**Model üzerinden beklenen ortalama kar hesaplanır.**
**BG-NBD ve GG modeli ile CLTV'nin hesaplanması:**

**GammaGammaFitter sınıfının customer_lifetime_value() yöntemi kullanılarak müşteri yaşam süresi değeri (CLTV) hesaplanır.**
**Hesaplanan CLTV değerleri, müşteri kimlik numarasıyla birleştirilen ve segmentlere ayrılan bir DataFrame'e aktarılır.**
**Son olarak, cltv_final2 DataFrame'i "cltv_prediction.csv" adlı bir CSV dosyasına kaydedilir.**

**Bu kod, müşterilerin değerlerini tahmin etmek ve onları segmentlere ayırmak için kullanılan bir modelin işleyişini göstermektedir. Özellikle müşteri değerlemesi ve müşteri segmentasyonu gibi konularla ilgilenenler için faydalı olabilir.**
