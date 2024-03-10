# IMPORT LIBRARIES
from fn__import_py_libs import *
from fn__create_charts import *
from fn__data_manipulation import *
from fn__mapping import *

mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'


# PAGE CONFIG
st.set_page_config(page_title="ITACA Streamlit App", page_icon='🍝', layout="wide")
from fn__page_header import create_page_header
color_marker_CTI, color_marker_COB, color_marker_MSTAT, color_marker_FWG = create_page_header()





# Define main path and csv path
MAIN_PATH = st.session_state['MAIN_PATH']
CSV_PATH = MAIN_PATH + 'data_csv/'

# Load data into session state
df__list__CTI, df__list__COB, df__list__MSTAT = st.session_state['df__list__CTI'], st.session_state['df__list__COB'], st.session_state['df__list__MSTAT']
df__list__ITA_capo, df__list__COB_capo = st.session_state['df__list__ITA_capo'], st.session_state['df__list__COB_capo']

df__DBT__CTI, df__DBT__COB, df__DBT__COB_capo = st.session_state['df__DBT__CTI'], st.session_state['df__DBT__COB'], st.session_state['df__DBT__COB_capo']

geojson_italy_regions, geojson_italy_provinces = st.session_state['geojson_italy_regions'], st.session_state['geojson_italy_provinces']




##### ##### ##### ##### #####       ##### ##### ##### ##### #####       ##### ##### ##### ##### #####

# Convert latitude and longitude to numeric values
df__list__CTI['lat'] = pd.to_numeric(df__list__CTI['lat'], errors='coerce')
df__list__CTI['lon'] = pd.to_numeric(df__list__CTI['lon'], errors='coerce')

df__list__COB['lat'] = pd.to_numeric(df__list__COB['lat'], errors='coerce')
df__list__COB['lon'] = pd.to_numeric(df__list__COB['lon'], errors='coerce')

df__list__COB_capo['lat'] = pd.to_numeric(df__list__COB_capo['lat'], errors='coerce')
df__list__COB_capo['lon'] = pd.to_numeric(df__list__COB_capo['lon'], errors='coerce')


# Drop 'id' column from df__list__MSTAT if it exists
try:
    df__list__MSTAT.drop(['id'], axis=1, inplace=True)
except:
    pass




##### ##### ##### ##### #####       ##### ##### ##### ##### #####       ##### ##### ##### ##### #####

# Prepare data for distance calculation
cti_coords = df__list__ITA_capo[['lat', 'lon']].to_numpy()
cob_coords = df__list__COB_capo[['lat', 'lon']].to_numpy()

# Calculate Euclidean distances
distances = cdist(cti_coords, cob_coords, metric='euclidean')
closest_cob_indices = np.argmin(distances, axis=1)

# Create a result dataframe with closest COB location and distance
result = df__list__ITA_capo.copy()
result['closest_COB_location'] = df__list__COB_capo.iloc[closest_cob_indices]['location'].values
result['wmo'] = df__list__COB_capo.iloc[closest_cob_indices]['wmo_code'].values
result['distance (km)'] = (1*np.min(distances, axis=1)).round(1)

df__list__CTI_COB_capo = result


# Assuming df1 and df__DBT__CTI are your dataframes, and df__DBT__CTI has a column 'location_name'
df__list__CTI_COB_capo_mapped = find_closest(df1=df__list__CTI_COB_capo, df2=df__list__CTI, lat_col='lat', lon_col='lon', name_col='location')



##### ##### ##### ##### #####       ##### ##### ##### ##### #####       ##### ##### ##### ##### #####

# MAPPING FUNCTIONS
# Extracting WMO codes and location names for COB data
wmo_code_to_location = df__list__COB_capo.set_index('wmo_code')['location'].to_dict()

# Create a mapping from the 'closest_COB_location' to the 'province' in df__list__CTI_COB_capo
location_to_province = df__list__CTI_COB_capo.set_index('closest_COB_location')['province'].to_dict()

# Create a mapping from the 'closest_COB_location' to the combined 'reg_shortname' and 'province' in df__list__CTI_COB_capo
location_to_reg_province = df__list__CTI_COB_capo.set_index('closest_COB_location').apply(lambda row: f"{row['reg_shortname']}__{row['province']}", axis=1).to_dict()

# Process the CTI temperature data using the same approach as for the COB data - We use the location names directly from df_result for CTI locations
cti_locations = df__list__ITA_capo['location']







##### ##### ##### ##### #####       ##### ##### ##### ##### #####       ##### ##### ##### ##### #####

max_percentile = 0.97

df__DBT__CTI__monthly_mean = process_temperature_data(
    df=df__DBT__CTI, locations=df__list__CTI.location, prefix='CTI', statistic='mean', percentile=None, convert_index_to_month=True,
    )
