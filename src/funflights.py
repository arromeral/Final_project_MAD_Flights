import time
import numpy as np
import pylab as plt   
import seaborn as sns
import pandas as pd
import re

def check_nan(df: pd.DataFrame) -> None:
    
    """
    Recibe un dataframe y enseña el % de valores nulos
    y lo grafica
    """
    
    nan_cols = df.isna().mean() * 100  # porcentaje de nulo en cada columna
    
    display(f'N nan cols: {len(nan_cols[nan_cols>0])}')
    display(nan_cols[nan_cols>0])
    
    
    # grafico de nulos en el dataframe
    #inicializa figura y establece un tamaño
    plt.figure(figsize=(100, 60)) # 100x60 pixeles

    sns.heatmap(df.isna(),          # datos
                yticklabels=False,  # quita las etiquetas del eje y
                cmap='viridis',     # mapa de color
                cbar=False,         # sin barra lateral
               )

    plt.show();

def add_2023_if_needed(date):
    """
    Agrega '2023' a una fecha si no termina con '2022' o '2023'.
    
    Parameters
    ----------
    date : str
        Fecha en formato de cadena. Se espera que termine con '2022' o '2023' para no ser modificada.

    Returns
    -------
    str
        Si 'date' no termina con '2022' o '2023', se le agrega ' 2023' al final. Si ya termina con alguno de estos, 
        se devuelve 'date' sin cambios.

    Notes
    -----
    La función verifica si 'date' termina con '2022' o '2023'. Si no es así, agrega ' 2023' al final. Esta función 
    asume que 'date' está en un formato en el que se puede agregar simplemente un espacio seguido de '2023' al final.
    """
    if not date.endswith('2022') and not date.endswith('2023'):
        return date + ' 2023'
    return date

def convertir_fecha(date):
    """
    Convierte un string de fecha a un formato reconocible por Pandas.

    Parameters
    ----------
    date : str
        Fecha en formato de cadena. Se espera que siga el formato '%a, %d. %b %Y'.

    Returns
    -------
    str
        Fecha convertida al formato '%Y-%m-%d' si la conversión tiene éxito. Si hay un error en el formato,
        devuelve 'Formato incorrecto'.

    Notes
    -----
    La función intenta convertir 'date' a un formato de fecha reconocible por Pandas. Se espera que 'date' siga
    el formato '%a, %d. %b %Y'. Si tiene éxito, devuelve la fecha convertida en el formato '%Y-%m-%d'. En caso de que 
    la conversión falle, se devuelve el mensaje 'Formato incorrecto'.
    """
    try:
        # Convierte el string de la fecha al formato de fecha reconocible por Pandas
        fecha = pd.to_datetime(date.strip(), format='%a, %d. %b %Y').strftime('%Y-%m-%d')
        return fecha
    except:
        return 'Formato incorrecto'  # Mensaje si hay un formato incorrecto

def separar_valores(dataframe, columna_origen):
    """
    Extrae valores de una columna en un DataFrame en la que se espera
    encontrar las secuencias de los códigos IATA e ICAO de la aerolínea
    y los divide en dos columnas separadas que crea la función.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        El DataFrame que contiene los datos.

    columna_origen : str
        Nombre de la columna del DataFrame desde la cual se extraerán los valores.

    Returns
    -------
    None
        La función modifica el DataFrame proporcionado 'dataframe' al agregar dos nuevas columnas:
        'cod_airliner_IATA' y 'cod_airliner_ICAO'.

    Notes
    -----
    La función utiliza expresiones regulares para extraer dos valores separados por un '/'. Luego, agrega dos
    nuevas columnas al DataFrame 'dataframe': 'cod_airliner_IATA' que almacena el primer valor extraído, y 
    'cod_airliner_ICAO' que almacena el segundo valor extraído.
    """

    # Utilizar expresiones regulares para extraer los valores
    valores = dataframe[columna_origen].str.extract(r'^(?P<Valor_1>[A-Z0-9]+)/(?P<Valor_2>[A-Z0-9]+)')

    # Crear dos nuevas columnas con los valores extraídos
    dataframe['cod_airliner_IATA'] = valores['Valor_1']
    dataframe['cod_airliner_ICAO'] = valores['Valor_2']

