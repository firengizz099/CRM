###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması


# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

data =  pd.read_csv('/home/firengiz/Belgeler/crm/data.csv',encoding='latin-1')
df = data.copy() #eger ileride ters bir durum olursa bu uzun veriyi tekrar okuma islemini tekrar beklememis olucam
print(df.head())

print(df.shape)

print(df.isnull().sum())

# essiz urun sayisi kactir?
print('essiz urun sayisi.',df['Description'].nunique())

# hangi urunden kacar tane var?
print(df['Description'].value_counts().head())

# hangi urunden toplam kacar tane siparis verilmis (adet olarak)? 
print(df.groupby('Description').agg({'Quantity':'sum'}).sort_values(by='Quantity',ascending=False).head())

# toplam kac tane essiz fartura kesilmis?
print(df['InvoiceNo'].nunique())

# urunlerin basina toplam kazanc?
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
print(df.head)

# urun basina kac para odendigi.
print(df.groupby('InvoiceNo').agg({'TotalPrice':'sum'}).head())


###############################################################
# 3. Veri Hazırlama (Data Preparation)
###############################################################
print(df.shape)
df.dropna(inplace=True)
print(df.shape)
print('Describe',df.describe().T)

# c ile baslayanlar iade edilmitir iade edilen urunleri dataframe'den cikarma islemi
df = df[~df['InvoiceNo'].str.contains('C',na=False)]

###############################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

# Recency - musterinin yeniligini (sicakligi) analinizin yapildigi tarih - (eksi) ilgili musterinin son satin alma tarihi
# Frequency - musterinin yaptigi toplam satin alma
# Monetary - musterinin biraktigi toplam parasal deger
print(df.head())

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])


today_date = dt.datetime(2011, 9, 11)
print(type(today_date))

# RFM metrikleri
# musterilere gore groupby'a aldiktan sonra 
# 1)Recency--InvoiceDate- today_date'den ilgili musterinin en son satin alma tarihi (InvoiceDate.max())
# 2)Frequency--Invoice - kullanicilara gore groupby'a aldiktan sonra essiz degerlerini aliyoruz (kac tane fatura var)
# 3) Monetary-- ToalPrice sum alma islemi
rfm = df.groupby('CustomerID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                    'InvoiceNo': lambda Invoice: Invoice.nunique(),
                                    'TotalPrice': lambda TotalPrice: TotalPrice.sum()})



rfm.columns = ['Recency','Frequency','Monetary']
print(rfm.head)

rfm = rfm[rfm['Monetary'] > 0]
rfm = rfm[rfm['Recency'] > 0]

print(rfm.describe().T)

###############################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

rfm['recency_score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])

rfm['frequency_socre'] = pd.qcut(rfm['Frequency'].rank(method='first'),5, labels=[1, 2, 3, 4, 5])

rfm['monetary_score'] = pd.qcut(rfm['Monetary'],5, labels=[1, 2, 3, 4, 5])


rfm['RFM_score'] = (rfm['frequency_socre'].astype(str)+rfm['recency_score'].astype(str))

print(rfm[rfm['RFM_score']=='55'])

print(rfm[rfm['RFM_score']=='11'])
print(rfm.shape)


###############################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
###############################################################
# regex

# RFM isimlendirmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


rfm['segment'] = rfm['RFM_score'].replace(seg_map, regex=True)
print(rfm)
print('#############################################################################################')
print(rfm[["segment", "Recency", "Frequency", "Monetary"]].groupby("segment").agg(["mean", "count"]))


print('head',rfm[rfm['segment'] == 'cant_loose'].head())
print('#################################################')
print('index',rfm[rfm['segment'] == 'cant_loose'].index)#sadece id'leri


new_df = pd.DataFrame()
new_df['new_customer_id'] = rfm[rfm['segment'] == 'new_customers'].index
new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)

new_df.to_csv('new_customers.csv')

rfm.to_csv('rfm.csv')