df__DBT__CTI__monthly_max = process_temperature_data(
    df=df__DBT__CTI, locations=df__list__CTI.location, prefix='CTI', statistic='max', percentile=max_percentile, convert_index_to_month=True,
    )



##### ##### ##### ##### #####       ##### ##### ##### ##### #####       ##### ##### ##### ##### #####

# Sample structure of df__DTB__CTI and df__DTB__COB
dataframes_dict = {}



def mapping__CTI__COB__df__capo_list(df_mapping, df_cti, df_cob):

    for index, row in df_mapping.iterrows():

        reg_shortname = row['reg_shortname']
        province = row['province']
        location = row['location']

        cti_location = row['closest_CTI_location']
        cob_location = row['closest_COB_location']
        wmo = row['wmo']

        # Construct the column header pattern
        cti_col_pattern = f"{reg_shortname}__{province}__{cti_location}"
        cob_col_pattern = f"{reg_shortname}__{province}__{wmo}"

        st.write(f'CTI: {cti_col_pattern} - - - COB: {cob_col_pattern}')

        # Extract the relevant columns
        cti_col = df_cti.filter(like=cti_col_pattern, axis=1)
        cob_col = df_cob.filter(like=cob_col_pattern, axis=1)

        # Combine into a new dataframe
        combined_df = pd.concat([cti_col, cob_col], axis=1)

        try:
            # Calculate the difference and create a new column
            diff_col_name = f"{reg_shortname}__{province}__diff"
            combined_df[diff_col_name] = combined_df['COB__'+cob_col_pattern] - combined_df['CTI__'+cti_col_pattern]
        except:
            pass
            

        # Store in the dictionary
        # dataframes_dict[index] = combined_df
        dataframes_dict[location] = combined_df

    return dataframes_dict





##### ##### ##### ##### #####       ##### ##### ##### ##### #####       ##### ##### ##### ##### #####

# Streamlit layout with tabs
tab1, tab2, tab3, tab4 = st.tabs(['Stazioni CTI', 'Stazioni COB', 'Stazioni MSTAT', 'MAPPA Confronto'])
map_width, map_height, table_width = 580, 680, 850

# Fill missing lat and lon values and create maps
df__list__CTI.fillna({'lat': 0, 'lon': 0}, inplace=True)
map1 = folium__map__italy(df__list__CTI, color_marker=color_marker_CTI, color_fill=color_marker_CTI, marker_radius=4000)
map2 = folium__map__italy(df__list__COB, color_marker=color_marker_COB, color_fill=color_marker_COB, marker_radius=4000)
map3 = folium__map__italy(df__list__MSTAT, color_marker=color_marker_MSTAT, color_fill=color_marker_MSTAT, marker_radius=4000)
map4 = folium__map__italy(df__list__ITA_capo, color_marker='black', color_fill='black', marker_radius=6000)



with tab1:
    col1, space1, col2 = st.columns([10,1,15])

    with col1:
        st.markdown('###### Mappa delle stazioni dal dataset Comitato Termotecnico Italiano (CTI)')
        folium_static(map1, width=map_width, height=map_height)

    with col2:
        tab11, tab12 = st.tabs(['Lista delle Stazioni', 'Temperature orarie'])
        with tab11:
            df__list__CTI__table = df__list__CTI.drop(['reg_shortname'], axis=1)
            st.markdown( f'###### Lista delle {df__list__CTI__table.shape[0]} stazioni meteo del dataset CTI')
            st.dataframe(df__list__CTI__table, width=table_width, height=map_height-50)

        with tab12:
            st.markdown(f'###### Temperature orarie per le {df__DBT__CTI.shape[1]} stazioni meteo del dataset CTI')
            st.dataframe(df__DBT__CTI, width=table_width, height=map_height-50)


with tab2:
    col1, space1, col2 = st.columns([10,1,15])
    with col1:
        st.markdown('###### Mappa delle stazioni dal dataset climate.onebuilding.org (COB)')
        folium_static(map2, width=map_width, height=map_height)

    with col2:
        tab11, tab12 = st.tabs(['Lista delle Stazioni', 'Temperature orarie'])
        with tab11:
            df__list__COB__table = df__list__COB.drop(['reg_shortname'], axis=1)
            st.markdown( f'###### Lista delle {df__list__COB__table.shape[0]} stazioni meteo del dataset COB')
            st.dataframe(df__list__COB__table, width=table_width, height=map_height-50)

        with tab12:
            st.markdown(f'###### Temperature orarie per le {df__DBT__COB.shape[1]} stazioni meteo del dataset COB')
            st.dataframe(df__DBT__COB, width=table_width, height=map_height-50)


