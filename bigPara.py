#coding: utf-8
from lxml import etree
import lxml.html
import json

# http://bigpara.hurriyet.com.tr/altin/ sitesinden ayıklanan 
# verilere göre Tür Id ve karşılıklarını kullanabilirsiniz.

# TurId                           Adi
# -----                           ---
# GLDGR                           ALTIN (TL/GR)
# BILEZIKAKAYNAK                  22 Ayar Bilezik
# XAUUSD                          Altın (ONS)
# SGLDD                           Altın ($/kg)
# SGLDE                           Altın (Euro/kg)
# SCUM                            Cumhuriyet Altını
# SGLDY                           Yarım Altın
# SGLDC                           Çeyrek Altın
# SRES                            Reşat Altını
# SRESK                           Kulplu Reşat Altını
# GLDATACEYREK                    Ata Ceyrek
# GLDATAYARIM                     Ata Yarim
# GLDATATEK                       Ata Tam
# GLDATA2_5                       Ata 2.5
# GLDATA5LI                       Ata 5 li
# GPOR22                          22 Ayar Altın TL/Gr
# GPOR18                          18 Ayar Altın TL/Gr
# GPOR14                          14 Ayar Altın TL/Gr
# GPOR8                           8 Ayar Altın TL/Gr
# GLDZIYNETCEYREK                 Kapalicarsi Ziynet Ceyrek
# GLDZIYNETYARIM                  Kapalicarsi Ziynet Yarim
# GLDZIYNETTEK                    Kapalicarsi Ziynet Tam
# GLDZIYNET2_5                    Kapalicarsi Ziynet 2.5
# GLDZIYNET5LI                    Kapalicarsi Ziynet 5 li


# Altta yer alan listeye yukarıda görünen kaynak türId'sini 
# ve bu kaynaktan adet/kg/gr türünden ne kadar sahip olduğunuzu yazmalısınız
# Örn: 3 tane çeyrek altınım var karşılığını "mySources.append(['SCUM', 3])"
# olarak girmeliyim, aynı şekilde gram/kg içinde durum aynı

mySources = []
mySources.append(['BILEZIKAKAYNAK', 85]) # 85 gr, "22 Ayar Bilezik"
mySources.append(['SCUM', 3]) # 3 tane, "Cumhuriyet Altın"
mySources.append(['SGLDC', 1]) # 1 tane, "Çeyrek Altın"

dom = lxml.html.parse("http://bigpara.hurriyet.com.tr/altin/") # sayfasının dom yapısı çekiliyor
xpatheval = etree.XPathDocumentEvaluator(dom) # xpath ile ağaçlandırılıyor
rawData = xpatheval('//*[@id="content"]/div[2]/script[1]/text()') # çekeceğimiz verinin xpath kodu ile yerini tespit ediyor
jsonValue = rawData[0].replace("var   altinData =","").replace(";","").strip() # veriyi temizliyor
jsonList = json.loads(jsonValue) # ham veriyi json liste nesnesine atıyor

firstTotal = 14900 # sahip olunan altın varlıkları için satış toplam tutarı (karşılığında ödediğim para)
currentTotal = 0 # sahip olunan altın varlıklarının şimdiki alış toplam tutarı (şimdiki değeri)

inFormat="{:20} {:<10}  {:<15} {:<15}"

print inFormat.format("Adi","Alis","Adet/Kg/Gr","AlisToplam")
print inFormat.format("---","----","----------","----------")

for i in mySources:

    for gold in jsonList:

        if(i[0]==gold["Sembol"]):
            
            aValue = gold["Alis"] * i[1];
            currentTotal += aValue

            adi = gold["Adi"].lower().encode('utf8').replace("ç","c").replace("ğ","g").replace("ı","i").replace("ö","o").replace("ş","s").replace("ü","u")
            print inFormat.format(adi,gold["Alis"],i[1],aValue)

print "Hepsinin toplamı:",currentTotal,"tl" # Varlıklarımın şimdiki toplam alış değeri
print "Sonuç:",(currentTotal-firstTotal),"tl" # Kar/Zarar değerini görmek için ödediğim tutar ile şimdiki değerini kıyaslıyorum. İşinize yarayan kurguyu uygulayabilirsiniz.