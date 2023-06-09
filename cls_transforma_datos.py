# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 13:16:00 2021

@author: scorp
"""
try:
    from pathlib import Path as p
    import pandas as pd
    import glob
    import os
    
    import pprint
    import shutil
    import chardet

    from pandas.api.types import is_numeric_dtype
    import datetime as dt
    import seaborn as sns
    
    
    
except Exception as exc:
    print('Module(s) {} are missing.:'.format(str(exc)))
#%%
class Transform_data(object):
    
    def __init__(self, path=None,percent=None, ld = None):
        self.data = None
        self.dataj = None
        self.status = False
        self.ld = None
        self.validacion=None




###############################################################################
    def integridad(self):
        '''
        Rellena con el promedio los datos vacios de las variables numericas 

        Returns
        -------
        None.

        '''
        try:
            self.data=self.data.apply(lambda x: x.fillna(x.mean()) if is_numeric_dtype(x)else x)
            print(self.data.info())
            
        except Exception as exc:
            self.show_error(exc)




                  
###############################################################################
    def Datos_duplicados(self):
        '''
        Imprime el numero de datos duplicados por columna 

        Returns
        -------
        None.

        '''
        self.data = self.ld.data

        df1 = self.data[self.data.duplicated(keep=False)]
        result=df1.empty
        
        if result==True:
            print("La data no tiene datos duplicados")
        else:
            df1 = df1.groupby(df1.columns.tolist()).apply(lambda x: x.index.tolist()).values.tolist()
            print(df1)
###############################################################################
    def Datos_nulos(self):
        '''
        Imprime el numero de datos null por columna 

        Returns
        -------
        None.

        '''
        print(self.data.isnull().sum())
        
        sns.heatmap(self.data.isnull(), cbar=False)
#%%
    def convertir_tipos_de_datos(self):
        '''
        Convierte los datos a su tipo  ya sea string , int o float

        Returns
        -------
        None.

        '''
        
        try:
            
            for columna in self.data.columns:
                tipo_dato = self.data[columna].dtype
        
                if tipo_dato == object:
                    # Verificar si los valores son enteros
                    if self.data[columna].apply(lambda x: str(x).isdigit()).all():
                        self.data[columna] = self.data[columna].astype(int)
                    else:
                        # Verificar si los valores son flotantes
                        try:
                            self.data[columna] = self.data[columna].astype(float)
                        except ValueError:
                            pass
                elif tipo_dato == int:
                    # Convertir a float si contiene valores decimales
                    if self.data[columna].apply(lambda x: isinstance(x, float) or (isinstance(x, str) and '.' in x)).any():
                        self.data[columna] = self.data[columna].astype(float)
                elif tipo_dato == float:
                    # Redondear a 2 decimales
                    self.data[columna] = self.data[columna].round(2)
            
        except Exception as exc:
            self.show_error(exc)
        
      
#%%
    def Minusculas(self):
        '''
        Convierte los datos a su miniscula con la primer letra mayuscula

        Returns
        -------
        None.

        '''
        
        try:
            for columna in self.data.columns:
                if self.data[columna].dtype == object:
                    self.data[columna] = self.data[columna].apply(lambda x: x.lower().title() if isinstance(x, str) else x)
         
        except Exception as exc:
            self.show_error(exc)        
     
#%%
    def Eliminar_columnas(self):
        '''
        Elimina las columnas que contienen Total

        Returns
        -------
        None.

        '''
        
        try:
            # Eliminar columnas que contienen la palabra "total"
            columnas_a_eliminar = self.data.filter(like='Total').columns
            self.data = self.data.drop(columnas_a_eliminar, axis=1)
            
        except Exception as exc:
            self.show_error(exc)        
#%%
    def Datos_finales(self):
        '''
        Elimina las columnas que contienen Total

        Returns
        -------
        None.

        '''
        
        try:
            
            
            ct=len(self.data.columns.values)


            #Dataframe con los datos que no cambian
            df_base = self.data.iloc[:, :21]

            #Columna A trabajar
            columna_seleccionada =pd.DataFrame(self.data.iloc[:, 21])
            #fragmentamos el nombre de la columna
            tem=columna_seleccionada.columns.values
            tem=tem[0].split("-")
            periodo=tem[1]
            tem=tem[0].split(" ")
            genero=tem[0]
            ano=tem[1]
            # Cambiamos el sexo por genero
            if genero =="Mujer":
                genero="Femenino"
            else:
                genero="Masculino"

            # Crear un DataFrame de ejemplo
            df_tem = {
                'Inscritos': columna_seleccionada.iloc[:, 0],
                'Genero': genero,
                'Año': ano,
                'Periodo': periodo
            }

            df_tem= pd.DataFrame(df_tem)
            df_final = pd.concat([df_base, df_tem], axis=1)
            ##################

            for x in range(22,ct):
                #Columna A trabajar
                columna_seleccionada =pd.DataFrame(self.data.iloc[:, x])
                #fragmentamos el nombre de la columna
                tem=columna_seleccionada.columns.values
                tem=tem[0].split("-")
                periodo=tem[1]
                tem=tem[0].split(" ")
                genero=tem[0]
                ano=tem[1]
                # Cambiamos el sexo por genero
                if genero =="Mujer":
                    genero="Femenino"
                else:
                    genero="Masculino"

                # Crear un DataFrame de ejemplo
                df_tem = {
                    'Inscritos': columna_seleccionada.iloc[:, 0],
                    'Genero': genero,
                    'Año': ano,
                    'Periodo': periodo
                }

                df_tem= pd.DataFrame(df_tem)
                df_unido2 = pd.concat([df_base, df_tem], axis=1)
                df_final= pd.concat([df_final, df_unido2], axis=0)
                
            self.data=df_final

            
        except Exception as exc:
            self.show_error(exc)       