def extraer_valores(dataframe, columna_origen):
    """
    Extrae valores de una columna en un DataFrame en la que se espera
    encontrar las secuencias de los códigos IATA e ICAO del aeropuerto y el nombre de la ciudad
    y los divide en tres columnas separadas que crea la función.


    Parameters
    ----------
    dataframe : pandas.DataFrame
        El DataFrame que contiene los datos.

    columna_origen : str
        Nombre de la columna del DataFrame desde la cual se extraerán los valores.

    Returns
    -------
    None
        La función modifica el DataFrame proporcionado 'dataframe' agregando tres nuevas columnas:
        'City', 'cod_airport_IATA', y 'cod_airport_ICAO'.

    Notes
    -----
    Utiliza expresiones regulares para extraer valores relacionados a la información del aeropuerto desde
    la columna dada en el DataFrame 'dataframe'. Posteriormente, agrega tres nuevas columnas al DataFrame
    'dataframe': 'City' para almacenar el nombre de la ciudad, 'cod_airport_IATA' para el código IATA del
    aeropuerto y 'cod_airport_ICAO' para el código ICAO del aeropuerto.
    """
    # Utilizar expresiones regulares para extraer los valores
    valores = dataframe[columna_origen].str.extract(r'[A-Z0-9]{2}/[A-Z0-9]{3}\s([A-Za-z\s\-]+)\s\(([A-Z]{3})\s/\s([A-Z]{4})\)')

    # Crear tres nuevas columnas con los valores extraídos
    dataframe['City'] = valores[0]
    dataframe['cod_airport_IATA'] = valores[1]
    dataframe['cod_airport_ICAO'] = valores[2]

def extraer_hora(dataframe, columna_origen):
    """
    Extrae la hora desde una columna en un DataFrame de datos de vuelo.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        El DataFrame que contiene los datos.

    columna_origen : str
        Nombre de la columna del DataFrame desde la cual se extraerán las horas.

    Returns
    -------
    None
        La función modifica el DataFrame proporcionado 'dataframe' añadiendo una columna 'Scheduled_dep'
        que representa la hora programada de salida.

    Notes
    -----
    Utiliza expresiones regulares para extraer la hora programada de salida desde la columna dada en el
    DataFrame 'dataframe'. Luego, agrega esta hora a una nueva columna llamada 'Scheduled_dep' en el
    DataFrame 'dataframe'.
    """
    # Utilizar expresiones regulares para extraer la hora
    dataframe['Scheduled_dep'] = dataframe[columna_origen].str.extract(r'(\d{2}:\d{2})\s[A-Z0-9]')


def extraer_segunda_hora(dataframe, columna_origen):
    """
    Extrae la segunda hora de una columna en un DataFrame de datos de vuelo.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        El DataFrame que contiene los datos.

    columna_origen : str
        Nombre de la columna del DataFrame desde la cual se extraerá la segunda hora.

    Returns
    -------
    None
        La función modifica el DataFrame proporcionado 'dataframe' añadiendo una columna 'depart_time'
        que representa la segunda hora de salida.

    Notes
    -----
    Utiliza expresiones regulares para extraer la segunda hora de la columna dada en el DataFrame 'dataframe'.
    Luego, agrega esta hora a una nueva columna llamada 'depart_time' en el DataFrame 'dataframe'.
    """
    # Utilizar expresiones regulares para extraer la segunda hora
    dataframe['depart_time'] = dataframe[columna_origen].str.extract(r'\d{2}:\d{2}\s\w+\s(\d{2}:\d{2})\s\w+')

