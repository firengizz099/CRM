############################################
# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)
############################################

# 1. Veri Hazırlama
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentlerin Oluşturulması

##################################################
# 1. Veri Hazırlama
##################################################
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

data =  pd.read_csv('/home/firengiz/Belgeler/crm/data.csv',encoding='latin-1')
df = data.copy()

print(df.head())
print(df.isnull().sum())

df = df[~df['InvoiceNo'].str.contains('C',na=False)]

df = df[(df['Quantity'] > 0)]

df.dropna(inplace=True)
print(df.describe().T)

df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

cltv_c = df.groupby('CustomerID').agg({'InvoiceNo': lambda  x:x.nunique(),#total_transaction
                                       'Quantity': lambda x:x.sum(),
                                       'TotalPrice': lambda x:x.sum()})

cltv_c.columns = ['total_transaction','total_unit','total_price']
print(cltv_c)

# 2. Average Order Value (average_order_value = total_price / total_transaction)
cltv_c['average_order_value'] = cltv_c['total_transaction'] / cltv_c['total_price']

# 3. Purchase Frequency (total_transaction / total_number_of_customers)

cltv_c['purchase_frequency'] = cltv_c['total_transaction'] / cltv_c.shape[0]

# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
repeat_rate = cltv_c[cltv_c['total_transaction'] > 1].shape[0] / cltv_c.shape[0]

churn_rate = 1 - repeat_rate
print(churn_rate)

# 5. Profit Margin (profit_margin =  total_price * 0.10)

cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10 

# 6. Customer Value (customer_value = average_order_value * purchase_frequency)

cltv_c['customer_value'] = cltv_c['average_order_value'] * cltv_c['purchase_frequency']
print(cltv_c)

# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)

cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']

print(cltv_c.sort_values(by='cltv',ascending=False))
print(cltv_c.describe().T)

cltv_c['segment'] = pd.qcut(cltv_c['cltv'], 4, labels=['D', 'C', 'B', 'A'])
print(cltv_c)

print(cltv_c.sort_values(by='cltv', ascending=False))

print(cltv_c.groupby('segment').agg({'count', 'mean', 'sum'}))

#cltv_c.to_csv('cltv.csv')



##################################################
# Tüm İşlemlerin Fonksiyonlaştırılması
##################################################

def create_cltv_c(dataframe, profit=0.10):

    # Veriyi hazırlama
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe['Quantity'] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                                   'Quantity': lambda x: x.sum(),
                                                   'TotalPrice': lambda x: x.sum()})
    cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
    # avg_order_value
    cltv_c['avg_order_value'] = cltv_c['total_price'] / cltv_c['total_transaction']
    # purchase_frequency
    cltv_c["purchase_frequency"] = cltv_c['total_transaction'] / cltv_c.shape[0]
    # repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate
    # profit_margin
    cltv_c['profit_margin'] = cltv_c['total_price'] * profit
    # Customer Value
    cltv_c['customer_value'] = (cltv_c['avg_order_value'] * cltv_c["purchase_frequency"])
    # Customer Lifetime Value
    cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']
    # Segment
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c


df = data.copy()

clv = create_cltv_c(df)


