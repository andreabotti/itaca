# IMPORT LIBRARIES
from fn__import_py_libs import *
from fn__load_data import *

mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'
#
#
#
#
#
# PAGE CONFIG
st.set_page_config(page_title="ITACA Streamlit App",   page_icon="🌡️", layout="wide")

st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 3rem; padding-right: 3rem;}</style>""",
    unsafe_allow_html=True)

# TOP CONTAINER
top_col1, top_col2 = st.columns([6,1])
with top_col1:
    st.markdown("# ITA.C.A")
    st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
    st.caption('Developed by AB.S.RD - https://absrd.xyz/')
#
#
#
#
#

# Variables to store the selections
data_sources = ["Local", "FTP", "GitHub"]
data_types = ["CSV", "Pickle", "Parquet"]
selected_source = None
selected_type = None

# Radio button for data source selection in the sidebar
data_source = st.sidebar.radio(
    "Select the data source:",
    ("Local", "FTP", "GitHub"), index=1,
)

# Radio button for data type selection in the sidebar
data_type = st.sidebar.radio(
    "Select the data type:",
    ("CSV", "Pickle", "Parquet"), index=1,
)

# Display the selections in the main area
st.sidebar.write(f"Loading data from: **{data_source}** and type: **{data_type}**")


LOCAL_PATH  = r'C:/_GitHub/andreabotti/itaca/'
FTP_PATH    = r'https://absrd.xyz/streamlit_apps/itaca/'
GITHUB_PATH = r'https://github.com/andreabotti/itaca/tree/main/'

if data_source == 'Local':
    MAIN_PATH = LOCAL_PATH
elif data_source == 'FTP':
    MAIN_PATH = FTP_PATH
elif data_source == 'GitHub':
    MAIN_PATH = GITHUB_PATH
#
if data_type == 'CSV':
    file_ext = '.csv'
elif data_type == 'Pickle':
    file_ext = '.pkl'
elif data_type == 'Parquet':
    file_ext = '.parquet'
#
CSV_PATH = MAIN_PATH + 'data_csv/'
GEOJSON_PATH = MAIN_PATH + 'data_geojson/'
TXT_PATH = MAIN_PATH + 'data_txt/'
SVG_PATH = MAIN_PATH + 'img_svg/'
#



# Load Data
@st.cache_resource()
def import_csv_data():
    df_locations_CTI, df_locations_COB, df_locations_CTI_capo, df_locations_COB_capo = LoadData__locations_CTI_COB(CSV_PATH,file_ext)
    df_CTI_DBT, df_COB_DBT, df__COB_capo__DBT = LoadData__DBT__CTI_COB__all(CSV_PATH,file_ext)
    
    return df_locations_CTI, df_locations_COB, df_locations_CTI_capo, df_locations_COB_capo, df_CTI_DBT, df_COB_DBT, df__COB_capo__DBT

df_locations_CTI, df_locations_COB, df_locations_CTI_capo, df_locations_COB_capo, df_CTI_DBT, df_COB_DBT, df__COB_capo__DBT = import_csv_data()

df_capoluoghi = df_locations_CTI_capo



# Load TopoJSON
@st.cache_resource
def import_geojson_data():
    geojson_italy_regions, geojson_italy_provinces = LoadData_regions_provinces(GEOJSON_PATH)

    return geojson_italy_regions, geojson_italy_provinces

geojson_italy_regions, geojson_italy_provinces = import_geojson_data()



# def LoadData__locations_CTI_COB():
#     try:
#         if file_ext == '.pkl':  # Handling for Pickle files
#             # Load Pickle file from URL
#             response_CTI = requests.get(CSV_PATH + 'CTI__list__ITA_WeatherStations__All' + file_ext)
#             response_CTI.raise_for_status()
#             df_CTI = pd.read_pickle(io.BytesIO(response_CTI.content))

#             response_COB = requests.get(CSV_PATH + 'COB__list__ITA_WeatherStations_All' + file_ext)
#             response_COB.raise_for_status()
#             df_COB = pd.read_pickle(io.BytesIO(response_COB.content))

#             response_CTI_capo = requests.get(CSV_PATH + 'CTI__list__ITA_WeatherStations_Capitals' + file_ext)
#             response_CTI_capo.raise_for_status()
#             df_CTI_capo = pd.read_pickle(io.BytesIO(response_CTI_capo.content))

#             response_COB_capo = requests.get(CSV_PATH + 'COB__list__ITA_WeatherStations__Capitals' + file_ext)
#             response_COB_capo.raise_for_status()
#             df_COB_capo = pd.read_pickle(io.BytesIO(response_COB_capo.content))

#         else:
#             # Assume it's a CSV or other format handled by pd.read_csv
#             df_CTI = pd.read_csv(CSV_PATH + 'CTI__list__ITA_WeatherStations__All' + file_ext, encoding='ISO-8859-1')
#             df_COB = pd.read_csv(CSV_PATH + 'COB__list__ITA_WeatherStations_All' + file_ext, encoding='ISO-8859-1')
#             df_CTI_capo = pd.read_csv(CSV_PATH + 'CTI__list__ITA_WeatherStations__Capitals' + file_ext, encoding='ISO-8859-1')
#             df_COB_capo = pd.read_csv(CSV_PATH + 'COB__list__ITA_WeatherStations_Capitals' + file_ext, encoding='ISO-8859-1')
    
#     except requests.exceptions.HTTPError as err:
#         raise SystemExit(f"HTTP error occurred: {err}")
#     except UnicodeDecodeError as e:
#         raise SystemExit(f"Encoding error in file: {e}")
#     return df_CTI, df_COB, df_CTI_capo, df_COB_capo



# # Load DBT for CTI and COB datasets
# @st.cache_resource
# def LoadData__DBT__CTI_COB__all():
#     try:
#         if file_ext == '.pkl':  # Handling for Pickle files
#             # Load Pickle file from URL
#             response_CTI = requests.get(CSV_PATH + 'CTI__DBT__ITA_WeatherStations__All' + file_ext)
#             response_CTI.raise_for_status()
#             df_CTI = pd.read_pickle(io.BytesIO(response_CTI.content))

#             response_COB = requests.get(CSV_PATH + 'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__All' + file_ext)
#             response_COB.raise_for_status()
#             df_COB = pd.read_pickle(io.BytesIO(response_COB.content))

#             response_COB_capo = requests.get(CSV_PATH + 'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__Capitals' + file_ext)
#             response_COB_capo.raise_for_status()
#             df_COB_capo = pd.read_pickle(io.BytesIO(response_COB_capo.content))

#         else:
#             # Assume it's a CSV or other format handled by pd.read_csv
#             df_CTI = pd.read_csv(CSV_PATH +     'CTI__DBT__ITA_WeatherStations__All'                    + file_ext, encoding='ISO-8859-1')
#             df_COB = pd.read_csv(CSV_PATH +     'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__All'     + file_ext, encoding='ISO-8859-1')
#             df_COB_capo = pd.read_csv(CSV_PATH +'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__Capitals'+ file_ext, encoding='ISO-8859-1')

#     except requests.exceptions.HTTPError as err:
#         raise SystemExit(f"HTTP error occurred: {err}")
#     except UnicodeDecodeError as e:
#         raise SystemExit(f"Encoding error in file: {e}")

#     return df_CTI, df_COB, df_COB_capo





# Load TopoJSON
@st.cache_resource
def LoadData_regions_provinces():
    json_file = json.loads(requests.get(GEOJSON_PATH + 'limits_IT_regions.geojson').text)
    geojson_italy_regions = json_file

    json_file = json.loads(requests.get(GEOJSON_PATH + 'limits_IT_provinces.geojson').text)
    geojson_italy_provinces = json_file
    return geojson_italy_regions, geojson_italy_provinces
geojson_italy_regions, geojson_italy_provinces = LoadData_regions_provinces()
#
#
#
#
#
url__cti__dict_regions      = MAIN_PATH + 'CTI__dict__Regions.json'
# DICT REGIONS
cti__dict_regions = {
    "AB":"Abruzzo",         "BC":"Basilicata",          "CM":"Campania",
    "CL":"Calabria",        "ER":"Emilia Romagna",      "FV":"Friuli Venezia Giulia",
    "LZ":"Lazio",           "LG":"Liguria",             "LM":"Lombardia",
    "MH":"Marche",          "ML":"Molise",              "PM":"Piemonte",
    "PU":"Puglia",          "SD":"Sardegna",            "SC":"Sicilia",
    "TC":"Toscana",         "TT":"Trentino Alto Adige", "UM":"Umbria",
    "VD":"Valle dAosta",    "VN":"Veneto"
    }
dict_regions = cti__dict_regions
# dict_regions = pd.read_json( url__cti__dict_regions, typ='series')
# dict_regions = dict(dict_regions)
regions_list = list(dict_regions.values())

#
#
#
#
#
# # DATAFRAME LOCATIONS
# df_locations_CTI['region'] = df_locations_CTI['reg'].apply(lambda x: dict_regions.get(x))
# sel_cols = ['reg','region','province','city','lat','lon','alt']
# df_locations_CTI = df_locations_CTI[sel_cols]

# df_locations_COB['wmo_code'] = df_locations_COB['wmo_code'].astype(str) 
# df_locations_COB = df_locations_COB[ ['reg', 'location', 'filename', 'wmo_code', 'lat', 'lon','alt'] ]
# df_locations_COB_capo['wmo_code'] = df_locations_COB_capo['wmo_code'].astype(str) 
# df_locations_COB_capo = df_locations_COB_capo[ ['reg', 'location', 'filename', 'wmo_code', 'lat', 'lon','alt'] ]


# # DATAFRAME PROVINCES
# df_province = df_locations_CTI.groupby('province').size()
# df_province.rename('station_count', inplace=True)

# # DATAFRAME REGION_SHORT
# df_reg_short   = df_locations_CTI.groupby('reg').size()
# df_reg_short.rename('station_count', inplace=True)
# df_reg_short = df_reg_short.reset_index()
# df_reg_short['region'] = df_reg_short['reg'].apply(lambda x: dict_regions.get(x))
# df_reg_short.set_index('reg',inplace=True)
# df_reg_short = df_reg_short[['region', 'station_count']]
#
#
#
#
#


def drop_unnamed_columns(df):
    """ Drop columns where the name contains 'Unnamed' """
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    return df


# SAVE ST SESSION STATES
st.session_state['df_locations_CTI'] = df_locations_CTI
st.session_state['df_locations_COB'] = df_locations_COB
st.session_state['df_locations_COB_capo'] = df_locations_COB_capo
st.session_state['df_capoluoghi'] = df_capoluoghi


st.session_state['df_CTI_DBT'] = df_CTI_DBT
st.session_state['df_COB_DBT'] = df_COB_DBT
st.session_state['df__COB_capo__DBT'] = df__COB_capo__DBT

st.session_state['geojson_italy_regions'] = geojson_italy_regions
st.session_state['geojson_italy_provinces'] = geojson_italy_provinces

# st.session_state['df_reg'] = df_reg_short
st.session_state['dict_regions'] = dict_regions
st.session_state['regions_list'] = regions_list

st.session_state['MAIN_PATH'] = MAIN_PATH


#
#
#
#
#
#
#
#
#
#
if data_source == 'Local':
    with open( TXT_PATH + 'CTI_TRY_description01.txt',encoding='utf8') as f:
        cti_try_descr01 = f.readlines()
    with open(TXT_PATH + '/CTI_TRY_description02.txt',encoding='utf8') as f:
        cti_try_descr02 = f.readlines()
    with open(TXT_PATH + 'weather_morphing_description.txt',encoding='utf8') as f:
        weather_morphing_descr01 = f.readlines()

elif data_source == 'FTP' or data_source == 'GitHub':
    MAIN_PATH = GITHUB_PATH
    try:
        response = requests.get(TXT_PATH + 'CTI_TRY_description01.txt')
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        cti_try_descr01 = response.text.splitlines()

        response = requests.get(TXT_PATH + 'CTI_TRY_description02.txt')
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        cti_try_descr02 = response.text.splitlines()

        response = requests.get(TXT_PATH + 'weather_morphing_description.txt')
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        weather_morphing_descr01 = response.text.splitlines()

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

#
#
#
#
#
col1, spacing, col2 = st.columns([9,1,12])

with col1:
    # st.markdown('#### Scopo di questa app')
    st.write('Lo scopo di questa app ITA.C.C.A è quello di colmare alcune **lacune** esistenti rispetto alla disponibilità, all\'interno di standards tecnici e normativi italiani \
              di **dati climatici** capaci di descrivere accuratamente gli **impatti presenti e futuri del cambiamento climatico** nelle varie zone del territorio Italiano.')
    st.write('Questo risulta di importanza capitale per informare la progettazione edile ed impiantistica degli edifici di varie destinazioni d\'uso, \
             e per valutarne il comportamento termico **con particolare riguardo al periodo estivo**.')

    st.divider()
    st.markdown('##### Come utilizzare l\'app:')
    st.markdown('1 Scegliere la regione italiana per visualizzare stazioni meteo disponibili rispetto alle banche dati CTI (*Comitato Termotecnico Italiano*) e COB (*climate.onebuilding.org*)')
    st.code('📂 Scelta Regione')
    st.markdown('2 Scegliere, esplorare e confrontare i dati di temperatura secondo i files normativi italiani (CTI) e quelli piu\' recenti, forniti dal dataset COB. \
                Laddove i dati climatici dei due *datasets* per le stesse località indicano discrepanze significative, la progettazione impiantistica e la modellazione energetica \
                elaborate secondo i dati CTI rischiano di non essere adeguate')
    st.code('📂 Confronto Dati Province')




with col2:
    tab1, tab2, tab3 = st.tabs([":file_cabinet: Il Passato Recente", ":world_map: Il Presente", ":thermometer: Il Futuro"])

with tab1:
    st.markdown('##### Il passato: Anni Tipo Climatici del Comitato Termotecnico Italiano \(CTI\)')
    st.write('Gli anni tipo climatici - *Test Reference Years (TRY)* o *Typical Meteorological Year (TMY)* - vengono forniti dal \
             **Comitato Termotecnico Italiano (CTI)** per 110 località di riferimento distribuite sul territorio nazionale e rappresentano i dati standard \
             ai fini del soddisfacimento della normativa energetica \
             L\'anno tipo climatico consiste in 12 mesi caratteristici scelti da un database di dati meteorologici di un periodo preferibilmente ampio almeno 10 anni.')

    # st.divider()
    with st.expander('*Per avere più dettagli sugli anni tipo climatici - banca dati CTI*'):
        st.write('\n'.join(cti_try_descr01))
        st.write('\n'.join(cti_try_descr02))
        st.caption('Fonte: https://try.cti2000.it/')

    st.divider()
    st.markdown('##### Ulteriori informazioni')
    st.markdown("*What is weather data, and how is it collected?*[https://docs.ladybug.tools/ladybug-tools-academy/v/climate-analysis/]",
                unsafe_allow_html=True)



with tab2:
    st.markdown('##### Il presente: anni tipici recenti dalla banca dati di *climate.onebuilding.org* \(COB\)')
    st.write('The weather data - *Typical Meteorological Years TMYx* - provided at https://climate.onebuilding.org/ are derived from a number of public sources, and produced by translating the source data into the EPW format. \
        TMYx files are typical meterological files derived from ISD \(US NOAA\'s Integrated Surface Database\) with hourly data through 2021 using the TMY/ISO 15927-4:2005 methodologies. \
        ISD individual year files are created using the general principles from the IWEC (International Weather for Energy Calculations) Typical Meteorological Years that was published in 2001. \
        The ERA5 data, courtesy of Oikolab, provides a comprehensive, worldwide gridded solar radiation data set based on satellite data.')
    st.write('For each location, the TMYx file structure \'EGY_AN_Aswan.Intl.AP.624140_TMYx.2007-2021\' indicate data collected for the most recent 15 years \(2007-2021\). Not all locations have recent data.')




with tab3:
    st.markdown('#### Il futuro: proiezioni climatiche e *morphing*')
    st.markdown('#### Il *morphing* dei dati climatici')
    with st.expander('*Dettagli sul morphing di dati climatici per ottenere l\'anno climatico tipo per climi futuri*'):
        st.markdown('\n'.join(weather_morphing_descr01), unsafe_allow_html=True)

    st.markdown('#### Lo strumento *Future Weather Generator*')
# st.dataframe( df_COB_DBT.reindex(sorted(df_COB_DBT.columns), axis=1) )