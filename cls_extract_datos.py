# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 19:50:00 2023

@author: camil
"""

try:
    import requests
    from pyxlsb import open_workbook as open_xlsb

    import pandas as pd
    import os
    
except Exception as exc:
            print('Module(s) {} are missing.:'.format(str(exc)))

#%%
class Extract_data(object):
    
    
    def __init__(self, path=None):
        self.path = path
        self.data = None
        self.ld = None


#%%
     
    def descargar_archivo(self,url, ruta_destino):
        '''
        Descarga el archivo solicitado

        Parameters
        ----------
        Url : Direccion_Web del archivo
        Destino :Ruta en donde se guardara el archivo

        Returns
        -------
        None.

        '''
        
        try:
            response = requests.get(url)
            # Lanza una excepción si ocurrió un error en la descarga
            response.raise_for_status()  
            
            with open(ruta_destino, 'wb') as archivo:
                archivo.write(response.content)
            
            print("Descarga exitosa.")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar el archivo: {e}")
#%%    
    # Carga datos desde archivos 
    def get_data(self, the_path):
        '''
        Parameters
        ----------
        the_path : ruta donde se encuentra el archivo


        Returns
        -------
        None.

        '''

        try:

            df = pd.DataFrame()
            
            with open_xlsb(the_path) as wb:
                with wb.get_sheet(1) as sheet:
                    datos = []
                    
                    for row in sheet.rows():

                        valores = [item.v for item in row]
                        datos.append(valores)
                        
                    df = pd.DataFrame(datos[1:], columns=datos[0])
                        
                
            
            self.data = df
            
        except Exception as exc:
            self.show_error(exc)
#%%
    # Carga datos desde archivos 
    def Eliminar_filas(self, inicio,fin):
        '''
        Parameters
        ----------
        Ininio : fila inicio para eleiminar
        fin: fila final para eleiminar


        Returns
        -------
        None.

        '''

        try:
            
            self.data = self.data.drop(self.data.index[inicio:fin])
            self.data = self.data.reset_index(drop=True)
            print("Filas eliminadas desde la fila  {} hasta la fila {}".format(inicio, fin))

            
        except Exception as exc:
            self.show_error(exc)
#%%
    # Designa nueva cabecera
    def Nueva_Cabecera(self, nc):
        '''
        Parameters
        ----------
        nc : la nueva cabcera



        Returns
        -------
        None.

        '''

        try:
            self.data.columns = self.data.iloc[nc]
            self.data = self.data.drop(nc)
            self.data = self.data.reset_index(drop=True)

            
        except Exception as exc:
            self.show_error(exc)
#%%
    # Designa nueva cabecera
    def Agrupar_Datos(self):
        '''
        Parameters
        ----------
        None



        Returns
        -------
        None.

        '''

        try:
            
            # Definir los valores a reemplazar y sus correspondientes reemplazos en la columna 'Columna1'
            reemplazos = { 'CIENCIA DE LA INFORMACION - BIBLIOTECOLOGIA': 'CIENCIA DE LA INFORMACION Y BIBLIOTECOLOGIA',
                            'COMUNICACION SOCIAL - PERIODISMO': 'COMUNICACION SOCIAL Y PERIODISMO',
                            'COMUNICACION SOCIAL  PERIODISMO': 'COMUNICACION SOCIAL Y PERIODISMO',
                            'COMUNICACION SOCIAL PERIODISMO': 'COMUNICACION SOCIAL Y PERIODISMO', 
                            'COMUNICACION SOCIAL- PERIODISMO': 'COMUNICACION SOCIAL Y PERIODISMO', 
                            'COMUNICACION SOCIAL-PERIODISMO': 'COMUNICACION SOCIAL Y PERIODISMO',
                            'COMUNICACION SOCIALY PERIODISMO': 'COMUNICACION SOCIAL Y PERIODISMO',
                            'COMUNICACION Y PERIODISMO': 'COMUNICACION SOCIAL Y PERIODISMO',
                            'DEPORTE Y ACTIVIDADA FISICA': 'DEPORTE Y ACTIVIDAD FISICA',
                            'DISEÑO DE MODA': 'DISEÑO DE MODAS',
                            'DOCTORADO EN CIENCIAS AGROPECUARIAS AREA AGRARIA': 'DOCTORADO EN CIENCIAS AGROPECUARIAS - AREA AGRARIA',
                            'DOCTORADO EN CIENCIAS AGROPECUARIAS- AREA AGRARIA': 'DOCTORADO EN CIENCIAS AGROPECUARIAS - AREA AGRARIA',
                            'DOCTORADO EN CIENCIAS- BIOLOGIA': 'DOCTORADO EN CIENCIAS BIOLOGICAS',
                            'DOCTORADO EN CIENCIAS -QUIMICA-': 'DOCTORADO EN CIENCIAS QUIMICAS',
                            'ESPECIALIZACION EN ADMINISTRACION DE SALUD: ENFASIS EN SEGURIDAD SOCIAL': 'ESPECIALIZACION EN ADMINISTRACION DE SALUD:ENFASIS EN SEGURIDAD SOCIAL',
                            'ESPECIALIZACION EN ANESTESIA CARDIOVASCULAR Y TORACICA': 'ESPECIALIZACION EN ANESTESIA CARDIOVASCULAR Y TORAXICA',
                            'ESPECIALIZACION EN ASEGURAMIENTO DE LA CALIDAD MICROBIOLOGICA DE LOS ALIMENTOS': 'ESPECIALIZACION EN ASEGURAMIENTO DE LA CALIDAD MICROBIOLOGICA DE ALIMENTOS',
                            'ESPECIALIZACION EN AUDITORIA Y GARANTIA DE CALIDAD EN SALUD': 'ESPECIALIZACION EN AUDITORIA Y GARANTIA DE LA CALIDAD EN SALUD'
                        }
            #Reemplazamos los datos en celda Programa para luego agruparla
            self.data['Programa Académico'] = self.data['Programa Académico'].replace(reemplazos)
            
            
            self.data = self.data.groupby(['Código de \nla Institución', 'IES PADRE',
                                          'Institución de Educación Superior (IES)',
                                           'Principal\n o\nSeccional', 'Sector IES', 'Carácter IES',
                                           'Código del \ndepartamento\n(IES)',
                                           'Departamento de \ndomicilio de la IES',
                                           'Código del \nMunicipio\n(IES)',
                                           'Municipio de\ndomicilio de la IES',
                                           'Código \nSNIES del\nprograma', 'Programa Académico',
                                           'Nivel de Formación', 'Nivel Académico',
                                           'Metodología \ndel programa', 'Área de Conocimiento',
                                           'Núcleo Básico del Conocimiento (NBC)',
                                           'Código del \nDepartamento\n(Programa)',
                                           'Departamento de oferta del programa',
                                           'Código del \nMunicipio\n(Programa)',
                                           'Municipio de oferta del programa'
                                           ]).sum().reset_index()
            
            
        except Exception as exc:
            self.show_error(exc)


#%%
    # Control de exceptions
    def show_error(self,ex):
        '''
        Captura el tipo de error, su description y localización.

        Parameters
        ----------
        ex : Object
            Exception generada por el sistema.

        Returns
        -------
        None.

        '''
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                          "filename": tb.tb_frame.f_code.co_filename,
                          "name": tb.tb_frame.f_code.co_name,
                          "lineno": tb.tb_lineno
                          })
            
            tb = tb.tb_next
            
        print('{}Something went wrong:'.format(os.linesep))
        print('---type:{}'.format(str(type(ex).__name__)))
        print('---message:{}'.format(str(type(ex))))
        print('---trace:{}'.format(str(trace)))
        

            
            


