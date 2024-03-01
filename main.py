import numpy as np
import pandas as pd
from functii import *
from geopandas import GeoDataFrame

judete=pd.read_csv("epidemie_covid.csv", index_col=0)
variabile_observate=list(judete.columns)[2:]

mortalitate=pd.read_csv("Mortalitate.csv", index_col=0)
ani=list(mortalitate.columns)[1:]
#print(ani)

macroregiuni=pd.read_csv("Macroregiuni_Romania.csv", index_col=0)
includere=list(macroregiuni.columns)[0:]

#Cerinta 1 - Realizati o jonctiune intre macroregiuni si epidemie_covid
judete1 = judete.merge(right=macroregiuni, left_index=True,right_index=True)
judete1.to_csv("Cerinta1.csv")

#Cerinta2 - Calculati totalul valorilor din epidemie_covid pe fiecare macroregiune
cerinta2= judete1[variabile_observate + ["includere"]].groupby(by="includere").agg(sum)
cerinta2.to_csv("Cerinta2.csv")

#Cerinta3 - Calculati procentele mortalitatii pe variabile si macroregiuni
mortalitate1 = mortalitate.merge(right=macroregiuni, left_index=True, right_index=True)
cerinta3=mortalitate1[ani+["includere"]].groupby(by="includere").agg(sum)
p= np.transpose(np.transpose(cerinta3.values)/np.sum(cerinta3.values, axis=1))
p_cerinta3=pd.DataFrame(p,cerinta3.index, cerinta3.columns)
p_cerinta3.to_csv("Cerinta3.csv")

#Cerinta 4 - Suma, media, minimul, maximul abaterea standard si variatia valorilor pentru 2021-Urban (tabela Mortalitate)
grupareM=mortalitate1.groupby(by="includere").agg({"2021-Urban" : ["sum","mean","min","max","median","std","var"]})
grupareM.to_csv("Cerinta4.csv")

#Cerinta 5 - Realizati un tabel cu totalitatea datelor din cele doua fisiere .csv de baza, grupate pe macroregiuni
total_grupari=judete1.merge(right=mortalitate1, left_index=True, right_index=True)
total_grupare1=total_grupari[variabile_observate+ani+["includere_y"]].groupby(by="includere_y").agg(sum)
total_grupare1.to_csv("Cerinta5.csv")

#Cerinta 6 -Realizati un DataFrame ce contine la final coloana Total , reprezentand totalitatea deceselor din 2019-2021, pe judete
df=pd.DataFrame(mortalitate, columns=["Judet","2019-Urban","2020-Urban","2021-Urban","2019-Rural","2020-Rural","2021-Rural"])
df.set_index("Judet", inplace=True)
valori=df.sum(axis=1)
df.insert(6, "Total", valori)
df.to_csv("Cerinta6.csv")

#Cerinta 7 - Salvati judetele cu o mortalitate totala mai mare decat media si ordonati descrescator rezultatul
media_deceselor=df["Total"].mean()
#print(media_deceselor)
cerinta7=df[df["Total"] > media_deceselor]
cerinta7[["Total"]].sort_values(by="Total",ascending=False).to_csv("Cerinta7.csv")

#Cerinta 8 -  Realizarea unui dataFrame cuprinzand Judetele, numarul de cazuri de Covid confirmate , ponderea deceselor , ponderea cazurilor active,
# ponderea cazurilor vindecate

total = sumaT(judete,"total_decese","cazuri_active","total_vindecari");
ponderi_decese_covid_inregistrate = ponderi(judete, "total_decese", total)
#print(ponderi_decese_covid_inregistrate)
pondere_vindecari_inregistrate=ponderi(judete,"total_vindecari",total)
#print(pondere_vindecari_inregistrate)
ponderea_cazurilor_active=ponderi(judete,"cazuri_active",total)
cerinta8= pd.DataFrame(judete, columns=["cod_judet","populatie"])
cerinta8.set_index("cod_judet", inplace=True)
cerinta8.insert(1,"Cazuri confirmate", total)
cerinta8.insert(2,"Ponderea cazurilor vindecate",pondere_vindecari_inregistrate)
cerinta8.insert(3,"Ponderea deceselor",ponderi_decese_covid_inregistrate)
cerinta8.insert(4,"Ponderea cazurilor active",ponderea_cazurilor_active)
cerinta8.to_csv("Cerinta8.csv")

#Cerinta 9 - Sa se determine anul care a inregistrat cea mai mare mortalitate, pe judete
cerinta9 = mortalitate.apply(func=an_dominant, axis=1, ani=ani)
cerinta9.to_csv("Cerinta9.csv")

#Cerinta 10 - Standardizare si centrare a datelor
x=p_cerinta3[ani].values
#print(x)
x_ = standardizare(x, scal=False)
z = standardizare(x)
salvare(x_, p_cerinta3.index, ani, "xc.csv")
salvare(z, p_cerinta3.index, ani, "z.csv")

#Cerinta 11  Să se calculeze matricele
# de corelații între indicatorii edidemiei de covid, la nivel
# de macroregiune și să se salveze în fișiere csv, câte un fișier pentru fiecare macroregiune.
judetedf =pd.DataFrame(judete, columns=["judet","cod_judet","cazuri_active","total_vindecari","total_decese"])
varb=list(judetedf.columns)[2:]
#print(judetedf)
judete_ = judetedf[varb].merge(macroregiuni[["includere"]], left_index=True, right_index=True)
cerinta11=judete_.groupby(by="includere").apply(func=corelatie)
#print(cerinta11)
for v in cerinta11.index.get_level_values(0).unique():
    cerinta11.loc[v,:].to_csv(v+".csv")

#Cerinta 12 - Bazându-ne pe cerința anterioară, au fost trasate corelogramele pentru fiecare element analizat și macroregiune
for t in cerinta11.index.get_level_values(0).unique():
    corelograma(cerinta11.loc[t, :],titlu="Corelograma "+t)

#Cerinta 13 - Trasati hărțile pentru cei trei indicatori analizați, anume cazuri active, total vindecări și total decese, raportate pe județe
judetedf_ =pd.DataFrame(judete, columns=["cod_judet","cazuri_active","total_vindecari","total_decese"])
judetedf_.set_index("cod_judet", inplace=True)
coloane=list(judetedf_.columns)[0:]
#print(judetedf_)
gdf = GeoDataFrame.from_file("RO_NUTS2/Ro.shp")
gdf_ = gdf.merge(judetedf_,left_on="sj", right_index=True)
for c in coloane:
    harta(gdf_, c, "Harta dupa " + c)

#Cerinta 14 - Trasati graficul scatterplot pentru grupări de câte doi indicatori analizați cu evidențierea județelor pe macroregiuni
for i in range(len(coloane)):
    for j in range(i + 1, len(coloane)):
        g_scatterplot(judete1, coloane[i], coloane[j], "includere",
                      titlu="Plot (" + coloane[i] + "," + coloane[j] + ")")

#Cerinta 15 -  Realizati un PieChart pentru reprezentarea ponderii cazurilor confirmate de Covid-19, pentru fiecare judet, in total cazuri confirmate,pe tara
labels=np.array(judete["judet"].values)
pieChart(cerinta8,"Cazuri confirmate",labels)

