
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
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


def proceso_pasiva(i_pasiva):
    df_pasiva= pd.DataFrame()
    df_pasiva['Fechas']=i_pasiva['Fechas']
    df_pasiva['Capital']=i_pasiva['Capital']
    df_pasiva['Rendimiento']=0
    df_pasiva['Rendimiento Acumulado']=0

    for i in range(1, len(df_pasiva)):
        division=(df_pasiva.loc[i, 'Capital'] / df_pasiva.loc[i - 1, 'Capital'])
        df_pasiva.loc[i, "Rendimiento"] =  division-1
        df_pasiva.loc[i, "Rendimiento Acumulado"] = df_pasiva.loc[i, 'Rendimiento'] + df_pasiva.loc[i - 1, 'Rendimiento Acumulado']
    return df_pasiva


