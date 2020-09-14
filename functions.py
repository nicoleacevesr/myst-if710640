
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import numpy as np
import time
import pandas as pd
import yfinance as yf
from os import listdir, path
from os.path import isfile, join
from datetime import datetime
from datetime import timedelta
import math

def fecha_mensual(archivos):
    fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]
    return fechas

def gtickers(archivos,data_archivos):
    tickers = []
    for i in archivos:
        l_tickers = list(data_archivos[i]['Ticker'])
        [tickers.append(i + '.MX') for i in l_tickers]
    global_tickers = np.unique(tickers).tolist()
    global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]
    global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
    global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
    [global_tickers.remove(i) for i in ['KOFL.MX', 'MXN.MX', 'KOFUBL.MX', 'BSMXB.MX', 'USD.MX']]
    return global_tickers

def desc_datos(global_tickers):
    inicio = time.time()
    data = yf.download(global_tickers, start="2018-01-30", end="2020-08-22", actions=False,
                       group_by="close", interval='1d', auto_adjust=False, prepost=False, threads=True)
    print('Se tardo', round(time.time() - inicio, 2), 'segundos')
    return data

def closed_data(data,global_tickers):
    data_close = pd.DataFrame({i: data[i]['Close'] for i in global_tickers})
    return data_close

def fechas_y(data_close,i_fechas):
    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(i_fechas)))
    return ic_fechas

def precios_f(data_close , ic_fechas):
    precios_v = data_close.iloc[[int(np.where(data_close.index.astype(str) == i)[0]) for i in ic_fechas]]
    precios_v = precios_v.reindex(sorted(precios_v.columns), axis=1)
    return precios_v

def posdatos(eliminacion,data_archivos,archivos,precios_v,k,c):
    pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]
    lista_activos = list(pos_datos[pos_datos['Ticker'].isin(eliminacion)].index)
    pos_datos.drop(lista_activos, inplace=True)
    pos_datos.reset_index(inplace=True, drop=True)
    pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')
    pos_datos['Precios'] = (np.array([precios_v.iloc[0, precios_v.columns.to_list().index(i)] for i in pos_datos['Ticker']]))
    cap=pos_datos['Peso (%)'] * k
    pos_datos['Capital'] = cap - cap * c
    pos_datos['Titulos'] = pos_datos['Capital'] // pos_datos['Precios']
    pos_datos['Postura'] = pos_datos['Precios'] * pos_datos['Titulos']
    pos_datos['Comisiones'] = pos_datos['Precios'] *  pos_datos['Titulos']*c
    return pos_datos

def inversion_pasiva(ic_fechas,pos_datos,precios_v,dinero_rest_pasivo,i_pasiva):
    long=len(ic_fechas)
    for i in range(long):
        pos_datos['Precios'] = (np.array([precios_v.iloc[i, precios_v.columns.to_list().index(j)] for j in pos_datos['Ticker']]))
        pos_datos['Comision'] = 0
        pos_datos['Postura'] = pos_datos['Precios'] * pos_datos['Titulos']
        i_pasiva['Capital'].append(pos_datos['Postura'].sum() + dinero_rest_pasivo)
        i_pasiva['Fechas'].append(ic_fechas[i])
    return i_pasiva