def redondear_horas(valor):
    """
    Redondea los valores de tiempo en horas (formato 'Xh' o 'Xh Xm') al número de horas más cercano.

    Parameters
    ----------
    valor : str
        Valor de tiempo en formato 'Xh' (horas) o 'Xh Xm' (horas y minutos).

    Returns
    -------
    str
        Redondea el valor al número de horas más cercano. Devuelve una cadena con el formato 'Xh'.

    Notes
    -----
    - Si 'valor' está en formato 'Xh Xm', la función extrae las horas y los minutos.
    - Si los minutos son 30 o más, redondea a la siguiente hora.
    - En caso de 'Xm', redondea siempre a 1 hora ('1h').
    - Si 'valor' es solo 'Xh', devuelve el valor original.
    !!!
    """
    valor = valor.replace('Estimated', '').strip()
    
    if 'h' in valor:
        horas = int(re.search(r'\d+', valor).group())
        minutos = 0
        if 'm' in valor:
            minutos_match = re.search(r'\d+', valor[valor.find('h'):])
            minutos = int(minutos_match.group()) if minutos_match else 0

        if minutos >= 30:
            horas += 1

        return f"{horas}h"
    else:
        return valor

def asignar_estado_departure(celda):
    """
    Asigna un estado de salida a los registros de vuelo según la descripción proporcionada.

    Parameters
    ----------
    celda : str
        Descripción del estado de salida del vuelo.

    Returns
    -------
    str
        Estado asignado según la descripción. Puede ser 'on time', 'early', 'late' o '-' si no coincide con ninguno.

    Notes
    -----
    - La función clasifica los registros de vuelos en 'on time', 'early' o 'late' según la descripción.
    - Si la descripción coincide con una de las condiciones, asigna el estado correspondiente.
    - Si la descripción no coincide con ninguna de las condiciones, asigna '-'.
    """
    if 'scheduled' in celda:
        return 'on time'
    elif 'early' in celda:
        return 'early'
    elif 'late' in celda:
        return 'late'
    elif 'on time' in celda:
        return 'on time'
    else:
        return "-"

def calcular_minutos(celda):
    """
    Calcula el tiempo en minutos, ya sea retraso o anticipación, según la descripción proporcionada.

    Parameters
    ----------
    celda : str
        Descripción del estado del tiempo en el vuelo.

    Returns
    -------
    int or str
        Los minutos calculados según la descripción. Puede ser un valor entero positivo o negativo representando el retraso o anticipación, o '-' si no coincide con ninguno.

    Notes
    -----
    - La función analiza la descripción del estado del tiempo en el vuelo y calcula los minutos de retraso o anticipación.
    - Si la descripción está en formato 'Xh Ymin late' o 'Xh Ymin early', calcula el total de minutos según las horas y los minutos indicados.
    - Si la descripción está en formato 'Xmin late' o 'Xmin early', calcula los minutos correspondientes.
    - Si la descripción coincide con 'on time' o 'scheduled', asigna 0 minutos.
    - Si la descripción no coincide con ninguna de las condiciones, asigna '-'.
    """
    match = re.search(r'(\d+)h (\d+)min (late|early)', celda)
    if match:
        horas = int(match.group(1))
        minutos = int(match.group(2))
        valor = horas * 60 + minutos
        if match.group(3) == 'late':
            return valor
        else:
            return -valor
    elif 'min late' in celda or 'min early' in celda:
        minutos = int(re.search(r'(\d+)min (late|early)', celda).group(1))
        if 'late' in celda:
            return minutos
        else:
            return -minutos
    elif 'on time' in celda or 'scheduled' in celda:
        return 0
    else:
        return '-'

def calcular_diferencia(fila):
    """
    Calcula la diferencia entre los minutos de retraso en la salida y en la llegada.

    Parameters
    ----------
    fila : pandas.Series
        Fila del DataFrame que contiene las columnas 'dep_mins_of_delay' y 'arr_mins_of_delay'.

    Returns
    -------
    int
        Diferencia entre los minutos de retraso en la salida y la llegada, si ambos valores son numéricos enteros.
        Si algún valor no puede convertirse a entero o no se proporciona, se devuelve 0.

    Notes
    -----
    - La función intenta restar los minutos de retraso en la salida a los minutos de retraso en la llegada.
    - Si algún valor no es numérico o no está disponible, la función devuelve 0.
    """
    try:
        dep = int(fila['dep_mins_of_delay'])
        arr = int(fila['arr_mins_of_delay'])
        return dep - arr
    except (ValueError, TypeError):
        return 0
