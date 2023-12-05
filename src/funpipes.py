from joblib import Parallel, delayed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select   # seleccion de un dropdown
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import pylab as plt   
import seaborn as sns
import multiprocessing as mp
import warnings
warnings.filterwarnings('ignore')

from joblib._parallel_backends import LokyBackend
import asyncio

from tqdm.notebook import tqdm
from datetime import datetime, timedelta
import re


def obtener_duracion_vuelo(cadena):
    match = re.search(r'(\d+)h (\d+)m|\d+m|\d+h', cadena)

    if match:
        horas = match.group(1)
        minutos = match.group(2)

        if horas:
            duracion_total = int(horas) * 60
        else:
            duracion_total = 0

        if minutos:
            duracion_total += int(minutos)

        return duracion_total
    else:
        return None

def obtener_fecha_manana():
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Calcular la fecha del día siguiente
    fecha_manana = fecha_actual + timedelta(days=1)

    # Formatear la fecha como "YYYY-MM-DD"
    formato_fecha = fecha_manana.strftime("%Y-%m-%d")

    return formato_fecha

def scrape_tutiempo_data():
    # Inicializar el driver de Chrome
    url = 'https://en.tutiempo.net/madrid-barajas.html?data=hourly&v=list'
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 33)

    # Esperar a que aparezca el botón de aceptar normas
    normas_button_xpath = '/html/body/div[16]/div[2]/div[1]/div[2]/div[2]/button[1]/p'
    normas_button_xpath2 = '/html/body/div[18]/div[2]/div[1]/div[2]/div[2]/button[1]/p'
    
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, normas_button_xpath)))
        normas_button = driver.find_element(By.XPATH, normas_button_xpath)
        normas_button.click()
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, normas_button_xpath2)))
        normas_button = driver.find_element(By.XPATH, normas_button_xpath2)
        normas_button.click()
    
    print("Aceptado normas")

    # Esperar a que aparezca el botón de aceptar cookies
    cookies_button_xpath = '//*[@id="DivAceptarCookies"]/div/a[2]'
    wait.until(EC.element_to_be_clickable((By.XPATH, cookies_button_xpath)))
    cookies_button = driver.find_element(By.XPATH, cookies_button_xpath)
    cookies_button.click()
    
    print("Aceptadas cookies")

    # Esperar a que cargue la página (usando un elemento en la tabla como referencia)
    wait.until(EC.presence_of_element_located((By.XPATH, '//table//tbody//tr[3]')))
    print("Página cargada")

    # Obtener la fecha del día siguiente
    day = driver.find_elements(By.XPATH, '//table//tbody//tr')[1].text

    time.sleep(5)

    # Copiar los registros
    table = [
        row.text.split('\n')[0:4] + row.text.split('\n')[-1].split(' ')
        for row in driver.find_elements(By.XPATH, '//table//tbody//tr')[6::]
    ]

    print("Registros extraídos")

    # Encontrar el índice de la primera sublista que comienza con 'Tomorrow'
    indice_inicio = next(i for i, sublist in enumerate(table) if sublist[0].startswith('Tomorrow'))

    # Seleccionar las 25 sublistas a partir del índice encontrado
    lista_filtrada = table[indice_inicio:indice_inicio + 26]

    columns = ['Hour', 'Condition', 'Temperature', 'Wind', 'Relative_hum', 'Clouds', 'AP', '1']
    mt = pd.DataFrame(lista_filtrada[2:], columns=columns)
    mt.loc[mt['Condition'].str.lower().str.contains('rain'), 'Condition'] = 'Rain'
    mt = mt[['Hour', 'Condition', 'Temperature', 'Wind']]
    mt['Temperature'] = pd.to_numeric(mt['Temperature'].str[:-1])
    mt['Wind'] = pd.to_numeric(mt['Wind'].str[:-5])
        
    
    # Cerrar el navegador
    driver.quit()

    return mt

