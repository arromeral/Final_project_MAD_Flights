from joblib import Parallel, delayed

from joblib import parallel_backend
from joblib import load
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



def generar_columna_gust(valor):
    """
    Extrae los dos primeros dígitos seguidos de un espacio del valor de la columna pressure
    ya que erroneamente los valores de ráfagas(gusts) cuando los hay se encuentran es esta columna.
    
    Parameters
    ----------
    valor : str
        Cadena de entrada desde la cual se intentan extraer los dos primeros dígitos.

    Returns
    -------
    str or int
        Si se encuentran dos dígitos seguidos de un espacio al principio de 'valor', se devuelve 
        la cadena que representa esos dos dígitos. De lo contrario, se devuelve 0.
        
    """
 
    pattern = re.compile(r'^(\d{2})\s')  # Dos dígitos seguidos de un espacio
    match = pattern.match(valor)

    if match:
        return match.group(1)

    else:
        return 0 
    

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

def create_acc_gusts():
    url = 'https://en.tutiempo.net/records/lemd/'

    condition_dict = {'Chance of Rain': 0.0,'Chance of Showers': 0.5,'Clear': 0.0,'Cloudy': 0.0,'Drizzle': 0.0,'Fair': 0.0,'Fog': 1.0,
    'Fog Patches': 0.0,'Freezing': 1.0,'Hail': 0.5,'Light Rain': 0.5,'Light Snow': 1.0,'Mist': 0.0,'Mostly Cloudy': 0.0,    
    'Partly Cloudy': 0.0,'Rain': 0.5,'Rain and Snow': 1.0,'Snow': 1.0,'T-Storm': 1.0,'Widespread Fog': 0.5}

    opciones = Options()
    opciones.add_extension('drivers/adblock.crx')  # adblocker
    opciones.add_argument('cookies=cookies')  # man

    # Inicializo el driver
    driver = webdriver.Chrome(options=opciones)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    time.sleep(20)

    # Esperar a que aparezca el botón de aceptar normas
    normas_button_xpath = '/html/body/div[18]/div[2]/div[1]/div[2]/div[2]/button[1]'
    wait.until(EC.element_to_be_clickable((By.XPATH, normas_button_xpath)))
    normas_button = driver.find_element(By.XPATH, normas_button_xpath)
    normas_button.click()
    print("Aceptado normas")

    # Esperar a que aparezca el botón de aceptar cookies
    cookies_button_xpath = '//*[@id="DivAceptarCookies"]/div/a[2]'
    wait.until(EC.element_to_be_clickable((By.XPATH, cookies_button_xpath)))
    cookies_button = driver.find_element(By.XPATH, cookies_button_xpath)
    cookies_button.click()
    print("Aceptadas cookies")

    # Esperar a que aparezca el botón de aceptar cookies
    last_button_xpath = '//*[@id="ColumnaIzquierda"]/div/div[3]/input'
    wait.until(EC.element_to_be_clickable((By.XPATH, last_button_xpath)))
    last_button = driver.find_element(By.XPATH, last_button_xpath)
    last_button.click()
    print("View last 24h")

    # Esperar a que cargue la página (usando un elemento en la tabla como referencia)
    wait.until(EC.presence_of_element_located((By.XPATH, '//table//tbody//tr[3]')))
    print("Página cargada")

    day = driver.find_elements(By.XPATH, '//table//tbody//tr')[1].text

    time.sleep(5)

    table = [
        row.text.split('\n')[0:3] + row.text.replace(' km/h', '').split('\n')[-1].split(' ', 2)
        for row in driver.find_elements(By.XPATH, '//table//tbody//tr')[3::2]
    ]  # Copia los registros

    print("Registros extraídos")

    columns = ["Day", "Hour", "Condition", "Temperature", "Wind", "Relative_hum", "Pressure"]  # Añade las columnas

    for i in table:
        i.insert(0, day)  # Inserta los registros en la tabla

    gs = pd.DataFrame(table, columns=columns)
    gs = gs.dropna()

    gs['gusts'] = gs['Pressure'].apply(generar_columna_gust)
    gs['bad_weather'] = gs['Condition'].map(condition_dict)

    gust = gs.gusts.loc[:20].sum()  # Añade programación defensiva
    bad_weather = gs.bad_weather.loc[:20].sum()
    driver.quit()  # Cerrar el navegador después de la extracción de datos

    return gust , bad_weather

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
        wait = WebDriverWait(driver, 33)
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
    fl[['acc_Gusts','acc_bad_weather']] = create_acc_gusts()
