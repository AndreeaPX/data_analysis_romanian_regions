import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import shapiro, kstest, norm, chi2
from pandas.api.types import is_numeric_dtype
from seaborn import scatterplot, heatmap

def sumaT(t,decese,active,vindecari):
    x=t[decese].values
    y=t[active].values
    z=t[vindecari].values
    suma =[]
    for i in range (len(x)):
        rezultat=x[i]+y[i]+z[i]
        suma.append(rezultat)
    return suma

def ponderi(t,decese, suma ):
    x=t[decese].values
    vector= []
    for i in range (len(x)):
        if suma[i] > 0:
            rezultat=(x[i]*100)/suma[i]
            vector.append(rezultat)
    return vector

def an_dominant(t, ani):
    x = t[ani].values
    k = np.argmax(x)
    return pd.Series([t.loc["Judet"], ani[k]], ["Judet", "An dominant"])

def standardizare(x, scal=True, nlib=0):
    x_ = x - np.mean(x, axis=0)
    if scal:
        x_ = x_ / np.std(x, axis=0, ddof=nlib)
    return x_

def salvare(x, nume_linii, nume_coloane, nume_fisier="out.csv"):
    pd.DataFrame(data=x, index=nume_linii, columns=nume_coloane).to_csv(nume_fisier)


def corelatie(t):
    assert isinstance(t, pd.DataFrame)
    return t.corr(numeric_only=True)

def corelograma(t, cmap="RdYlBu", titlu="Grafic corelograma"):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 18, "color": "b"})
    heatmap(t, vmin=-1, vmax=1, annot=True, cmap=cmap, ax=ax)
    plt.show()

def g_scatterplot(t, var1, var2, varg1, titlu):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 18, "color": "b"})
    scatterplot(data=t, x=var1, y=var2, hue=varg1, legend=True, ax=ax)
    plt.show()

def harta(gdf,camp_harta,titlu):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 18, "color": "b"})
    gdf.plot(column = camp_harta,cmap="Reds",legend=True,ax=ax)
    plt.show()

def pieChart(t,valori,label):
    y=np.array(t[valori].values)
    plt.pie(y,labels=label,startangle=90)
    plt.show()