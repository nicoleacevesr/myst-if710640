
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import data as dat
import functions as func
import visualizations as vis
import pandas as pd
from os.path import isfile, join
from os import listdir, path

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

# -------------------------------------------------------------------------------------------------
#Archivos ordenados por fecha

path = path.abspath('files/')
archivos = dat.fun(path)

# -------------------------------------------------------------------------------------------------
data_archivos= dat.limpieza_archivos(archivos)
# -------------------------------------------------------------------------------------------------
ic_fechas = func.fecha_mensual(archivos)

# -------------------------------------------------------------------------------------------------
global_tickers = func.gtickers(archivos,data_archivos)

# -------------------------------------------------------------------------------------------------
data = func.desc_datos(global_tickers)

# -------------------------------------------------------------------------------------------------
data_close = func.closed_data(data,global_tickers)

# -------------------------------------------------------------------------------------------------
ic_fechas = func.fechas_y(data_close,ic_fechas)

# -------------------------------------------------------------------------------------------------
precios = func.precios_f(data_close,ic_fechas)

# -------------------------------------------------------------------------------------------------
#INVERSION PASIVA

# capital inicial
k = 1000000
# comisiones por transaccion
c = 0.00125

# Eliminamos porcentajes de KOFUBL, KOFL, BSMXB, MXN, USD
eliminacion = ['KOFL', 'KOFUBL', 'BSMXB', 'MXN', 'USD']

# -------------------------------------------------------------------------------------------------
pos_datos = func.posdatos(eliminacion,data_archivos,archivos,precios,k,c)

# -------------------------------------------------------------------------------------------------
dinero_rest_pasivo = k - pos_datos['Postura'].sum() - pos_datos['Comisiones'].sum()

# -------------------------------------------------------------------------------------------------
total_comision_pasivo = pos_datos['Comisiones'].sum()

# -------------------------------------------------------------------------------------------------
# Definimos el dicionario en donde vamos a guardar los resultados de fecha y capital
i_pasiva = {'Fechas': ['2018-01-30'], 'Capital': [k]}

# -------------------------------------------------------------------------------------------------
i_pasiva =func.inversion_pasiva(ic_fechas,pos_datos,precios,dinero_rest_pasivo,i_pasiva)

# -------------------------------------------------------------------------------------------------
#Resultado oara inversión pasiva
r_pasiva=vis.proceso_pasiva(i_pasiva)
