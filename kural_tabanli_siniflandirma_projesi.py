#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################
import numpy as np
#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.


#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı

################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


#############################################
# PROJE GÖREVLERİ
#############################################

#############################################
# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

import pandas as pd
df = pd.read_csv("datasets/persona.csv")
df.head()

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?

df["SOURCE"].nunique()
len(df["SOURCE"].unique())
df["SOURCE"].value_counts()
#df["SOURCE"].value_counts().unique()

# Soru 3: Kaç unique PRICE vardır?

df["PRICE"].nunique()
len(df["PRICE"].unique())

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?

df["COUNTRY"].value_counts()


# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("COUNTRY").agg({"PRICE": "sum"})
df.groupby("COUNTRY")["PRICE"].sum()

# Soru 7: SOURCE türlerine göre göre satış sayıları nedir?

df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?

df.groupby("COUNTRY").agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)
df.groupby("COUNTRY")["PRICE"].mean()

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby("SOURCE").agg({"PRICE": "mean"})
df.groupby("SOURCE")["PRICE"].mean()

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})
df.groupby(["COUNTRY", "SOURCE"])["PRICE"].mean()

#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################

df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"])["PRICE"].mean().head()

#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.

agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values(by="PRICE", ascending=False)
agg_df.head()
#############################################
# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()
# agg_df.reset_index(inplace=True)
agg_df.shape
agg_df.reset_index(inplace=True)
#agg_df.rename_axis(None, axis=1)
agg_df.head()
#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins=[0, 18, 23, 30, 40, agg_df["AGE"].max()],
                           labels=['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())])
pd.crosstab(agg_df["AGE"], agg_df["AGE_CAT"])
#agg_df.drop(columns=["NEW_AGE"], inplace=True)
#############################################
# GÖREV 6: Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
# customers_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.
# Dikkat!
# list comp ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18
# Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.

agg_df.columns
for row in agg_df.values:
    print(row)
[row[0].upper() +"_"  for row in agg_df.values]
[row["COUNTRY"].upper() + "_" for index, row in agg_df.iterrows()]
['_'.join(i).upper() for i in agg_df.drop(["AGE", "PRICE"], axis=1).values]
agg_df["customers_level_based"] = (agg_df["COUNTRY"] + "_" + agg_df["SOURCE"]
                                   + "_" + agg_df["SEX"] + "_" + agg_df["AGE_CAT"].astype(str)).str.upper()
agg_df1 = agg_df[["customers_level_based","PRICE"]]
agg_df1.groupby(["customers_level_based"]).agg({"PRICE": "mean"})
agg_df["customers_level_based"].value_counts()
agg_df1.reset_index(inplace=True)
agg_df1.head()
agg_df1.shape
#############################################
# GÖREV 7: Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################
# PRICE'a göre segmentlere ayırınız,
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz,
# segmentleri betimleyiniz,

def segmentler(price):
    if price <= 10:
        return "Düşük Fiyat Aralığı"
    elif price <= 50:
        return  "Orta Fiyat Aralığı"
    else:
        return "Yüksek Fiyat Aralığı"

agg_df["SEGMENT2"] = agg_df["PRICE"].apply(segmentler)
agg_df["SEGMENT2"].value_counts()

agg_df.groupby(["SEGMENT2"]).agg({"PRICE" : ["mean", "max", "sum"]})
#küçükten büyüye böler qcut o yüzden d,b, c,a
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=['D', 'B', 'C', 'A'])
agg_df["SEGMENT"].value_counts()

agg_df.groupby(["SEGMENT"]).agg({"PRICE" : ["mean", "max", "sum"]}).sort_values("SEGMENT", ascending=False)

agg_df.groupby(["SEGMENT", "customers_level_based"]).agg({"PRICE" : "mean"}).sort_values("SEGMENT", ascending=False)
#############################################
# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user = "TUR_ANDROID_FEMALE_31_40"
user_df = agg_df1[agg_df1["customers_level_based"] == new_user]
user_df.groupby(["SEGMENT", "customers_level_based"]).agg({"PRICE" : "mean"})

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

new_user2 = "FRA_IOS_FEMALE_31_40"
user_df2 = agg_df[agg_df["customers_level_based"] == new_user2]
user_df2.groupby(["SEGMENT", "customers_level_based"]).agg({"PRICE" : "mean"})

[x for x in range(2, 22, 2)]

np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])