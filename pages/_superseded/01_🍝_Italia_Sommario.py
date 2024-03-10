# IMPORT LIBRARIES
from fn__import_py_libs import *
from fn__create_charts import *
from streamlit_folium import folium_static
mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'
#
#
#
#
#
#
# PAGE CONFIG
st.set_page_config(page_title="ITACA Streamlit App",   page_icon='🍝', layout="wide")
st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 2.5rem; padding-right: 2.5rem;}</style>""",
    unsafe_allow_html=True)


# TOP CONTAINER
TopColA, TopColB = st.columns([6,2])
with TopColA:
    st.markdown("# ITA.C.A")
    st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
    st.caption('Developed by AB.S.RD - https://absrd.xyz/')
#
with TopColB:
    # Introduce vertical spaces
    st.markdown('<div style="margin: 35px;"></div>', unsafe_allow_html=True)  # 20px vertical space

    # with st.container(border=True):
    with st.container():
        # Your content here
        st.markdown('###### Scegli colore dei markers')
        TopColB1, TopColB2, TopColB3, TopColB4 = st.columns([1,1,1,1])
        with TopColB1:
            color_marker_CTI = st.color_picker(
                'CTI', '#8C8C8C', help='**CTI = Comitato Termotecnico Italiano** : dati climatici rappresentativi (*anno tipo*) del recente passato',
                )
        with TopColB2:
            color_marker_COB = st.color_picker(
                'COB', '#E2966D', help='**COB = climate.onebuilding.org** : dati climatici rappresentativi (*anno tipo*) del presente',
                )
        with TopColB3:
            color_marker_MSTAT = st.color_picker(
                'MSTAT', '#85A46E', help='**MSTAT = Meteostat** : dati climatici (*anni reali*) del recente passato e presente',
                )
        with TopColB4:
            color_marker_FWG = st.color_picker(
                'FWG', '#6C90AF', help='**FWG = Future Weather Generator** : dati climatici (*anno tipo*) rappresentativi di proiezioni future in linea con gli scenari IPCC',
                )
#####



#####
MAIN_PATH = st.session_state['MAIN_PATH']
CSV_PATH = MAIN_PATH + 'data_csv/'

# STREAMLIT SESSION STATE - LOAD DATA
df__list__CTI = st.session_state['df__list__CTI']
df__list__COB = st.session_state['df__list__COB']
df__list__MSTAT = st.session_state['df__list__MSTAT']
df__list__COB_capo = st.session_state['df__list__COB_capo']
df__list__ITA_capo = st.session_state['df__list__ITA_capo']

df__DBT__CTI = st.session_state['df__DBT__CTI']
df__DBT__COB = st.session_state['df__DBT__COB']
df__DBT__COB_capo = st.session_state['df__DBT__COB_capo']

geojson_italy_regions = st.session_state['geojson_italy_regions']
geojson_italy_provinces = st.session_state['geojson_italy_provinces']

#####
df__list__CTI['lat'] = pd.to_numeric(df__list__CTI['lat'], errors='coerce')
df__list__CTI['lon'] = pd.to_numeric(df__list__CTI['lon'], errors='coerce')

df__list__COB['lat'] = pd.to_numeric(df__list__COB['lat'], errors='coerce')
df__list__COB['lon'] = pd.to_numeric(df__list__COB['lon'], errors='coerce')

df__list__COB_capo['lat'] = pd.to_numeric(df__list__COB_capo['lat'], errors='coerce')
df__list__COB_capo['lon'] = pd.to_numeric(df__list__COB_capo['lon'], errors='coerce')
#####

















#####
def create_map(df, color_marker, color_fill):
    # Create a map centered around Italy
    m = folium.Map(location=[42, 12.6], zoom_start=6)

    # Add bubble markers for each capital in df
    for index, row in df.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            # radius=row['DBT'] * 2000,  # Example radius calculation
            radius=5000,  # Example radius calculation
            color=color_marker,
            fill=True,
            fill_color=color_fill,
        ).add_to(m)
    return m

try:
    df__list__MSTAT.drop(['id'], axis=1, inplace=True)
except:
    ''


#####
df_cti = df__list__ITA_capo
df_cob = df__list__COB_capo

cti_coords = df_cti[['lat', 'lon']].to_numpy()
cob_coords = df_cob[['lat', 'lon']].to_numpy()

# Recalculate the Euclidean distance between each pair of points
distances = cdist(cti_coords, cob_coords, metric='euclidean')

# Find the index of the closest COB location for each CTI location
closest_cob_indices = np.argmin(distances, axis=1)

# Add information about the closest COB location and distance to the result dataframe
df_result = df_cti.copy()
df_result['closest_COB_location'] = df_cob.iloc[closest_cob_indices]['location'].values
df_result['wmo'] = df_cob.iloc[closest_cob_indices]['wmo_code'].values
df_result['distance (km)'] = (1*np.min(distances, axis=1)).round(1)

df__list__CTI_COB_capo = df_result
#####






#####
# Streamlit layout
tab1, tab2, tab3, tab4 = st.tabs(['Stazioni CTI', 'Stazioni COB', 'Stazioni MSTAT', 'MAPPA Confronto'])
map_width   = 580
map_height  = 680
table_width = 850



# Create and display maps
df__list__CTI.fillna({'lat': 0, 'lon': 0}, inplace=True)
map1 = create_map(df__list__CTI, color_marker=color_marker_CTI, color_fill=color_marker_CTI)
map2 = create_map(df__list__COB, color_marker=color_marker_COB, color_fill=color_marker_COB)
map3 = create_map(df__list__MSTAT, color_marker=color_marker_MSTAT, color_fill=color_marker_MSTAT)



with tab1:
    col1, space1, col2 = st.columns([10,1,15])
    with col1:
        st.markdown('###### Mappa delle stazioni dal dataset Comitato Termotecnico Italiano (CTI)')
        folium_static(map1, width=map_width, height=map_height)
    with col2:
        st.markdown('###### Tabella delle stazioni')
        df__list__CTI__table = df__list__CTI.drop(['reg_shortname'], axis=1)
        st.dataframe(df__list__CTI__table, width=table_width, height=map_height)

with tab2:
    col1, space1, col2 = st.columns([10,1,15])
    with col1:
        st.markdown('###### Mappa delle stazioni dal dataset climate.onebuilding.org (COB)')
        folium_static(map2, width=map_width, height=map_height)
    with col2:
        st.markdown('###### Tabella delle stazioni')
        df__list__COB__table = df__list__COB.drop(['reg_shortname'], axis=1)
        st.dataframe(df__list__COB__table, width=table_width, height=map_height)

with tab3:
    col1, space1, col2 = st.columns([10,1,15])
    with col1:
        st.markdown('###### Mappa delle stazioni dal dataset Meteostat (MSTAT)')
        folium_static(map3, width=map_width, height=map_height)
    with col2:
        st.markdown('###### Tabella delle stazioni')
        st.dataframe(df__list__MSTAT, width=table_width, height=map_height)




with tab4:
    col1, space1, col2 = st.columns([10,1,15])
    ''
    # map1 = create_map(df__list__MSTAT, color_marker=color_marker_MSTAT, color_fill=color_marker_MSTAT)
    # map2 = create_map(df__list__COB_capo, color_marker=color_marker_COB, color_fill=color_marker_COB)
    # map3 = create_map(df__list__MSTAT, color_marker=color_marker_MSTAT, color_fill=color_marker_MSTAT)
    
    with col2:
        st.dataframe(df__list__CTI_COB_capo, width=table_width, height=740)



def process_temperature_data__CTI(df, locations, prefix, percentile):
    """
    Process the temperature data for the given locations.
    Calculate average, median, and 95th percentile for each month.
    """
    # Filter the dataframe to include only columns for the specified locations
    df_filtered = df[[col for col in df.columns if any(loc in col for loc in locations)]]
    df_filtered.index = pd.to_datetime(df_filtered.index)  # Ensure the index is in datetime format

    # Creating separate DataFrames for mean, median, and max (xth percentile)
    df_monthly_mean = df_filtered.resample('M').mean().round(1)
    df_monthly_median = df_filtered.resample('M').median().round(1)
    df_monthly_max = df_filtered.resample('M').quantile(percentile).round(1)

    # Rename columns to include prefix and statistic type
    df_monthly_mean.columns = [f"{prefix}__{col}__mean" for col in df_monthly_mean.columns]
    df_monthly_median.columns = [f"{prefix}__{col}__median" for col in df_monthly_median.columns]
    df_monthly_max.columns = [f"{prefix}__{col}__max" for col in df_monthly_max.columns]

    return df_monthly_mean, df_monthly_median, df_monthly_max



def process_temperature_data__COB(df, df_list, mapping, prefix, percentile):
    relevant_columns = [col for col in df.columns if col.split('_')[0] in mapping]
    df_filtered = df[relevant_columns]
    df_filtered.index = pd.to_datetime(df_filtered.index)

    # Rename columns according to the mapping
    df_filtered.rename(columns={col: mapping[col.split('_')[0]] for col in relevant_columns}, inplace=True)

    # Creating suffix from 'reg_shortcode' and 'province'
    prefix_mapping  = df_list.set_index('location').apply(lambda row: f"{row['reg_shortname']}__{row['province']}", axis=1).to_dict()
    df_filtered = df_filtered.rename(columns=lambda x: prefix_mapping.get(x, '') + '__' + x)

    # Creating separate DataFrames for mean, median, and max (xth percentile)
    df_monthly_mean = df_filtered.resample('M').mean()
    df_monthly_median = df_filtered.resample('M').median()
    df_monthly_max = df_filtered.resample('M').quantile(percentile)

    # Rename columns to include prefix and statistic type
    df_monthly_mean.columns = [f"{prefix}__{col}__mean" for col in df_monthly_mean.columns]
    df_monthly_median.columns = [f"{prefix}__{col}__median" for col in df_monthly_median.columns]
    df_monthly_max.columns = [f"{prefix}__{col}__max" for col in df_monthly_max.columns]

    return df_monthly_mean, df_monthly_median, df_monthly_max




max_percentile = 0.97

# Extracting WMO codes and location names for COB data
wmo_code_to_location = df__list__COB_capo.set_index('wmo_code')['location'].to_dict()

df__DBT__COB__monthly_mean, df__DBT__COB__monthly_median, df__DBT__COB__monthly_max = process_temperature_data__COB(
    df=df__DBT__COB_capo, df_list=df__list__CTI_COB_capo, mapping=wmo_code_to_location, prefix="COB", percentile=max_percentile,
)

# Process the CTI temperature data using the same approach as for the COB data - We use the location names directly from df_result for CTI locations
cti_locations = df__list__ITA_capo['location']
# cti_locations = df__list__CTI['location']

df__DBT__CTI__monthly_mean, df__DBT__CTI__monthly_median, df__DBT__CTI__monthly_max = process_temperature_data__CTI(
    df=df__DBT__CTI, locations=cti_locations, prefix="CTI", percentile=max_percentile,
)


st.markdown('###### *df__DBT__CTI*')
st.dataframe(df__DBT__CTI[:3])

st.markdown('###### *df__DBT__CTI__monthly_mean*')
st.dataframe(df__DBT__CTI__monthly_mean[6:9])

st.markdown('###### *df__DBT__COB__monthly_mean*')
st.dataframe(df__DBT__COB__monthly_mean[6:9])


st.write(df__DBT__COB__monthly_mean.columns)

