# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:37:28 2020

@author: Ruben
"""
from pathlib import Path
import io
from ftplib import FTP
import datetime as dt

import pandas as pd

IP_DATALOGGER = '138.4.46.201'

def lee_fichero_gl840(file):
    data = pd.read_csv(file, skiprows=37, parse_dates=True, index_col=1, sep=',')
    
    # Deja las columnas que interesan
    data = data[['V', 'V.1', 'V.2', 'V.3', 'V.4', 'V.5',
                 'V.6', 'V.7', 'degC', 'degC.1', 'degC.2', 'degC.3']]
    
    # Quitar los espacios que se encuentran entre el caracter '+' y el digito
    data = data.replace(" ", "", regex=True)
    
    data = data.replace('BURNOUT', 9999).astype(float, errors='raise')
    
    # Se renombran las columnas con los nombres de interés
    # conf. canales anterior a 2020-11
    # data = data.rename(columns={'Time': 'Data&Time', 'V': 'CH1: M1-T', 'V.1': 'CH2: M1-RH',
    #                             'V.2': 'CH3: M2-T', 'V.3': 'CH4: M2-RH', 'V.4': 'CH5: C-T_amb',
    #                             'V.5': 'CH6: C-RH_amb','V.6': 'CH7: M1-SP', 'V.7': 'CH8: M2-SP',
    #                             'degC': 'CH9: M1-Tp Chapa', 'degC.1': 'CH10: M1-Tp Cristal',
    #                             'degC.2': 'CH11: M2-Tp Cristal', 'degC.3': 'CH12: M2-Tp Chapa'})

    data = data.rename(columns={'Time': 'Data&Time', 'V': 'CH1:M1-TEMP', 'V.1': 'CH2:M1-RH',
                                'V.2': 'CH3:M2-TEMP', 'V.3': 'CH4:M2-RH', 'V.4': 'CH5:C-TEMP',
                                'V.5': 'CH6:C-RH','V.6': 'CH7:M2-SP', 'V.7': 'CH8:M1-SP',
                                'degC': 'CH9:M1-Tp FS', 'degC.1': 'CH10:M1-Tp BS',
                                'degC.2': 'CH11:M2-Tp FS', 'degC.3': 'CH12:M2-TP BS'})

    return data

def guarda_ultimo_fichero_sesion(sesion, ip=IP_DATALOGGER, path_sesiones='sesiones'):
    with FTP(host=ip) as ftp:
        ftp.login()
        ftp.cwd('SD1/MEDIDAS/' + sesion)
        file_list = []
        ftp.dir(file_list.append)
        # ftp.dir()
        filename_list = [filename for filename in ' '.join(file_list).split() if '.CSV' in filename]
        
        fichero = sorted(filename_list)[-1]
        print('Leyendo y guardando fichero en carpeta "sesiones": ', fichero)
        
        with open(Path(path_sesiones, fichero), 'wb') as fp:
            ftp.retrbinary(f'RETR {fichero}', fp.write)

def lee_fichero_sesion(fichero_sesion, path_sesiones='sesiones'):
    data = lee_fichero_gl840(Path(path_sesiones, fichero_sesion))
    
    return data

def nombre_fichero_ultima_sesion(ip=IP_DATALOGGER):
    with FTP(host=IP_DATALOGGER) as ftp:
        ftp.login()
        ftp.cwd('SD1/MEDIDAS/')
        dir_list = []
        ftp.dir(dir_list.append)
    
        dirname_list = [dirname.split()[-1] for dirname in dir_list if dirname]
        
        ultima_sesion = sorted(dirname_list)[-1]
        
        ftp.cwd(ultima_sesion)
        file_list = []
        ftp.dir(file_list.append)
        
        filename_list = [filename for filename in ' '.join(file_list).split() if '.CSV' in filename]
    
        fichero = sorted(filename_list)[-1]
        
        return fichero
    
def lee_ultima_sesion(ip=IP_DATALOGGER):
    fichero = nombre_fichero_ultima_sesion(ip)
    print('Leyendo fichero en FTP: ', fichero)
    
    with FTP(host=ip) as ftp:
        ftp.login()
        directorio = fichero[0:6]
        ftp.cwd('SD1/MEDIDAS/'+directorio)
        # download the file but first create a virtual file object for it
        buffer_data = io.BytesIO()
        ftp.retrbinary(f'RETR {fichero}', buffer_data.write)
        buffer_data.seek(0) # after writing go back to the start of the virtual file
        
        data = lee_fichero_gl840(buffer_data)
    
    return data


def diferencia_segundos_comprueba_hora_ftp(ip=IP_DATALOGGER):
    fichero = nombre_fichero_ultima_sesion(ip)
    
    with FTP(host=IP_DATALOGGER) as ftp:
        ftp.login()
        directorio = fichero[0:6]
        ftp.cwd('SD1/MEDIDAS/'+directorio)
        file_list = []
        ftp.dir(file_list.append)
        
        file_prop = [filename for filename in file_list if '.CSV' in filename]
        time_file = file_prop[0].split()[-2]
        
        dt_fichero = dt.datetime.combine(dt.date.today(), dt.time.fromisoformat(time_file))
        dt_actual = dt.datetime.now()
        
        print(dt_fichero, dt_actual)
    
        diferencia_segundos = abs((dt_fichero - dt_actual).total_seconds())   
        
        return diferencia_segundos
