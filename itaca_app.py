# IMPORT LIBRARIES
from fn__import_py_libs import *
from fn__load_data import *

mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'
#
#
#
#
# PAGE CONFIG
st.set_page_config(page_title="ITACA Streamlit App",   page_icon=':mostly_sunny:', layout="wide")
st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 2.5rem; padding-right: 2.5rem;}</style>""",
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


# Define custom CSS
custom_css = """
    <style>
        /* Adjust the padding of the entire sidebar */
        .css-1e5imcs {
            padding-top: 0rem;  /* Adjust the top padding */
            padding-right: 1rem; /* Adjust the right padding */
            padding-left: 1rem;  /* Adjust the left padding */
            padding-bottom: 1rem;/* Adjust the bottom padding */
        }
        /* Adjust the margin around each widget in the sidebar */
        .stSidebar .css-xq1lnh-EmotionIconBase {
            margin-bottom: 0.5rem; /* Adjust the space between widgets */
        }
    </style>
"""
# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Your Streamlit app code goes here
st.sidebar.title("DATA MENU")

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
# st.sidebar.write(f"Loading data from: **{data_source}** and type: **{data_type}**")


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
    FileExt = '.csv'
elif data_type == 'Pickle':
    FileExt = '.pkl'
elif data_type == 'Parquet':
    FileExt = '.parquet'
#
CSV_PATH = MAIN_PATH + 'data_csv/'
GEOJSON_PATH = MAIN_PATH + 'data_geojson/'
TXT_PATH = MAIN_PATH + 'data_txt/'
SVG_PATH = MAIN_PATH + 'img_svg/'
#


# Load Data
@st.cache_resource()
def import_csv_data():
    df_locations_CTI, df_locations_COB, df_locations_CTI_capo, df_locations_COB_capo = LoadData__locations_CTI_COB(CSV_PATH,FileExt)
    df_CTI_DBT, df_COB_DBT, df__COB_capo__DBT = LoadData__DBT__CTI_COB__all(CSV_PATH,FileExt)
    
    return df_locations_CTI, df_locations_COB, df_locations_CTI_capo, df_locations_COB_capo, df_CTI_DBT, df_COB_DBT, df__COB_capo__DBT

df_locations_CTI, df_locations_COB, df_locations_CTI_capo, df_locations_COB_capo, df_CTI_DBT, df_COB_DBT, df__COB_capo__DBT = import_csv_data()


def drop_unnamed_columns(df):
    """ Drop columns where the name contains 'Unnamed' """
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    return df

df_locations_CTI = drop_unnamed_columns(df_locations_CTI)
df_locations_CTI_capo = drop_unnamed_columns(df_locations_CTI_capo)
df_locations_COB = drop_unnamed_columns(df_locations_COB)
df_locations_COB_capo = drop_unnamed_columns(df_locations_COB_capo)
df_capoluoghi = df_locations_CTI_capo



# Load TopoJSON
@st.cache_resource
def import_geojson_data():
    geojson_italy_regions, geojson_italy_provinces = LoadData_regions_provinces(GEOJSON_PATH)

    return geojson_italy_regions, geojson_italy_provinces

geojson_italy_regions, geojson_italy_provinces = import_geojson_data()


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
regions_list = list(dict_regions.values())



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
st.session_state['CSV_PATH'] = CSV_PATH
st.session_state['GEOJSON_PATH'] = GEOJSON_PATH

st.session_state['FileExt'] = FileExt