def scrape_flightera_data():
    # Obtengo fecha del día siguiente
    tomorrow = obtener_fecha_manana()

    url = f'https://www.flightera.net/en/airport/Madrid/LEMD/departure/{tomorrow}%2000_00'
    
    table2 = []  # Inicializa table como una lista vacía
    
    # Fecha de la URL
    match = re.search(r'\d{4}-\d{2}-\d{2}', url)
    match = match.group()
    
    try:
        # Opciones
        opciones = Options()
        opciones.add_extension('drivers/adblock.crx')       # Adblocker
        opciones.add_argument('cookies=cookies')    # Manejo de cookies

        # Inicializo el driver
        driver = webdriver.Chrome(options=opciones)
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        time.sleep(35)

        # Aceptar cookies
        aceptar = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
        aceptar.click()

        # Extraer la información la primera vez
        table2 += [flight.text.split('\n') for flight in driver.find_elements(By.XPATH, '//table//tbody//tr')[1:]]
        time.sleep(2)

        # Clickar en el botón Later Flights para abrir una nueva URL
        aceptar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/div[6]/div[2]/a')))
        aceptar.click()
        time.sleep(2)

        # Clickar en boton popup
        aceptar2 = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div/div/div/div[3]/span[1]/button')
        aceptar2.click()
        time.sleep(2)

        # Extraer la información la primera vez
        table2 += [flight.text.split('\n') for flight in driver.find_elements(By.XPATH, '//table//tbody//tr')[1:]]
        time.sleep(2)

        aceptar = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[6]/div[2]/a')
        aceptar.click()
        time.sleep(2)

        # Bucle while hasta que la fecha de cada link desaparezca de la URL
        while match in driver.current_url:
            try:
                # Extraer datos
                table2 += [flight.text.split('\n') for flight in driver.find_elements(By.XPATH, '//table//tbody//tr')[1:]]
                
                # Clickar en el botón Later Flights para abrir una nueva URL
                aceptar = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[6]/div[2]/a')
                aceptar.click()
            except:
                # Clickar en boton popup si aparece
                aceptar2 = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div/div/div/div[3]/span[1]/button')
                aceptar2.click()       

    except:
        print("Extraction Failed")
    finally:
        print("Extraction completed")
        driver.quit()

    # Generar el DataFrame
    columns = ['Date', '1', 'Status', 'code', 'airliner', 'mix_data1', 'mix_data2']
    fl = pd.DataFrame(table2, columns=columns)

    # Eliminar nulos
    fl = fl.dropna() 

    # Quedarse solo con los vuelos del día de mañana
    fl = fl[fl.Date == fl.Date.loc[0]] 

    # Convertir la columna 'Date' al formato de fecha
    fl['Date'] = pd.to_datetime(fl['Date'] + ' 2023', format='%a, %d. %b %Y')

    # Generar la columna 'week_day' con el día de la semana en inglés
    fl['week_day'] = fl['Date'].dt.strftime('%A')

    # Generar la columna 'week_num' con el número de la semana (considerando que los registros son de 2023)
    fl['week_num'] = fl['Date'].dt.strftime('%U')
    fl = fl.drop_duplicates(keep='first')
    fl['code'] = fl['code'].str.split().str[0]

    # Generar columnas con el código de la aerolínea, del aeropuerto y la hora
    fl['cod_airliner_IATA'] = fl['mix_data1'].str.extract(r'(\b\w{2})')
    fl['cod_airport_IATA'] = fl['mix_data1'].str.extract(r'\(\s*(\b\w{3})\s*/')  # Modificación aquí
    fl['hora'] = fl['mix_data1'].str.extract(r'(\d{2}:\d{2})')

    # Aplicar la función a la columna mix_data2 y almacenar los resultados en la columna duration
    fl['duration'] = fl['mix_data2'].apply(obtener_duracion_vuelo)
    
    # Redondear la duración total a la unidad de horas
    fl['duration'] = fl['duration'].apply(lambda x: max(round(x / 60), 1))

    # Columnas a eliminar
    columnas_a_eliminar = ['Date', '1', 'airliner', 'mix_data1', 'mix_data2']
    fl = fl.drop(columnas_a_eliminar, axis=1)
    fl = fl.rename(columns={'Status': 'status', 'hora': 'hour', "code": "cod_flight_IATA"})

    return fl

def procesar_datos(fl, mt):
    # Renombrar la columna 'Hour' en el DataFrame 'mt'
    mt = mt.rename(columns={'Hour': 'hour'})

    # Convertir las columnas 'hour' a tipo de datos timedelta en ambos DataFrames
    fl['hour'] = pd.to_datetime(fl['hour'], format='%H:%M').dt.time
    mt['hour'] = pd.to_datetime(mt['hour'], format='%H:%M').dt.time

    # Convertir la columna 'hour' a tipo de datos timedelta en ambos DataFrames
    mt['hour'] = pd.to_timedelta(mt['hour'].astype(str))
    fl['hour'] = pd.to_timedelta(fl['hour'].astype(str))

    # Calcular la cantidad total de segundos desde la medianoche
    mt['seconds_since_midnight'] = mt['hour'].dt.total_seconds()
    fl['seconds_since_midnight'] = fl['hour'].dt.total_seconds()

    # Ordenar ambos DataFrames por la columna 'seconds_since_midnight'
    mt = mt.sort_values('seconds_since_midnight')
    fl = fl.sort_values('seconds_since_midnight')

    # Realizar la fusión en la dirección contraria ('backward')
    fl = pd.merge_asof(fl, mt, on='seconds_since_midnight', direction='backward')

    # Eliminar la columna temporal agregada para la fusión
    fl = fl.drop(columns='seconds_since_midnight')

    # Convertir la columna 'hour_x' al formato de tiempo
    fl['hour_x'] = pd.to_timedelta(fl['hour_x'])

    # Extraer solo la parte de la hora
    fl['hour_x'] = fl['hour_x'].apply(lambda x: '{:02}:{:02}:{:02}'.format(int(x.total_seconds() // 3600), int((x.total_seconds() % 3600) // 60), int(x.total_seconds() % 60)))

    # Seleccionar las columnas deseadas y renombrar la columna 'hour_x' a 'hour'
    fl = fl[['status', 'cod_flight_IATA', 'week_day', 'week_num', 'cod_airliner_IATA', 'cod_airport_IATA', 'hour_x', 'duration', 'Condition', 'Temperature', 'Wind']]
    fl = fl.rename(columns={'hour_x': 'hour'})

    # Convertir la columna 'hour' al formato de tiempo
    fl['hour'] = pd.to_datetime(fl['hour'])

    # Crear una nueva columna 'day_time' basada en las horas del día
    fl['day_time'] = pd.cut(fl['hour'].dt.hour, bins=[0, 6, 12, 18, 24], labels=['Early Morning', 'Morning', 'Afternoon', 'Night'], right=False)

    return fl
