# IMPORT LIBRARIES
from fn__import_py_libs import *





# Load Data
def LoadData__locations_CTI_COB_MSTAT(CSV_PATH,file_ext):
    try:
        if file_ext == '.pkl':  # Handling for Pickle files
            # Load Pickle file from URL
            response_CTI = requests.get(CSV_PATH + 'CTI__list__ITA_WeatherStations__All' + file_ext)
            response_CTI.raise_for_status()
            df_CTI = pd.read_pickle(io.BytesIO(response_CTI.content))

            response_COB = requests.get(CSV_PATH + 'COB__list__ITA_WeatherStations__All' + file_ext)
            response_COB.raise_for_status()
            df_COB = pd.read_pickle(io.BytesIO(response_COB.content))

            response_MSTAT = requests.get(CSV_PATH + 'MSTAT__list__ITA_WeatherStations__All' + file_ext)
            response_MSTAT.raise_for_status()
            df_MSTAT = pd.read_pickle(io.BytesIO(response_MSTAT.content))

            response_ITA_capo = requests.get(CSV_PATH + 'ALL__list__ITA_Capitals' + file_ext)
            response_ITA_capo.raise_for_status()
            df__list__ITA_capo = pd.read_pickle(io.BytesIO(response_ITA_capo.content))

            response_COB_capo = requests.get(CSV_PATH + 'COB__list__ITA_WeatherStations__Capitals' + file_ext)
            response_COB_capo.raise_for_status()
            df_COB_capo = pd.read_pickle(io.BytesIO(response_COB_capo.content))

        else:
            # Assume it's a CSV or other format handled by pd.read_csv
            df__list__CTI = pd.read_csv(
                CSV_PATH + 'CTI__list__ITA_WeatherStations__All' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df__list__ITA_capo = pd.read_csv(
                CSV_PATH + 'ALL__list__ITA_Capitals' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                error_bad_lines=False,
                )
            df__list__COB = pd.read_csv(
                CSV_PATH + 'COB__list__ITA_WeatherStations__All' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                dtype={'wmo_code': str},
                )
            df__list__COB_capo = pd.read_csv(
                CSV_PATH + 'COB__list__ITA_WeatherStations__Capitals' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                dtype={'wmo_code': str},
                )
            df__list__MSTAT = pd.read_csv(
                CSV_PATH + 'MSTAT__list__ITA_WeatherStations__All' + file_ext,
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                error_bad_lines=False,
                )

    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred: {err}")
    except UnicodeDecodeError as e:
        raise SystemExit(f"Encoding error in file: {e}")

    return df__list__CTI, df__list__COB, df__list__MSTAT, df__list__ITA_capo, df__list__COB_capo



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
            df__DBT__CTI = pd.read_csv(
                CSV_PATH +     'CTI__DBT__ITA_WeatherStations__All'                    + file_ext,
                parse_dates=['datetime'], index_col='datetime',
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df__DBT__COB = pd.read_csv(
                CSV_PATH +     'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__All'     + file_ext,
                parse_dates=['datetime'], index_col='datetime',
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
            df__DBT__COB_capo = pd.read_csv(
                CSV_PATH +'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__Capitals'+ file_ext,
                parse_dates=['datetime'], index_col='datetime',
                encoding='ISO-8859-1', keep_default_na=False, na_values=['NaN'],
                )
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred: {err}")
    except UnicodeDecodeError as e:
        raise SystemExit(f"Encoding error in file: {e}")

    return df__DBT__CTI, df__DBT__COB, df__DBT__COB_capo





def load_geojson(file_path):
    # Check if the source is a URL (http/https) or a local file

    if file_path.startswith('http://') or file_path.startswith('https://'):
        # Source is a URL, use requests to access the data
        response = requests.get( file_path )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to load data from URL: {file_path}")
    else:
        # Source is a local file, load it using open
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


# Load TopoJSON
def LoadData_regions_provinces(GEOJSON_PATH):
    # json_file = json.loads(requests.get(GEOJSON_PATH + 'limits_IT_provinces.geojson').text)
    file_path = GEOJSON_PATH + 'limits_IT_regions.geojson'
    geojson_italy_regions = load_geojson(file_path)

    file_path = GEOJSON_PATH + 'limits_IT_provinces.geojson'
    geojson_italy_provinces = load_geojson(file_path)
    return geojson_italy_regions, geojson_italy_provinces




def load_file_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error if the download failed
    return response.text



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
