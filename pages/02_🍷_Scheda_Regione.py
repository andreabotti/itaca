# IMPORT LIBRARIES
from fn__import_py_libs import *
from fn__create_charts import *
from streamlit_folium import folium_static
from fn__mapping import *
mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'



# PAGE CONFIG
st.set_page_config(page_title="ITACA Streamlit App", page_icon='🍝', layout="wide")
from fn__page_header import create_page_header
color_marker_CTI, color_marker_COB, color_marker_MSTAT, color_marker_FWG = create_page_header()






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
df__list__CTI = st.session_state['df__list__CTI']
df__list__COB = st.session_state['df__list__COB']
df__list__COB_capo = st.session_state['df__list__COB_capo']
df__list__ITA_capo = st.session_state['df__list__ITA_capo']


df__DBT__CTI = st.session_state['df__DBT__CTI']
df__DBT__COB = st.session_state['df__DBT__COB']
df__DBT__COB_capo = st.session_state['df__DBT__COB_capo']

geojson_italy_regions = st.session_state['geojson_italy_regions']
geojson_italy_provinces = st.session_state['geojson_italy_provinces']





# Filter CTI and COB stations based on selected region
selected_reg = [i for i in dict_regions if dict_regions[i]==selected_region][0]
df_SelectedLocations_COB = df__list__COB[df__list__COB.reg_shortname == selected_reg]
df_SelectedLocations_CTI = df__list__CTI[df__list__CTI.reg_name == selected_region]

df_SelectedLocations_CTI['lat'] = pd.to_numeric(df_SelectedLocations_CTI['lat'], errors='coerce')
df_SelectedLocations_CTI['lon'] = pd.to_numeric(df_SelectedLocations_CTI['lon'], errors='coerce')
df_SelectedLocations_COB['lat'] = pd.to_numeric(df_SelectedLocations_COB['lat'], errors='coerce')
df_SelectedLocations_COB['lon'] = pd.to_numeric(df_SelectedLocations_COB['lon'], errors='coerce')

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


image_path = SVG_PATH + '{r}.svg'.format(r=selected_reg)

st.sidebar.markdown('\n')
st.sidebar.image(image_path, width=200)





# Calculate the centroid of the provided data points
center_latitude = sum(df_SelectedLocations_CTI.lat) / len(df_SelectedLocations_CTI.lat)
center_longitude = sum(df_SelectedLocations_CTI.lon) / len(df_SelectedLocations_CTI.lon)




selected_folium_style = st.sidebar.selectbox("Selezionare lo stile mappa:", leaflet_styles)

# Example usage
tile_name = selected_folium_style  # Example tile style
tile_info = leaflet_styles[tile_name]
url = tile_info['url']
attribution = tile_info['attribution']



# selected_folium_style = 'openstreetmap'

folium_map = generate_folium_map_with_geojson_popup(
    selected_region=selected_region,
    geojson_province=geojson_italy_provinces,
    geojson_region=geojson_italy_regions,
    center_lat=center_latitude,  # Latitude for the center of the map
    center_lon=center_longitude,  # Longitude for the center of the map
    zoom_start=8,     # Initial zoom level
    map_tileset = selected_folium_style,
    jawg_access_token = jawg_access_token,
    jawg_style = selected_folium_style,
    color_region = '#E26017',   fill_opacity_region = 0.02,
    color_province = '#2C5D85', fill_opacity_province = 0.15,
    )

# folium.TileLayer(tiles=url, attr=attribution).add_to(folium_map)

folium_map = add_markers_to_map(
    m=folium_map,
    latitude_col=df_SelectedLocations_CTI.lat,  # Column for marker latitudes
    longitude_col=df_SelectedLocations_CTI.lon,  # Column for marker longitudes
    location_col=df_SelectedLocations_CTI.location,  # Column for marker labels
    marker_color = 'lightgray',
    marker_icon='', marker_size=7,
    )

folium_map = add_markers_to_map(
    m=folium_map,
    latitude_col=df_SelectedLocations_COB.lat,  # Column for marker latitudes
    longitude_col=df_SelectedLocations_COB.lon,  # Column for marker longitudes
    location_col=df_SelectedLocations_COB.epw_filename,  # Column for marker labels
    marker_color = 'orange',
    marker_icon='star', marker_size=7,
    )


# Add a layer control panel
folium.LayerControl().add_to(folium_map)


# marker_svg_path = image_path = SVG_PATH + 'marker_02.svg'
# add_custom_svg_markers(folium_map, [41.5], [11.0], ['TUZZO'], marker_svg_path)










