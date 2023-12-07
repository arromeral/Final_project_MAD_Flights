
# MAD FLIGHTS Final Project
![banner](https://github.com/arromeral/Final_project_MAD_Flights/assets/138980560/e4d28428-379e-4a05-af17-8c0843177be6)
## Descripition
This project consists of several parts:
- A complete ETL process (Extract-Transfor-Load) for the generation of a database of all flight departures from the Madrid-Barajas Adolfo Suárez Airport over a period of six years (November 2017 - October 2023). Additionally, METAR weather reports for the same period had bene extracted and related to the flights.
- Data visualization created using Power BI, focusing on analyzing flights departures from Adolfo Suárez Madrid-Barajas Airport over the last 7 years. The visualization consists of two interactive dashboards providing detailed insights into various aspects of flights; correlating flight data and METAR weather reports.
- Implementing machine learning for predicting flight delays. This includes training and deploying regression and classification models. Additionally, pipelines are generated to automate the prediction process.
- Creation of a comprehensive, user-friendly Streamlit application that consolidates all the previously mentioned components.

## Contents

The contents of the project are as follows:

- [**Jupyter_Notebooks**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/Jupyter_Notebooks): Folder with the Jupyter Notebooks used during the project, classified among extraction, cleaning, processing, database generation, and machine learning
- [**data**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/data): Folder that contains the main data used in the project, both extracted and transformed for later loading or model training.
   - [**ML**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/data/ML): Folder with data used to train the ML models.      
   - [**flights**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/data/flights): Folder with data referring to flight records obtained from flightera.
   - [**metar**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/data/metars): Folder with data referring to the METAR reports obtained from tutiempo.net.
- [**sql_databases**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/sql_databases): Folder with the files with the EER Diagram of the relational Database created and the file to import the Database created.
- [**src**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/src): Folder with the files of functions created and the predictions pipeline.
- [**visualization**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/visualization): Folder with the Power BI Dashboards.
- [**images**](https://github.com/arromeral/Final_project_MAD_Flights/tree//main/images): Folder with the images used in this document.
- [**Streamlit**](https://github.com/arromeral/Final_project_MAD_Flights/tree/main/Streamlit): Folder with the streamlit app configuration and objects.

## About the project
### Introduction
Embark on a fascinating journey through the skies with MAD FLIGHTS, our interactive application designed to explore the dynamic world of flights departing from Madrid Barajas Airport. Delve into a comprehensive dataset encompassing a million flights from 2017 to the present day, uncovering the unique narratives behind each departure.

### Discover the Heart of European Aviation
Madrid Barajas Airport stands as a bustling hub in the heart of Spain, a testament to the marvels of civil aviation. With its state-of-the-art facilities and strategic location, this airport plays a pivotal role in connecting the world. Explore the significance of Barajas in the realm of civil aviation and get ready to navigate the skies.

### Unveiling the Flight Patterns
MAD FLIGHTS provides a window into the dynamic world of flights through an intricate ETL process. We seamlessly integrate data on a million flights with meteorological reports (METAR) from Barajas Airport. Each flight is intricately linked to the meteorological conditions preceding its departure, offering you a comprehensive understanding of the interplay between flights and weather.

### Interactive Dashboards
Your first stop on this exploration journey is our interactive dashboard. Delve into statistics and insights on delays, exploring trends based on dates, airlines, destinations, and more. Uncover the nuanced impact of external factors, from the ripple effects of the COVID era to the seasonal ebb and flow of flights.

### Predicting the Skies
Looking ahead, our second page employs cutting-edge Machine Learning models to predict delays for the next 24 hours. Enter the flight details and witness the power of data-driven foresight in understanding potential disruptions.

### Flight Flow in Foursquare Studio
On the third page, experience flight patterns like never before. Navigate a 24-hour flight map, created with Foursquare Studio, showcasing the ebb and flow of aircraft. Visualize the skies coming alive as planes take off and soar, providing a captivating snapshot of aviation in motion.

Step into a captivating experience with MAD FLIGHTS, where data seamlessly intertwines with stories, and each flight reveals a distinctive narrative. Beyond charts and predictions, our platform immerses you in the vibrant tales of aviation. Navigate the skies with us, where every departure becomes a chapter, and each piece of information offers a glimpse into the dynamic world above. Join us in Connecting Data and Unveiling Stories – your gateway to narratives that soar high in the boundless expanse of aviation.


https://github.com/arromeral/Final_project_MAD_Flights/assets/138980560/93a4b9db-304b-4b92-8cfa-6acf15dcc375


## Technical workflow
![flujos](https://github.com/arromeral/Final_project_MAD_Flights/assets/138980560/a1d39ca6-2cf5-4fc3-b3c7-f4fe1de59066)

## Greetings

