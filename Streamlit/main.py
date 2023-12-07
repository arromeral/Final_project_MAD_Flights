# para ejecutar, escribir por terminal : streamlit run main.py
# %%

from PIL import Image
import streamlit as st
import pandas as pd
import webbrowser
import base64
from datetime import datetime, timedelta
from pathlib import Path
import io
# %%
######################################################################################################################


st.set_page_config(page_title='Mad Flights', page_icon="✈️", layout="wide")
# st.title('MAD Flights')
######################################################################################################################
# Construct the path to the logo file using pathlib

logo_path = Path(__file__).resolve().parent / 'logo.png'

# Display the logo in the sidebar header
try:
    st.sidebar.image(Image.open('logo.png'))
except:
    st.sidebar.image(str(logo_path), use_column_width=True)

# st.title("Live Weather in MAD Barajas")


# Código HTML con iframe
# html_code = '''
# <center>
#     <div id="TT_FfNHCydBw4K9peKK7auka4mDg5uKaMloGoGom" style="width: 539px; height: 99px;">Weather - Tutiempo.net</div>
#     <script type="text/javascript" src="https://en.tutiempo.net/s-widget/l_FfNHCydBw4K9peKK7auka4mDg5uKaMloGoGom"></script>
# </center>
# '''

# # Insertar HTML usando st.components.html
# st.components.v1.html(html_code, height=89)



######################################################################################################################

######################################################################################################################
# Cargar el archivo CSV
try:
    df = pd.read_csv('prediciones/prediciones_07_12_2023.csv')
except FileNotFoundError:
    df = pd.read_csv(Path(__file__).resolve().parent / 'prediciones/prediciones_07_12_2023.csv')
print(df.info())
# Variable de estado para controlar la pestaña activa
active_tab = st.sidebar.radio("Navigation", ["🛫 **What is MAD FLIGHTS Stats?**" , "📊 **MAD Flights Dashboards**","🎯 **Flight Delay Predictions**",
"🗺️ **Foursquare Studio Flights map**","🔄 **About the Project**"])
# Define the labels with HTML styling for white text color

# Contenido de la pestaña "Flight Predictions"

if active_tab == "🛫 **What is MAD FLIGHTS Stats?**":
    # st.header("🛫 What is Mad Flights Stats?")
    st.image('banner.png', use_column_width = True)
    st.title('🛫 Welcome to MAD FLIGHTS')
    st.write("Embark on a journey through the skies with our interactive application, the Madrid Barajas Airport Explorer. Dive into a million flights' worth of data, spanning from 2017 to today, as we unravel the stories behind departures from one of Europe's busiest airports.")
    st.text("")
    col1, col2 = st.columns(2)
    with col1:

        st.header('*Discover the Heart of European Aviation* ')
        st.write('Madrid Barajas Airport, a bustling hub in the heart of Spain, stands as a testament to the marvels of civil aviation. With its state-of-the-art facilities and strategic location, this airport plays a pivotal role in connecting the world. Explore the significance of Barajas in the realm of civil aviation and get ready to navigate the skies.')
        st.image('src/images/torre.jpg', use_column_width=True)
        st.header('*Unveiling the Flight Patterns*')
        st.write("Our application is your window into the dynamic world of flights. Through an intricate ETL process, we've seamlessly integrated data on a million flights with meteorological reports (METAR) from Barajas Airport. Each flight is intricately linked to the meteorological conditions preceding its departure, offering you a comprehensive understanding of the interplay between flights and weather.")
        
    with col2:
        # st.title('Columna 1')
        # st.header('Columna 1.2')
        # st.write('holahola')
        st.image('src/images/terminal.jpg', use_column_width=True)
        st.header('*Interactive Dashboards* ')
        st.write('The first stop on your exploration journey is our interactive dashboard. Delve into statistics and insights on delays, exploring trends based on dates, airlines, destinations, and more. Uncover the nuanced impact of external factors, from the ripple effects of the COVID era to the seasonal ebb and flow of flights.')
        st.header('*Predicting the Skies* ')       
        st.write("Looking ahead, our second page employs cutting-edge Machine Learning models to predict delays for the next 24 hours. Enter the flight details, and witness the power of data-driven foresight in understanding potential disruptions.")
        st.header('*Flight Flow in Foursquare Studio* ')
        st.write("On the third page, experience flight patterns like never before. Navigate a 24-hour flight map, created with Foursquare Studio, showcasing the ebb and flow of aircraft. Visualize the skies coming alive as planes take off and soar, providing a captivating snapshot of aviation in motion.")
    st.text("")
    st.write("Step into a captivating experience with Madrid Barajas Airport Explorer, where data seamlessly intertwines with stories, and each flight reveals a distinctive narrative. Beyond charts and predictions, our platform immerses you in the vibrant tales of aviation. Navigate the skies with us, where every departure becomes a chapter, and each piece of information offers a glimpse into the dynamic world above. Join us in Connecting Data and Unveiling Stories – your gateway to narratives that soar high in the boundless expanse of aviation.")
