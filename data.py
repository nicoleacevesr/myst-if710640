"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
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


def fun(path):
    archivos = [f[:-4] for f in listdir(path) if isfile(join(path, f))]
    archivos = sorted(archivos, key=lambda t: datetime.strptime(t[8:], '%d%m%y'))
    return archivos

def limpieza_archivos(archivos):
    data_final = {}
    for i in archivos:
        data = pd.read_csv('files/' + i + '.csv', skiprows=2, header=None)
        data.columns = list(data.iloc[0, :])
        data = data.loc[:, pd.notnull(data.columns)]
        data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
        data['Precio'] = [i.replace(',', '') for i in data['Precio']]
        data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
        convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
        data = data.astype(convert_dict)
        data['Peso (%)'] = data['Peso (%)'] / 100
        data_final[i] = data
    return data_final

