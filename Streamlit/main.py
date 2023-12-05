# para ejecutar, escribir por terminal : streamlit run main.py
# %%

from PIL import Image
import streamlit as st
import pandas as pd
import webbrowser
import base64
import io
# %%
######################################################################################################################
st.set_page_config(page_title='Mad Flights', page_icon="✈️", layout="wide")
# st.title('MAD Flights')
######################################################################################################################
st.title("Live Weather in MAD Barajas")
# Código HTML con iframe

html_code = '''
<iframe id="TTF_FiThuxWheYU9zQsUjauEEcmjA6nU1W1lrdktEZCoK1z53I35m" src="https://en.tutiempo.net/s-widget/tt_NXwxfDI1MjUyNXxufG58bnwyNTEwNHwzMHwxMXwxfDZ8NXwzfDI1fHN8c3xufEU4NkY2Rnw3MUI5RjB8fEJEQkRCRHxGRjdEMDN8NjZ8M3w2OHw2MHwxNDR8MjJ8NzR8MHw1MDV8ODl8Njh8Mzd8MTV8MTV8MzJ8NjF8Mjh8aWp8MXw%2C" frameborder="0" scrolling="no" width="100%" height="100%" allowtransparency="allowtransparency" style="overflow:hidden;pointer-events:auto;"></iframe>
'''

# Insertar HTML usando st.components.html
st.components.v1.html(html_code, height=89)

# img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1500835556837-99ac94a94552?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
background-size: 110%;
background-position: top left;
background-repeat: space;
background-attachment: local;
}}

"""
st.markdown(page_bg_img, unsafe_allow_html=True)

######################################################################################################################
# st.sidebar.header('MAD Flights Project')
# st.sidebar.subheader('Streamlit Workshop for IH')
# st.sidebar.image(Image.open('logo.png'))
# st.sidebar.image('logo.png')
######################################################################################################################

######################################################################################################################
if st.sidebar.button("📊 MAD Flights Dashboards"):
    # st.header("MAD Flights Dashboards")
    iframe_code = '''
    <iframe title="Report Section" width="800" height="1330" src="https://app.powerbi.com/view?r=eyJrIjoiYTc2Yzk0N2MtNGM0Yy00ZjJmLTg5MDktZjM3ZTY5ODdkYWUxIiwidCI6IjZhZmVhODVkLWMzMjMtNDI3MC1iNjlkLWE0ZmIzOTI3YzI1NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
    '''
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_code, unsafe_allow_html=True)
######################################################################################################################

if st.sidebar.button("🗺️ Foursquare Studio Flights map"):
    # st.header("Foursquare Studio Flights map")
    iframe_code2 = '''
    <iframe width="100%" height="500px" src="https://studio.foursquare.com/public/cb363a0b-a11a-436d-9ecf-c848b70702d4/embed" frameborder="0" allowfullscreen></iframe>
    '''
    # Mostrar el iframe en Streamlit
    st.markdown(iframe_code2, unsafe_allow_html=True)

######################################################################################################################