# COLUMNS AND LAYOUT
col1, space1, col2 = st.columns([20,1,25])

with col1:
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
    folium_output = st_folium(folium_map, width=720, height=630, returned_objects=["last_object_clicked"])
##########



# Define a styling function for highlighting the entire row and making text bold
thres_dist = 5  #nearby_threshold_distance


def highlight_entire_row(row, threshold=thres_dist):
    style = []
    for _ in row:
        if row['distance'] < threshold:
            style.append(f'background-color: {bg_color}; font-weight: bold; font-size: {font_size}')
        else:
            style.append(f'font-size: {font_size}')
    return style



df_TablePlot_CTI.rename({'province':'prov'}, axis=1, inplace=True)
df_TablePlot_COB.drop(['reg_name'], axis=1, inplace=True)

##########
with col2:
    
    font_size = 6

    folium_output = folium_output.get("last_object_clicked")
    if folium_output != None:
        point = (folium_output.get("lat"), folium_output.get("lng"))
        # Calculate distances for each dataframe
        distances_COB = calculate_distances(df_TablePlot_COB, point)
        distances_CTI = calculate_distances(df_TablePlot_CTI, point)

        # You can add these distances back to the dataframe if needed
        df_TablePlot_COB['distance'] = distances_COB
        df_TablePlot_CTI['distance'] = distances_CTI

        # Filter rows where distance is less than 1 km in df_TablePlot_COB and  df_TablePlot_CTI
        df_nearby_CTI = df_TablePlot_CTI[df_TablePlot_CTI['distance'] < thres_dist]
        df_nearby_COB = df_TablePlot_COB[df_TablePlot_COB['distance'] < thres_dist]    

        st.markdown('**{s}** Stazioni in **{r}** da banca dati [**CTI**](https://try.cti2000.it/)'.format(
            s=len(df_TablePlot_CTI), r=selected_region)
        )
        # Combine styling and formatting and apply in Streamlit
        bg_color = color_marker_CTI
        styled_df_TablePlot_CTI = df_TablePlot_CTI.style.apply(highlight_entire_row, axis=1).format(
            {"alt": "{:.0f}", "lat": "{:.2f}", "lon": "{:.2f}", "distance": "{:.2f}"}
        )
        st.dataframe(styled_df_TablePlot_CTI)

        st.markdown(
            '**{s}** Stazioni in **{r}** da banca dati [Climate OneBuilding (COB)](https://climate.onebuilding.org)'.format(
            s=len(df_TablePlot_COB), r=selected_region)
        )
        # Combine styling and formatting and apply in Streamlit
        bg_color = color_marker_COB
        styled_df_TablePlot_COB = df_TablePlot_COB.style.apply(highlight_entire_row, axis=1).format(
            {"alt": "{:.0f}", "lat": "{:.2f}", "lon": "{:.2f}", "distance": "{:.2f}"}
        )
        st.dataframe(styled_df_TablePlot_COB)

        if len(df_nearby_CTI) > 0:
            output_value = df_nearby_CTI.iloc[0]['location']
        elif len(df_nearby_COB) > 0:
            output_value = df_nearby_COB.iloc[0]['epw_filename']
        else:
            output_value=None
        st.write(output_value)


    else:
        st.markdown('**{s}** Stazioni in **{r}** da banca dati [**CTI**](https://try.cti2000.it/)'.format(
            s=len(df_TablePlot_CTI), r=selected_region)
        )
        df_TablePlot_CTI = df_TablePlot_CTI.style.format(
            {"alt": "{:.0f}", "lat": "{:.2f}", "lon": "{:.2f}"}
        )
        st.dataframe(df_TablePlot_CTI)

        st.markdown(
            '**{s}** Stazioni in **{r}** da banca dati [Climate OneBuilding (COB)](https://climate.onebuilding.org)'.format(
            s=len(df_TablePlot_COB), r=selected_region)
        )
        df_TablePlot_COB = df_TablePlot_COB.style.format(
            {"alt": "{:.0f}", "lat": "{:.2f}", "lon": "{:.2f}"}
        )
        st.dataframe(df_TablePlot_COB)



##########



st.session_state['df_SelectedLocations_CTI'] = df_SelectedLocations_CTI
st.session_state['df_SelectedLocations_COB'] = df_SelectedLocations_COB

st.session_state['selected_reg'] = selected_reg
st.session_state['selected_region'] = selected_region

st.session_state['color_marker_CTI'] = color_marker_CTI
st.session_state['color_marker_COB'] = color_marker_COB
