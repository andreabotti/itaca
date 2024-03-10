# IMPORT LIBRARIES
from fn__import_py_libs import *
from fn__load_data import *


def get_coordinates(city):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city + ", Italy")
        return location.latitude, location.longitude
    except GeocoderTimedOut:
        return get_coordinates(city)

def add_lat_lon(df):
    df['lat'] = None
    df['lon'] = None

    for index, row in df.iterrows():
        city = row['location']
        try:
            lat, lon = get_coordinates(city)
            df.at[index, 'lat'] = lat
            df.at[index, 'lon'] = lon
        except AttributeError:
            # In case the city is not found or there's an error in getting coordinates
            print(f"Coordinates not found for {city}")

    return df



#####

LOCAL_PATH  = r'C:/_GitHub/andreabotti/itaca/'
FTP_PATH    = r'https://absrd.xyz/streamlit_apps/itaca/'
GITHUB_PATH = r'https://github.com/andreabotti/itaca/tree/main/'
MAIN_PATH = LOCAL_PATH
FileExt = '.csv'
CSV_PATH = MAIN_PATH + 'data_csv/'
GEOJSON_PATH = MAIN_PATH + 'data_geojson/'
TXT_PATH = MAIN_PATH + 'data_txt/'
SVG_PATH = MAIN_PATH + 'img_svg/'

# Load Data
@st.cache_resource()
def import_csv_data():
    df__list__CTI, df__list__COB, df__list__MSTAT, df__list__CTI_capo, df__list__COB_capo = LoadData__locations_CTI_COB_MSTAT(CSV_PATH,FileExt)
    df__DBT__CTI, df__DBT__COB, df__DBT__COB_capo = LoadData__DBT__CTI_COB__all(CSV_PATH,FileExt)
    
    return df__list__CTI, df__list__COB, df__list__MSTAT, df__list__CTI_capo, df__list__COB_capo, \
        df__DBT__CTI, df__DBT__COB, df__DBT__COB_capo

df__list__CTI, df__list__COB, df__list__MSTAT, df__list__CTI_capo, df__list__COB_capo, \
    df__DBT__CTI, df__DBT__COB, df__DBT__COB_capo = import_csv_data()

def drop_unnamed_columns(df):
    """ Drop columns where the name contains 'Unnamed' """
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    return df

df__list__CTI       = drop_unnamed_columns(df__list__CTI)
df__list__CTI_capo  = drop_unnamed_columns(df__list__CTI_capo)
df__list__COB       = drop_unnamed_columns(df__list__COB)
df__DBT__COB_capo   = drop_unnamed_columns(df__DBT__COB_capo)


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

print(df__list__CTI_capo)
# print(df__DBT__CTI)



# Assuming your DataFrame is named df_list_CTI
df__list__CTI = add_lat_lon(df__list__CTI)

df__list__CTI_capo = add_lat_lon(df__list__CTI_capo)


df__list__CTI.to_csv(CSV_PATH + 'CTI__list__ITA_WeatherStations__All.csv')
df__list__CTI_capo.to_csv(CSV_PATH + 'CTI__list__ITA_WeatherStations__Capitals.csv')
