import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mode

# Definir una función para la conversión
def convertir_a_minutos(valor):
    """
    Convierte un valor de tiempo en formato de minutos a un formato específico (1h o 30m).

    Parameters:
    - valor (str): El valor de tiempo a ser convertido. Debe estar en formato de minutos o contener 'h' o 'm'.

    Returns:
    - str: El valor convertido en formato '1h' si los minutos son mayores a 30, o '30m' si son menores o iguales a 30.
           Si el valor es NaN o "-", se devuelve tal cual.

    Examples:
    >>> convertir_a_minutos('45m')
    '1h'
    
    >>> convertir_a_minutos('20m')
    '30m'
    
    >>> convertir_a_minutos('1h')
    '1h'
    
    >>> convertir_a_minutos('-')
    '-'
    
    >>> convertir_a_minutos(np.nan)
    np.nan
    """
    if pd.isna(valor) or valor == "-":
        return valor  # Dejar como está si es NaN o "-"

    if 'h' in valor:
        return valor  # Dejar como está si ya está en formato de horas

    if 'm' in valor:
        total_minutos = int(valor.split('m')[0])
    else:
        return valor  # Dejar como está si no tiene ni 'h' ni 'm'

    # Convertir a 1h si los minutos son mayores a 30, a 30m si son menores o iguales a 30
    if total_minutos > 30:
        return '1h'
    else:
        return '30m'