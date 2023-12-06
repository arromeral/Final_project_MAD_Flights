# para ejecutar, escribir por terminal : streamlit run main.py
# %%

from PIL import Image
import streamlit as st
import pandas as pd
import webbrowser
import base64
from datetime import datetime, timedelta

import io
# %%
######################################################################################################################
st.set_page_config(page_title='Mad Flights', page_icon="✈️", layout="wide")
# st.title('MAD Flights')
######################################################################################################################
# st.title("Live Weather in MAD Barajas")
# Código HTML con iframe
html_code = '''
<center>
<div id="TT_yVNEuwkgE4KQpchKKFzk1E6xA6lKBMlEpkEk3" style="width: 600px; height: 130px;">Weather - Tutiempo.net</div>
<script type="text/javascript" src="https://en.tutiempo.net/s-widget/l_yVNEuwkgE4KQpchKKFzk1E6xA6lKBMlEpkEk3"></script>
</center>
'''

# html_code = '''
# <center>
# <div id="TT_yVNEuwkgE4KQpchKKFzk1E6xA6lKBMlEpkEk3">Weather - Tutiempo.net</div>
# <script type="text/javascript" src="https://en.tutiempo.net/s-widget/l_yVNEuwkgE4KQpchKKFzk1E6xA6lKBMlEpkEk3"></script>
# </center>
# '''
# html_code = '''
# <center>
# <iframe id="TTF_FiThuxWheYU9zQsUjauEEcmjA6nU1W1lrdktEZCoK1z53I35m" src="https://en.tutiempo.net/s-widget/tt_NXwxfDI1MjUyNXxufG58bnwyNTEwNHwzMHwxMXwxfDZ8NXwzfDI1fHN8c3xufEU4NkY2Rnw3MUI5RjB8fEJEQkRCRHxGRjdEMDN8NjZ8M3w2OHw2MHwxNDR8MjJ8NzR8MHw1MDV8ODl8Njh8Mzd8MTV8MTV8MzJ8NjF8Mjh8aWp8MXw%2C" frameborder="0" scrolling="no" width="100%" height="100%" allowtransparency="allowtransparency" style="overflow:hidden;pointer-events:auto;"></iframe>
# </center>
# '''

# Insertar HTML usando st.components.html
st.components.v1.html(html_code, height=89)

# img = get_img_as_base64("image.jpg")

# page_bg_img = f"""
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-image: url("https://images.unsplash.com/photo-1624985053839-b53b3045aaac?q=80&w=1972&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
# background-size: 110%;
# background-position: top left;
# background-repeat: space;
# background-attachment: local;
# }}

# """
# st.markdown(page_bg_img, unsafe_allow_html=True)

######################################################################################################################
# st.sidebar.header('MAD Flights Project')
# st.sidebar.subheader('Streamlit Workshop for IH')
# st.sidebar.image(Image.open('logo.png'))
# st.sidebar.image('logo.png')
######################################################################################################################
# Cargar el archivo CSV
df = pd.read_csv('prediciones/prediciones_07_12_2023.csv')

# Variable de estado para controlar la pestaña activa
active_tab = st.sidebar.radio("Navigation", ["🎯 **Flight Delay Predictions**", "📊 **MAD Flights Dashboards**",
"🗺️ **Foursquare Studio Flights map**"])

# Contenido de la pestaña "Flight Predictions"
if active_tab == "🎯 **Flight Delay Predictions**":
    st.header("🎯 Flight Delay Predictions")
    # Widget para el filtro de cod_flight_IATA
    cod_flight_iata = st.selectbox('Write or select your Flight code:', df['cod_flight_IATA'].unique())

    # Widget para el filtro de fecha
    selected_date = pd.to_datetime(st.date_input('Select the day of your flight:')).strftime('%Y-%m-%d')

    # Filtrar el DataFrame
    filtered_df = df[(df['cod_flight_IATA'] == cod_flight_iata) & (df['day'] == selected_date)]

    st.write('Resultado:')
    if not filtered_df.empty:
        result_tipo = filtered_df['Tipo'].iloc[0]

        # Mostrar mensaje según el valor de la columna "Tipo"
        if result_tipo == 'Tipo 0':
            st.write('¡Resultado correspondiente a Tipo 1!')
        elif result_tipo == 'Tipo 1':
            st.write('¡Resultado correspondiente a Tipo 2!')
        elif result_tipo == 'Tipo 2':
            st.write('¡Resultado correspondiente a Tipo 3!')
        elif result_tipo == 'Tipo 3':
            st.write('¡Resultado correspondiente a Tipo 4!')
        elif result_tipo == 'Tipo 4':
            st.write('¡Resultado correspondiente a Tipo 5!')
        else:
            st.write('Tipo no reconocido.')
    else:
        st.write('No hay resultados para la combinación seleccionada.')

elif active_tab == "📊 **MAD Flights Dashboards**":
    st.header("📊 MAD Flights Dashboards")
    iframe_code = '''
    <iframe title="Report Section" width="800" height="1330" src="https://app.powerbi.com/view?r=eyJrIjoiYTc2Yzk0N2MtNGM0Yy00ZjJmLTg5MDktZjM3ZTY5ODdkYWUxIiwidCI6IjZhZmVhODVkLWMzMjMtNDI3MC1iNjlkLWE0ZmIzOTI3YzI1NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
    '''
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_code, unsafe_allow_html=True)