elif active_tab == "🎯 **Flight Delay Predictions**":
    # html_code = '''
    # <center>
    # <div id="TT_FVtHiCYxwYUaz87UKaz1anmjA5nUBW1" style="width: 539px; height: 99px;">Weather - Tutiempo.net</div>
    # <script type="text/javascript" src="https://en.tutiempo.net/s-widget/l_FVtHiCYxwYUaz87UKaz1anmjA5nUBW1"></script>
    # </center>
    # '''
    # st.components.v1.html(html_code, height=89)
    
    html_code = '''
    <div style="width: 100%; display: flex; justify-content: center; align-items: center;">
        <div id="TT_FVtHiCYxwYUaz87UKaz1anmjA5nUBW1" style="width: 300px; height: 95px;"></div>
    </div>
    <script type="text/javascript" src="https://en.tutiempo.net/s-widget/l_FVtHiCYxwYUaz87UKaz1anmjA5nUBW1"></script>
    '''
    st.components.v1.html(html_code, height=110)
    st.title("🎯 Flight Delay Predictions")

    # Insertar HTML usando st.components.html
    
    
    # Widget para el filtro de cod_flight_IATA y fecha en paralelo
    col1, col2 = st.columns(2)

    # Widget para el filtro de cod_flight_IATA
    cod_flight_iata = col1.selectbox('Write or select your Flight code:', df['cod_flight_IATA'].unique())

    # Widget para el filtro de fecha
    selected_date = pd.to_datetime(col2.date_input('Select the day of your flight:')).strftime('%Y-%m-%d')

    # Filtrar el DataFrame
    filtered_df = df[(df['cod_flight_IATA'] == cod_flight_iata) & (df['day'] == selected_date)]

    st.write('Our prediction:')
    if not filtered_df.empty:
        result_tipo = filtered_df['Tipo'].iloc[0]

        # Mostrar mensaje según el valor de la columna "Tipo"
        if result_tipo == 'Tipo 0':
            st.header('*Flight On-time* ')
            st.write("Great news! Our predictive model indicates that your flight is expected to arrive on time. However, please note that predictions may not account for unforeseen circumstances. We recommend checking for updates closer to your departure time.")
            
        elif result_tipo == 'Tipo 1':
            st.header('*Slight Delay Predicted* ')
            st.write("Our model suggests a minor potential delay of less than 30 minutes for your flight. While this delay is not expected to be significant, we advise you to stay informed by checking for real-time updates from the airline. As a general precaution, consider arriving at the airport well in advance.")
            
        elif result_tipo == 'Tipo 2':
            st.header('*Moderate Delay Predicted* ')
            st.write("Please be aware that our model predicts a delay of approximately 30 minutes for your flight. While this delay is within a manageable range, we recommend planning accordingly. Stay updated with the latest information from the airline, and ensure you arrive at the airport with sufficient time before departure.")
           
        elif result_tipo == 'Tipo 3':
            st.header('*Significant Delay Predicted* ')
            st.write("Our model anticipates a significant delay, possibly exceeding one hour, for your flight. We advise you to adjust your plans accordingly and monitor real-time updates from the airline. For such delays, consider reaching out to the airline for additional guidance and ensure you allow ample time at the airport.")
            
        elif result_tipo == 'Tipo 4':
            st.header('*Flight Officially Delayed* ')
            st.write("We regret to inform you that your flight is officially delayed. For the most accurate and up-to-date information, we recommend checking directly with the airline. Please plan accordingly, and we suggest arriving at the airport well in advance to accommodate any further changes in the schedule.")
           
        elif result_tipo == 'Tipo 5':
            st.header('*Flight Officially Cancelled* ')
            st.write("We regret to inform you that your flight has been officially canceled. For detailed information on rebooking or refunds, please contact the airline directly. We recommend checking alternative travel options and reaching out to the airline's customer service for further assistance.")
            

        else:
            st.write('Tipo no reconocido.')
    else:
        st.write('No hay resultados para la combinación seleccionada.')
    st.write("Please note that these predictions are based on historical data and machine learning algorithms, and there is always the possibility of unforeseen events affecting flight schedules. It is advisable to check for real-time updates from the airline and arrive at the airport well in advance. Our model's accuracy is not guaranteed, and the airline's official information should be consulted for the most accurate details regarding your flight.")
elif active_tab == "📊 **MAD Flights Dashboards**":
    st.title("📊 MAD Flights Dashboards")
    iframe_code = '''
    <iframe title="Report Section" width="800" height="1330" src="https://app.powerbi.com/view?r=eyJrIjoiYTc2Yzk0N2MtNGM0Yy00ZjJmLTg5MDktZjM3ZTY5ODdkYWUxIiwidCI6IjZhZmVhODVkLWMzMjMtNDI3MC1iNjlkLWE0ZmIzOTI3YzI1NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
    '''
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_code, unsafe_allow_html=True)

# Contenido de la pestaña "Flight Map"
elif active_tab == "🗺️ **Foursquare Studio Flights map**":
    st.title("🗺️ Foursquare Studio Flights map")
    iframe_code2 = '''
    <iframe width="100%" height="500px" src="https://studio.foursquare.com/public/cb363a0b-a11a-436d-9ecf-c848b70702d4/embed" frameborder="0" allowfullscreen></iframe>
    '''
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_code2, unsafe_allow_html=True)
elif active_tab == "🔄 **About the Project**":
    st.title("🔄 Project Workflow")
    st.image('src/images/flujos.png', use_column_width=True)
    
# ######################################################################################################################

# ######################################################################################################################

######################################################################################################################