<<<<<<< HEAD
    fl.Condition[fl.Condition.str.strip() == 'Mostly cloudy'] = 'Mostly Cloudy'
=======
    
>>>>>>> 8278c306b701fd8bd0ce93eeae23b0c5ae3afd99
    return fl

def predecir_y_asignar_tipos_retraso(fl):
    # Importar modelos y escaladores
    modelo_clasificacion = load('modelos_ML/modelo_clasificacion.joblib')
    escalador_clasificacion = load('modelos_ML/escalador_clasificacion.joblib')
    modelo_regresion = load('modelos_ML/modelo_regresion.joblib')
    escalador_regresion = load('modelos_ML/escalador_regresion.joblib')
    print('Empezando prediciones')
    # Listas de valores categóricos
    col_dum = ['duration', 'Temperature', 'Wind', 'acc_Gusts', 'acc_bad_weather', 'week_num_1',
            'week_num_2', 'week_num_3', 'week_num_4', 'week_num_5', 'week_num_6', 'week_num_7', 'week_num_8', 
            'week_num_9', 'week_num_10', 'week_num_11', 'week_num_12', 'week_num_13', 'week_num_14', 'week_num_15',
            'week_num_16', 'week_num_17', 'week_num_18', 'week_num_19', 'week_num_20', 'week_num_21', 'week_num_22', 
            'week_num_23', 'week_num_24', 'week_num_25', 'week_num_26', 'week_num_27', 'week_num_28', 'week_num_29',
            'week_num_30', 'week_num_31', 'week_num_32', 'week_num_33', 'week_num_34', 'week_num_35', 'week_num_36', 
            'week_num_37', 'week_num_38', 'week_num_39', 'week_num_40', 'week_num_41', 'week_num_42', 'week_num_43', 
            'week_num_44', 'week_num_45', 'week_num_46', 'week_num_47', 'week_num_48', 'week_num_49', 'week_num_50',
            'week_num_51', 'week_num_52', 'week_num_53', 'Condition_Chance of Showers', 'Condition_Clear', 
            'Condition_Cloudy', 'Condition_Drizzle', 'Condition_Fair', 'Condition_Fog', 'Condition_Fog Patches', 
            'Condition_Freezing', 'Condition_Hail', 'Condition_Light Rain', 'Condition_Light Snow', 'Condition_Mist',
            'Condition_Mostly Cloudy', 'Condition_Partly Cloudy', 'Condition_Rain', 'Condition_Rain and Snow', 
            'Condition_Snow', 'Condition_T-Storm', 'Condition_Widespread Fog', 'week_day_Monday', 'week_day_Saturday', 
            'week_day_Sunday', 'week_day_Thursday', 'week_day_Tuesday', 'week_day_Wednesday', 'day_time_Early Morning', 
            'day_time_Morning', 'day_time_Night', 'cod_airliner_IATA_2L', 'cod_airliner_IATA_2W', 'cod_airliner_IATA_3O',
            'cod_airliner_IATA_3V', 'cod_airliner_IATA_5O', 'cod_airliner_IATA_5X', 'cod_airliner_IATA_6H', 
            'cod_airliner_IATA_9U', 'cod_airliner_IATA_A3', 'cod_airliner_IATA_AA', 'cod_airliner_IATA_AC', 
            'cod_airliner_IATA_AF', 'cod_airliner_IATA_AH', 'cod_airliner_IATA_AI', 'cod_airliner_IATA_AM', 
            'cod_airliner_IATA_AR', 'cod_airliner_IATA_AT', 'cod_airliner_IATA_AV', 'cod_airliner_IATA_AY', 
            'cod_airliner_IATA_AZ', 'cod_airliner_IATA_BA', 'cod_airliner_IATA_BF', 'cod_airliner_IATA_BT', 
            'cod_airliner_IATA_C2', 'cod_airliner_IATA_CA', 'cod_airliner_IATA_CU', 'cod_airliner_IATA_CX',
            'cod_airliner_IATA_D0', 'cod_airliner_IATA_D8', 'cod_airliner_IATA_DL', 'cod_airliner_IATA_DT',
            'cod_airliner_IATA_DY', 'cod_airliner_IATA_E9', 'cod_airliner_IATA_EB', 'cod_airliner_IATA_EI', 
            'cod_airliner_IATA_EK', 'cod_airliner_IATA_ES', 'cod_airliner_IATA_ET', 'cod_airliner_IATA_EW',
            'cod_airliner_IATA_EY', 'cod_airliner_IATA_FB', 'cod_airliner_IATA_FI', 'cod_airliner_IATA_FR',
            'cod_airliner_IATA_FX', 'cod_airliner_IATA_HU', 'cod_airliner_IATA_HV', 'cod_airliner_IATA_I2', 
            'cod_airliner_IATA_IB', 'cod_airliner_IATA_JD', 'cod_airliner_IATA_JJ', 'cod_airliner_IATA_JU',
            'cod_airliner_IATA_KE', 'cod_airliner_IATA_KL', 'cod_airliner_IATA_KM', 'cod_airliner_IATA_KU',
            'cod_airliner_IATA_LA', 'cod_airliner_IATA_LG', 'cod_airliner_IATA_LH', 'cod_airliner_IATA_LO',
            'cod_airliner_IATA_LX', 'cod_airliner_IATA_LY', 'cod_airliner_IATA_ME', 'cod_airliner_IATA_MS',
            'cod_airliner_IATA_MU', 'cod_airliner_IATA_NI', 'cod_airliner_IATA_NP', 'cod_airliner_IATA_OB', 
            'cod_airliner_IATA_OE', 'cod_airliner_IATA_OG', 'cod_airliner_IATA_OK', 'cod_airliner_IATA_Other',
            'cod_airliner_IATA_PC', 'cod_airliner_IATA_PM', 'cod_airliner_IATA_PS', 'cod_airliner_IATA_PU',
            'cod_airliner_IATA_QR', 'cod_airliner_IATA_QS', 'cod_airliner_IATA_QY', 'cod_airliner_IATA_RJ', 
            'cod_airliner_IATA_RK', 'cod_airliner_IATA_RO', 'cod_airliner_IATA_SN', 'cod_airliner_IATA_SU', 
            'cod_airliner_IATA_SV', 'cod_airliner_IATA_TK', 'cod_airliner_IATA_TO', 'cod_airliner_IATA_TP', 
            'cod_airliner_IATA_TS', 'cod_airliner_IATA_TU', 'cod_airliner_IATA_U2', 'cod_airliner_IATA_UA', 
            'cod_airliner_IATA_UX', 'cod_airliner_IATA_V7', 'cod_airliner_IATA_VY', 'cod_airliner_IATA_W6',
            'cod_airliner_IATA_WT', 'cod_airliner_IATA_YW']

    lista_aerolineas = ['TP', 'IB', 'FX', 'UX', 'LA', 'SU', 'WT', '5O', 'BA', 'LH', 'KL', 'AZ', 'FR', 'VY', 'D8', 'U2', 'QY',
                    'AV', 'QR', 'DL', 'TO', 'AA', 'EY', 'AF', 'PU', 'AY', '0B', 'RO', 'AT', 'AC', '3O', 'CA', 'TU', 'UA', 
                    'EI', 'TK', 'LY', 'SN', 'PC', 'E9', 'EW', 'EK', 'AM', 'MS', 'OK', 'LX', 'RJ', 'A3', 'V7', 'ET', 'LG', 
                    'W6', 'AH', 'OB', '5X', 'AR', 'C2', 'CX', 'FB', 'SV', 'LO', 'KE', 'AI', 'MU', 'PS', 'CU', 'JD', 'EB', 
                    '9U', 'JJ', 'JU', 'QS', 'HV', 'I2', '6H', 'DY', '3V', 'YW', 'ES', '2L', 'BF', 'HU', 'BT', 'KM', 'FI', 
                    'TS', 'ME', 'OE', 'PM', 'D0', 'NI', 'NP', '2W', 'RK', 'KU', 'OG', 'DT']

    lista_conditions = ['Clear','Partly Cloudy','Mostly Cloudy','Fair','Rain','Light Rain','Mist','Drizzle','Cloudy',
                    'Fog Patches','Fog','Freezing','Rain and Snow','Snow','Light Snow','Chance of Showers','Hail',
                    'T-Storm','Chance of Rain','Widespread Fog']
    
    reorder = ['duration', 'Temperature', 'Wind', 'acc_Gusts', 'acc_bad_weather', 'Condition_Chance of Showers', 
           'Condition_Clear', 'Condition_Cloudy', 'Condition_Drizzle', 'Condition_Fair', 'Condition_Fog',
           'Condition_Fog Patches', 'Condition_Freezing', 'Condition_Hail', 'Condition_Light Rain', 'Condition_Light Snow',
           'Condition_Mist', 'Condition_Mostly Cloudy', 'Condition_Partly Cloudy', 'Condition_Rain', 'Condition_Rain and Snow',
           'Condition_Snow', 'Condition_T-Storm', 'Condition_Widespread Fog', 'day_time_Early Morning', 'day_time_Morning',
           'day_time_Night', 'week_day_Monday', 'week_day_Saturday', 'week_day_Sunday', 'week_day_Thursday', 'week_day_Tuesday',
           'week_day_Wednesday', 'week_num_1', 'week_num_2', 'week_num_3', 'week_num_4', 'week_num_5', 'week_num_6',
           'week_num_7', 'week_num_8', 'week_num_9', 'week_num_10', 'week_num_11', 'week_num_12', 'week_num_13', 
           'week_num_14', 'week_num_15', 'week_num_16', 'week_num_17', 'week_num_18', 'week_num_19', 'week_num_20',
           'week_num_21', 'week_num_22', 'week_num_23', 'week_num_24', 'week_num_25', 'week_num_26', 'week_num_27', 
           'week_num_28', 'week_num_29', 'week_num_30', 'week_num_31', 'week_num_32', 'week_num_33', 'week_num_34', 
           'week_num_35', 'week_num_36', 'week_num_37', 'week_num_38', 'week_num_39', 'week_num_40', 'week_num_41', 
           'week_num_42', 'week_num_43', 'week_num_44', 'week_num_45', 'week_num_46', 'week_num_47', 'week_num_48', 
           'week_num_49', 'week_num_50', 'week_num_51', 'week_num_52', 'week_num_53', 'cod_airliner_IATA_2L', 
           'cod_airliner_IATA_2W', 'cod_airliner_IATA_3O', 'cod_airliner_IATA_3V', 'cod_airliner_IATA_5O',
           'cod_airliner_IATA_5X', 'cod_airliner_IATA_6H', 'cod_airliner_IATA_9U', 'cod_airliner_IATA_A3', 
           'cod_airliner_IATA_AA', 'cod_airliner_IATA_AC', 'cod_airliner_IATA_AF', 'cod_airliner_IATA_AH', 
           'cod_airliner_IATA_AI', 'cod_airliner_IATA_AM', 'cod_airliner_IATA_AR', 'cod_airliner_IATA_AT',
           'cod_airliner_IATA_AV', 'cod_airliner_IATA_AY', 'cod_airliner_IATA_AZ', 'cod_airliner_IATA_BA',
           'cod_airliner_IATA_BF', 'cod_airliner_IATA_BT', 'cod_airliner_IATA_C2', 'cod_airliner_IATA_CA',
           'cod_airliner_IATA_CU', 'cod_airliner_IATA_CX', 'cod_airliner_IATA_D0', 'cod_airliner_IATA_D8',
           'cod_airliner_IATA_DL', 'cod_airliner_IATA_DT', 'cod_airliner_IATA_DY', 'cod_airliner_IATA_E9',
           'cod_airliner_IATA_EB', 'cod_airliner_IATA_EI', 'cod_airliner_IATA_EK', 'cod_airliner_IATA_ES',
           'cod_airliner_IATA_ET', 'cod_airliner_IATA_EW', 'cod_airliner_IATA_EY', 'cod_airliner_IATA_FB',
           'cod_airliner_IATA_FI', 'cod_airliner_IATA_FR', 'cod_airliner_IATA_FX', 'cod_airliner_IATA_HU',
           'cod_airliner_IATA_HV', 'cod_airliner_IATA_I2', 'cod_airliner_IATA_IB', 'cod_airliner_IATA_JD',
           'cod_airliner_IATA_JJ', 'cod_airliner_IATA_JU', 'cod_airliner_IATA_KE', 'cod_airliner_IATA_KL',
           'cod_airliner_IATA_KM', 'cod_airliner_IATA_KU', 'cod_airliner_IATA_LA', 'cod_airliner_IATA_LG',
           'cod_airliner_IATA_LH', 'cod_airliner_IATA_LO', 'cod_airliner_IATA_LX', 'cod_airliner_IATA_LY', 
           'cod_airliner_IATA_ME', 'cod_airliner_IATA_MS', 'cod_airliner_IATA_MU', 'cod_airliner_IATA_NI',
           'cod_airliner_IATA_NP', 'cod_airliner_IATA_OB', 'cod_airliner_IATA_OE', 'cod_airliner_IATA_OG',
           'cod_airliner_IATA_OK', 'cod_airliner_IATA_Other', 'cod_airliner_IATA_PC', 'cod_airliner_IATA_PM',
           'cod_airliner_IATA_PS', 'cod_airliner_IATA_PU', 'cod_airliner_IATA_QR', 'cod_airliner_IATA_QS',
           'cod_airliner_IATA_QY', 'cod_airliner_IATA_RJ', 'cod_airliner_IATA_RK', 'cod_airliner_IATA_RO', 
           'cod_airliner_IATA_SN', 'cod_airliner_IATA_SU', 'cod_airliner_IATA_SV', 'cod_airliner_IATA_TK',
           'cod_airliner_IATA_TO', 'cod_airliner_IATA_TP', 'cod_airliner_IATA_TS', 'cod_airliner_IATA_TU', 
           'cod_airliner_IATA_U2', 'cod_airliner_IATA_UA', 'cod_airliner_IATA_UX', 'cod_airliner_IATA_V7', 
           'cod_airliner_IATA_VY', 'cod_airliner_IATA_W6', 'cod_airliner_IATA_WT', 'cod_airliner_IATA_YW']
    # Preprocesamiento de datos a predecir 
    fl['cod_airliner_IATA'] = fl['cod_airliner_IATA'].apply(lambda x: x if x in lista_aerolineas else 'Other')
    fl = fl[fl['Condition'].isin(lista_conditions)]
    fl.Condition[fl.Condition == 'Mostly cloudy'] = 'Mostly Cloudy'
    fl = fl[fl.duration.notna()]
    fl_p = fl[['week_day', 'week_num','cod_airliner_IATA','duration',
           'Condition', 'Temperature', 'Wind', 'day_time', 'acc_Gusts',
           'acc_bad_weather']]

    # One Hot Encoding
    fl_p=pd.get_dummies(fl_p, columns=['week_num','Condition','week_day','day_time','cod_airliner_IATA'], drop_first=True)
    fl_p = fl_p.reindex(columns=col_dum, fill_value=0)

    # Normalización
    fl_p[['duration','Temperature', 'Wind', 'acc_Gusts','acc_bad_weather']] = escalador_clasificacion.transform(fl_p[['duration','Temperature', 'Wind', 'acc_Gusts','acc_bad_weather']])

    # Predicción
    fl_pred = modelo_clasificacion.predict(fl_p)

    # Aplicación del umbral
    prob = modelo_clasificacion.predict_proba(fl_p)

    fl_copy = fl.copy()
    fl_pred = [1 if e[1]>0.32 else 0 for e in prob]
    fl_copy['Delayed'] = fl_pred
    print('Pre-clasificación completada')
    # Importar modelos y ML y los escaladores
    fl_p2 = fl[['week_day', 'week_num','cod_airliner_IATA','duration',
           'Condition', 'Temperature', 'Wind', 'day_time', 'acc_Gusts',
           'acc_bad_weather']]

    # One Hot Encoding
    fl_p2=pd.get_dummies(fl_p2, columns=['week_num','Condition','week_day','day_time','cod_airliner_IATA'], drop_first=True)
    fl_p2 = fl_p2.reindex(columns=col_dum, fill_value=0)

    # Normalización
    fl_p2[['duration','Temperature', 'Wind', 'acc_Gusts','acc_bad_weather']] = escalador_regresion.transform(fl_p2[['duration','Temperature', 'Wind', 'acc_Gusts','acc_bad_weather']])

    # Reordenación columnas
    
    fl_p2 = fl_p2[reorder]

    # Predicción
    fl_pred2 = modelo_regresion.predict(fl_p2)

    fl_copy['Delay'] = fl_pred2
    fl_copy['Delayed'][fl_copy['Delay'] < 15] = 0
    fl_copy['Delayed'][fl_copy['Delay'] < 15] = 0
    fl_copy['Delay'] =   fl_copy['Delay'] + 10
    fl_copy['Delay'][fl_copy.Delayed == 0] = 0

    # Definir las condiciones y los valores correspondientes
    conditions = [
        ((fl_copy['Delay'] == 0 )|(fl_copy['Delay'] < 15 ) ),
        (fl_copy['Delay'] < 30),
        (fl_copy['Delay'] < 60),
        (fl_copy['Delay'] >= 60)
    ]

    values = ['Tipo 0', 'Tipo 1', 'Tipo 2', 'Tipo 3']

    # Crear la columna 'Tipo' utilizando np.select
    fl_copy['Tipo'] = np.select(conditions, values, default='Otro')
    fl_copy['Tipo'][fl_copy.status == 'Delayed'] = 'Tipo 4'
    fl_copy['Tipo'][fl_copy.status == 'Cancelled'] = 'Tipo 5'
    print('Prediciones completadas')
    return fl_copy