# Contenido de la pestaña "Flight Map"
elif active_tab == "🗺️ **Foursquare Studio Flights map**":
    st.header("🗺️ Foursquare Studio Flights map")
    iframe_code2 = '''
    <iframe width="100%" height="500px" src="https://studio.foursquare.com/public/cb363a0b-a11a-436d-9ecf-c848b70702d4/embed" frameborder="0" allowfullscreen></iframe>
    '''
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_code2, unsafe_allow_html=True)

# ######################################################################################################################
# if st.sidebar.button("📊 MAD Flights Dashboards"):
    # # st.header("MAD Flights Dashboards")
    # iframe_code = '''
    # <iframe title="Report Section" width="800" height="1330" src="https://app.powerbi.com/view?r=eyJrIjoiYTc2Yzk0N2MtNGM0Yy00ZjJmLTg5MDktZjM3ZTY5ODdkYWUxIiwidCI6IjZhZmVhODVkLWMzMjMtNDI3MC1iNjlkLWE0ZmIzOTI3YzI1NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
    # '''
    # # Mostrar el iframe en Streamlit
    # st.markdown(iframe_code, unsafe_allow_html=True)
# ######################################################################################################################

# if st.sidebar.button("🗺️ Foursquare Studio Flights map"):
#     # st.header("Foursquare Studio Flights map")
#     iframe_code2 = '''
#     <iframe width="100%" height="500px" src="https://studio.foursquare.com/public/cb363a0b-a11a-436d-9ecf-c848b70702d4/embed" frameborder="0" allowfullscreen></iframe>
#     '''
#     # Mostrar el iframe en Streamlit
#     st.markdown(iframe_code2, unsafe_allow_html=True)



# # Variable de estado para controlar la visibilidad de la nueva ventana
# show_predictions = False
# # Botón en la barra lateral para abrir la nueva ventana
# if st.sidebar.button("🗺️ Fligth predictions"):
#     show_predictions = True

# # Nueva ventana con la información correspondiente
# if show_predictions:

#     # Cargar el archivo CSV
#     df = pd.read_csv('prediciones/prediciones_07_12_2023.csv')

#     # Widget para el filtro de cod_flight_IATA
#     cod_flight_iata = st.selectbox('Write or select your Flight code:', df['cod_flight_IATA'].unique())

#     # Widget para el filtro de fecha
#     selected_date = pd.to_datetime(st.date_input('Select the day of your flight:')).strftime('%Y-%m-%d')

#     # Filtrar el DataFrame
#     filtered_df = df[(df['cod_flight_IATA'] == cod_flight_iata) & (df['day'] == selected_date)]
#     st.subheader('Flight Predictions')
    
#     st.write('Resultado:')
#     if not filtered_df.empty:
#         result_tipo = filtered_df['Tipo'].iloc[0]

#         # Mostrar mensaje según el valor de la columna "Tipo"
#         if result_tipo == 'Tipo 0':
#             st.write('¡Resultado correspondiente a Tipo 1!')
#         elif result_tipo == 'Tipo 1':
#             st.write('¡Resultado correspondiente a Tipo 2!')
#         elif result_tipo == 'Tipo 2':
#             st.write('¡Resultado correspondiente a Tipo 3!')
#         elif result_tipo == 'Tipo 3':
#             st.write('¡Resultado correspondiente a Tipo 4!')
#         elif result_tipo == 'Tipo 4':
#             st.write('¡Resultado correspondiente a Tipo 5!')
#         else:
#             st.write('Tipo no reconocido.')
#     else:
#         st.write('No hay resultados para la combinación seleccionada.')




# # Cargar el archivo CSV
# df = pd.read_csv('prediciones/prediciones_07_12_2023.csv')

# # Widget para el filtro de cod_flight_IATA
# cod_flight_iata = st.selectbox('Write or select your Flight code:', df['cod_flight_IATA'].unique())

# # # Widget para el filtro de fecha
# selected_date = pd.to_datetime(st.date_input('Select the day of your flight:')).strftime('%Y-%m-%d')
# # selected_date = st.selectbox('Selecciona día:', df['day'].unique())
# # Filtrar el DataFrame

# # Convertir el formato de fecha
# # selected_date = pd.to_datetime(selected_date).strftime('%Y-%m-%d')

# filtered_df = df[(df['cod_flight_IATA'] == cod_flight_iata) & (df['day'] == selected_date)]
# #
# # Mostrar el resultado
# st.write('Resultado:')
# if not filtered_df.empty:
#     result_tipo = filtered_df['Tipo'].iloc[0]

#     # Mostrar mensaje según el valor de la columna "Tipo"
#     if result_tipo == 'Tipo 0':
#         st.write('¡Resultado correspondiente a Tipo 1!')
#     elif result_tipo == 'Tipo 1':
#         st.write('¡Resultado correspondiente a Tipo 2!')
#     elif result_tipo == 'Tipo 2':
#         st.write('¡Resultado correspondiente a Tipo 3!')
#     elif result_tipo == 'Tipo 3':
#         st.write('¡Resultado correspondiente a Tipo 4!')
#     elif result_tipo == 'Tipo 4':
#         st.write('¡Resultado correspondiente a Tipo 5!')
#     else:
#         st.write('Tipo no reconocido.')
# else:
#     st.write('No hay resultados para la combinación seleccionada.')
    # Mostrar el iframe en Streamlit
    # st.markdown(iframe_code2, unsafe_allow_html=True)
######################################################################################################################







