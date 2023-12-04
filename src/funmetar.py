import numpy as np
import pylab as plt   
import seaborn as sns
import pandas as pd
import re
def check_nan(df: pd.DataFrame) -> None:
    

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
def fix_hum_column(row):
    """
    Corrige la columna 'Relative_hum' en un DataFrame.
    
    Se examina el valor de 'Relative_hum' en una fila dada. Si el valor está marcado como '>', se intenta extraer 
    el porcentaje de humedad de la columna 'Pressure' y devuelve el valor encontrado. En caso de no hallar el valor, 
    se mantiene 'Relative_hum' sin cambios.
    
    Parameters
    ----------
    row : pandas.Series
        Fila de un DataFrame. Se asume que contiene al menos las columnas 'Relative_hum' y 'Pressure'.

    Returns
    -------
    str
        Si 'Relative_hum' contiene '>', se intenta extraer el porcentaje de humedad de 'Pressure'. Si se encuentra, 
        se devuelve el valor. En caso contrario, se devuelve 'Relative_hum' sin modificar.

    Notes
    -----
    Se asume que 'Pressure' contiene una cadena que incluye el valor de humedad (expresado en porcentaje) para 
    'Relative_hum' cuando 'Relative_hum' tiene el valor '>'. El valor esperado está en formato de dos caracteres 
    seguidos por el símbolo '%' (por ejemplo, '85%'). Si no se encuentra ningún valor, se mantiene 'Relative_hum' 
    sin cambios.

    """
    
    if row['Relative_hum'].strip() == '>':
        match = re.search(r'(\w{2})%', row['Pressure'])
        
        if match:
            return match.group(1)
        else:
            return row['Relative_hum']
    else:
        return row['Relative_hum']


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


