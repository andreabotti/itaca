# IMPORT LIBRARIES
from fn__import_py_libs import *



# Load Data
def LoadData__locations_CTI_COB(CSV_PATH,file_ext):
    try:
        if file_ext == '.pkl':  # Handling for Pickle files
            # Load Pickle file from URL
            response_CTI = requests.get(CSV_PATH + 'CTI__list__ITA_WeatherStations__All' + file_ext)
            response_CTI.raise_for_status()
            df_CTI = pd.read_pickle(io.BytesIO(response_CTI.content))

            response_COB = requests.get(CSV_PATH + 'COB__list__ITA_WeatherStations_All' + file_ext)
            response_COB.raise_for_status()
            df_COB = pd.read_pickle(io.BytesIO(response_COB.content))

            response_CTI_capo = requests.get(CSV_PATH + 'CTI__list__ITA_WeatherStations_Capitals' + file_ext)
            response_CTI_capo.raise_for_status()
            df_CTI_capo = pd.read_pickle(io.BytesIO(response_CTI_capo.content))

            response_COB_capo = requests.get(CSV_PATH + 'COB__list__ITA_WeatherStations__Capitals' + file_ext)
            response_COB_capo.raise_for_status()
            df_COB_capo = pd.read_pickle(io.BytesIO(response_COB_capo.content))

        else:
            # Assume it's a CSV or other format handled by pd.read_csv
            df_CTI = pd.read_csv(
                CSV_PATH + 'CTI__list__ITA_WeatherStations__All' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df_COB = pd.read_csv(
                CSV_PATH + 'COB__list__ITA_WeatherStations_All' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df_CTI_capo = pd.read_csv(
                CSV_PATH + 'CTI__list__ITA_WeatherStations__Capitals' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df_COB_capo = pd.read_csv(
                CSV_PATH + 'COB__list__ITA_WeatherStations_Capitals' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )

    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred: {err}")
    except UnicodeDecodeError as e:
        raise SystemExit(f"Encoding error in file: {e}")

    return df_CTI, df_COB, df_CTI_capo, df_COB_capo



# Load DBT for CTI and COB datasets
def LoadData__DBT__CTI_COB__all(CSV_PATH,file_ext):
    try:
        if file_ext == '.pkl':  # Handling for Pickle files
            # Load Pickle file from URL
            response_CTI = requests.get(CSV_PATH + 'CTI__DBT__ITA_WeatherStations__All' + file_ext)
            response_CTI.raise_for_status()
            df_CTI = pd.read_pickle(io.BytesIO(response_CTI.content))

            response_COB = requests.get(CSV_PATH + 'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__All' + file_ext)
            response_COB.raise_for_status()
            df_COB = pd.read_pickle(io.BytesIO(response_COB.content))

            response_COB_capo = requests.get(CSV_PATH + 'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__Capitals' + file_ext)
            response_COB_capo.raise_for_status()
            df_COB_capo = pd.read_pickle(io.BytesIO(response_COB_capo.content))

        else:
            # Assume it's a CSV or other format handled by pd.read_csv
            df_CTI = pd.read_csv(
                CSV_PATH +     'CTI__DBT__ITA_WeatherStations__All'                    + file_ext,
                parse_dates=['datetime'], index_col='datetime',
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df_COB = pd.read_csv(
                CSV_PATH +     'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__All'     + file_ext,
                parse_dates=['datetime'], index_col='datetime',
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df_COB_capo = pd.read_csv(
                CSV_PATH +'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__Capitals'+ file_ext,
                parse_dates=['datetime'], index_col='datetime',
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred: {err}")
    except UnicodeDecodeError as e:
        raise SystemExit(f"Encoding error in file: {e}")

    return df_CTI, df_COB, df_COB_capo



# Load TopoJSON
def LoadData_regions_provinces(GEOJSON_PATH):
    json_file = json.loads(requests.get(GEOJSON_PATH + 'limits_IT_regions.geojson').text)
    geojson_italy_regions = json_file

    json_file = json.loads(requests.get(GEOJSON_PATH + 'limits_IT_provinces.geojson').text)
    geojson_italy_provinces = json_file
    return geojson_italy_regions, geojson_italy_provinces




def load_file_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error if the download failed
    return response.text

# # Load Text Descriptions
# def LoadData_text_descriptions(TXT_PATH, file_name_ext):
    
#     if TXT_PATH.startswith('http://') or TXT_PATH.startswith('https://'):
#         url_text_file = TXT_PATH + file_name_ext
#         parsed_text = load_file_from_url(url=url_text_file)

#     else:
#         with open(url_text_file,  encoding='utf8') as f:
#             parsed_text = f.readlines()

#     return parsed_text



def fetch_daily_data(latitude, longitude, start_date, end_date):
    # Create a Point for the location
    location = Point(latitude, longitude)

    # Fetch daily data
    data = Daily(location, start_date, end_date)
    daily_data = data.fetch()

    return daily_data
#
def fetch_hourly_data(latitude, longitude, start_date, end_date):
    # Create a Point for the location
    location = Point(latitude, longitude)

    # Fetch hourly data
    data = Hourly(location, start_date, end_date)
    hourly_data = data.fetch()

    return hourly_data
