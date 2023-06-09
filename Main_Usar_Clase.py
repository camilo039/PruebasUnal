# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 19:48:52 2023

@author: camil
"""

try:
    import os, sys
    import pandas as pd
    import numpy as np
    from pathlib import Path as p
    from pandas_profiling import ProfileReport


except Exception as exc:
            print('Module(s) {} are missing.:'.format(str(exc)))

dir_root = p(__file__).parents[0]
sys.path.append(str(p(dir_root) ))

from cls_extract_datos import Extract_data as data_extract
from cls_transforma_datos import Transform_data as data_transforma
#from cls_carga_datos import carga_data_mf as data_loader




#%%
###############################################################################
# Inicializa la clase y realiza validaciones básicas
###############################################################################
#%%
''' Crear una instancia de la clase '''
ex_d= data_extract()
ex_d.path = dir_root


#%%
###############################################################################
# Descargar datasets desde pagina web
###############################################################################


''' Descargar DataSet '''

url="https://snies.mineducacion.gov.co/1778/articles-391562_recurso.xlsb"
path_data = str(p(ex_d.path) / 'Dataset'/'Inscritos.xlsb')

ex_d.descargar_archivo(url,path_data)


#%%
###############################################################################
# Cargar datos en memoria
###############################################################################

''' Cargar datos a memoria'''
ex_d.get_data(path_data)


#%%
''' Eliminar filas no requeridas '''

inicio=0
fin=5

ex_d.Eliminar_filas(inicio, fin)
#%%
''' Establece la cabecera '''
nCabecera=0
ex_d.Nueva_Cabecera(nCabecera)


#%%
''' Mostrar datos'''
print(ex_d.data.info())

df=pd.DataFrame(ex_d.data)

#%%
#Zona de pruebas


#%%


#%%
#ru="C:/Users/camil/Desktop/PruebasUnal/archivo_excel.xlsx"

#df.to_excel(ru, index=False)


#%%
###############################################################################
# Transformar datos
###############################################################################
#%%
''' Crear una instancia de la clase '''
tr_d = data_transforma()
tr_d.ld = ex_d
tr_d.data=ex_d.data
#%%

'''Validar datos nulos'''
tr_d.Datos_nulos()
#%%
'''Validar datos Duplicados'''
tr_d.Datos_duplicados()
#%%
'''Convertir los datos segun su tipo'''
tr_d.convertir_tipos_de_datos()
#%%
'''Convertir en minusculas'''
tr_d.Minusculas()


#%%
''' eliminar columnas totales '''
tr_d.Eliminar_columnas()

#%%

''' Transformar datos a datos finales '''

tr_d.Datos_finales()
#%%
tr_d.data.tail()
#%%

''' Exportar datos finales ''' 

ru="C:/Users/cagarciach/OneDrive - Telefonica/CANALES COMERCIALES/PruebasUnal/archivo_final.csv"
tr_d.data.to_csv(ru, index=False)
#%%
from pandas_profiling import ProfileReport
prof = ProfileReport(tr_d.data)
prof.to_file(output_file='output.html')

