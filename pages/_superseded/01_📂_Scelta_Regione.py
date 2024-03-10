# IMPORT LIBRARIES
from fn__import_py_libs import *
mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'
#
#
#
#
#
#
# PAGE CONFIG
st.set_page_config(page_title="ITACA Streamlit App",   page_icon='🌡️', layout="wide")
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
                'CTI', '#C4C5C4', help='**CTI = Comitato Termotecnico Italiano** : dati climatici rappresentativi (*anno tipo*) del recente passato',
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


MAIN_PATH = st.session_state['MAIN_PATH']
SVG_PATH = MAIN_PATH + 'img_svg/'
#
#
#
#
#

# Region Selection
dict_regions = st.session_state['dict_regions']
regions_list = st.session_state['regions_list']
selected_region = st.sidebar.selectbox("Selezionare la regione:", regions_list)

# STREAMLIT SESSION STATE - LOAD DATA
df_locations_CTI = st.session_state['df_locations_CTI']
df_locations_COB = st.session_state['df_locations_COB']
df_locations_COB_capo = st.session_state['df_locations_COB_capo']
df_capoluoghi = st.session_state['df_capoluoghi']

geojson_italy_regions = st.session_state['geojson_italy_regions']
geojson_italy_provinces = st.session_state['geojson_italy_provinces']

df_CTI_DBT = st.session_state['df_CTI_DBT']
df_COB_DBT = st.session_state['df_COB_DBT']
df__COB_capo__DBT = st.session_state['df__COB_capo__DBT']




#
# Filter CTI and COB stations based on selected region
selected_reg = [i for i in dict_regions if dict_regions[i]==selected_region][0]
df_SelectedLocations_COB = df_locations_COB[df_locations_COB.reg_shortname == selected_reg]
df_SelectedLocations_CTI = df_locations_CTI[df_locations_CTI.reg_name == selected_region]
#
df_TablePlot_CTI = df_SelectedLocations_CTI
df_TablePlot_COB = df_SelectedLocations_COB



try:
    df_TablePlot_COB.drop(['location'], axis=1, inplace=True)
except:
    ''
df_TablePlot_CTI = df_TablePlot_CTI[['province', 'location', 'lat', 'lon', 'alt']]
df_TablePlot_COB.drop(['reg_shortname'], axis=1, inplace=True)
n = df_TablePlot_CTI.shape[0]
#
#
#
#
#
image_path = SVG_PATH + '{r}.svg'.format(r=selected_reg)

st.sidebar.markdown('\n')
st.sidebar.image(image_path, width=200)
#
#
#
#
#
# COLUMNS AND LAYOUT
col1, space1, col2 = st.columns([20,1,25])

with col1:
    # Calculate the centroid of the provided data points
    center_latitude = sum(df_SelectedLocations_CTI.lat) / len(df_SelectedLocations_CTI.lat)
    center_longitude = sum(df_SelectedLocations_CTI.lon) / len(df_SelectedLocations_CTI.lon)

    fig2 = go.Figure()
    fig2.add_traces(
        go.Scattermapbox(
            lat=df_SelectedLocations_CTI.lat,
            lon=df_SelectedLocations_CTI.lon,
            text=df_SelectedLocations_CTI.province,
            mode='markers',
            marker=go.scattermapbox.Marker(size=10, color=color_marker_CTI),
            )
    )
    fig2.add_traces(
        go.Scattermapbox(
            lat=df_SelectedLocations_COB.lat,
            lon=df_SelectedLocations_COB.lon,
            text=df_SelectedLocations_COB.epw_filename,
            mode='markers',
            marker=go.scattermapbox.Marker(size=10, color=color_marker_COB),
            )
    )
    fig2.update_layout(
        showlegend=False,
        height=600,
        hovermode='closest',
        mapbox_style="light",
        # mapbox_style = 'mapbox://styles/andreabotti/cln47wjba036a01qubmem1lox',
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(lat=center_latitude,lon=center_longitude),
            zoom=7,
            # style='mapbox://styles/andreabotti/cln47wjba036a01qubmem1lox',
        )
    )

    st.markdown('###### Mappa delle stazioni meteo in {r}'.format(r=selected_region))
    st.plotly_chart(fig2, use_container_width=True)
##########




##########
with col2:
    df_TablePlot_CTI.rename({'province':'prov'}, axis=1, inplace=True)

    st.markdown('**{s}** Stazioni in **{r}** da banca dati [**CTI**](https://try.cti2000.it/)'.format(
        s=len(df_TablePlot_CTI), r=selected_region)
    )
    st.dataframe(df_TablePlot_CTI.style.format(
        { "alt": "{:.0f}", "lat": "{:.2f}", "lon": "{:.2f}", }
        ))

with col2:
    df_TablePlot_COB.drop(['reg_name'], axis=1, inplace=True)

    st.markdown(
        '**{s}** Stazioni in **{r}** da banca dati [Climate OneBuilding (COB)](https://climate.onebuilding.org)'.format(
        s=len(df_TablePlot_COB), r=selected_region)
    )
    st.dataframe(df_TablePlot_COB.style.format(
        { "alt": "{:.0f}", "lat": "{:.2f}", "lon": "{:.2f}", }
        ))

##########



st.session_state['df_SelectedLocations_CTI'] = df_SelectedLocations_CTI
st.session_state['df_SelectedLocations_COB'] = df_SelectedLocations_COB

st.session_state['selected_reg'] = selected_reg
st.session_state['selected_region'] = selected_region

st.session_state['color_marker_CTI'] = color_marker_CTI
st.session_state['color_marker_COB'] = color_marker_COB