with tab3:
    col1, space1, col2 = st.columns([10,1,15])
    with col1:
        st.markdown('###### Mappa delle stazioni dal dataset Meteostat (MSTAT)')
        folium_static(map3, width=map_width, height=map_height)

    with col2:
        tab11, tab12 = st.tabs(['Lista delle Stazioni', 'Temperature orarie'])
        with tab11:
            df__list__MSTAT__table = df__list__MSTAT
            st.markdown( f'###### Lista delle {df__list__MSTAT__table.shape[0]} stazioni meteo del dataset CTI')
            st.dataframe(df__list__MSTAT__table, width=table_width, height=map_height-50)

        with tab12:
            # st.markdown(f'###### Temperature orarie per le {df__DBT__MSTAT.shape[1]} stazioni meteo del dataset CTI')
            st.dataframe(df__DBT__CTI, width=table_width, height=map_height-50)


with tab4:
    col1, space1, col2 = st.columns([10,1,15])
    with col1:
        st.markdown('###### Mappa dei capoluoghi italiani')
        folium_static(map4, width=map_width, height=map_height)

    with col2:
        tab11, tab12 = st.tabs(['Lista delle Stazioni', 'Dati'])
        with tab11:
            df__list__ITA_capo__table = df__list__ITA_capo
            st.markdown( f'###### Lista dei {df__list__ITA_capo__table.shape[0]} capoluoghi d\'Italia')
            st.dataframe(df__list__ITA_capo__table, width=table_width, height=map_height-50)


st.markdown('---')
with st.expander(label='Dataframe mapping CTI and COB locations'):
    st.dataframe(df__list__CTI_COB_capo_mapped, width=1500, height=750)

st.markdown('---')



dataframes_dict = mapping__CTI__COB__df__capo_list(df_cti = df__DBT__CTI, df_cob = df__DBT__COB, df_mapping = df__list__CTI_COB_capo_mapped)


for key in dataframes_dict:
    st.write(key)
    df = dataframes_dict[key]
    st.dataframe(df[:5], width=600, height=300)



st.markdown('---')






'''
# Display of Processed Data
with st.expander('# Display of CTI Data'):

    st.markdown('---')
    st.markdown('###### *df__DBT__CTI*')
    st.dataframe(df__DBT__CTI[:3])
    st.write(df__DBT__CTI.shape)
    
    st.markdown('---')
    st.markdown('###### *df__DBT__CTI__monthly_mean*')
    st.dataframe(df__DBT__CTI__monthly_mean[6:9])
    st.write(df__DBT__CTI__monthly_mean.shape)


with st.expander('# Display of COB Data'):

    st.markdown('---')
    st.markdown('###### *df__DBT__COB__monthly_mean*')
    st.dataframe(df__DBT__COB__monthly_mean[6:9])
    st.write(df__DBT__COB__monthly_mean.shape)

    st.markdown('---')
    st.markdown('###### *df__DBT__COB__monthly_mean - columns*')
    st.write(df__DBT__COB__monthly_mean.columns)

st.markdown('---')
'''








def rename_columns_with_mapping(df, df_mapping):
    # Check if 'reg_shortname' and 'province' columns exist in df_mapping
    if 'reg_shortname' not in df_mapping.columns or 'province' not in df_mapping.columns:
        raise ValueError("df_mapping must have 'reg_shortname' and 'province' columns")

    # Create a dictionary for column renaming
    column_rename_mapping = {}
    for index, row in df_mapping.iterrows():
        # Extract 'reg_shortname' and 'province' values from df_mapping
        reg_shortname = row['reg_shortname']
        province = row['province']

        # Create the new column prefix
        new_prefix = f"{reg_shortname}__{province}__"

        # Iterate through the columns of df__DBT__COB and create new column names
        for column in df.columns:
            new_column_name = f"{new_prefix}{column}"
            column_rename_mapping[column] = new_column_name

    # Rename the columns of df__DBT__COB using the mapping
    df = df.rename(columns=column_rename_mapping)

    return df

# Example usage:
# df__DBT__COB is your DataFrame, and df_mapping is the mapping DataFrame
# renamed_df = rename_columns_with_mapping(df__DBT__COB, df_mapping)


df__DBT__COB__renamed = rename_columns_with_mapping(df=df__DBT__COB, df_mapping=df_mapping)
df__DBT__COB_capo__renamed = rename_columns_with_mapping(df=df__DBT__COB_capo, df_mapping=df_mapping)



# LOCAL_PATH  = r'C:/_GitHub/andreabotti/itaca/'
# MAIN_PATH = LOCAL_PATH
# CSV_PATH = MAIN_PATH + 'data_csv/'

# df__DBT__COB__renamed.to_csv( CSV_PATH + 'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__All.csv')
# df__DBT__COB_capo__renamed.to_csv( CSV_PATH + 'COB__DBT__ITA_WeatherStations_TMYx.2007-2021__Capitals.csv')