# IMPORT LIBRARIES
from fn__import_py_libs import *
#
#
#
#
#
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # haversine formula 
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r



def calculate_distances(df, point):
    distances = []
    for _, row in df.iterrows():
        data_point = (row['lat'], row['lon'])
        distance = haversine(point, data_point)
        distances.append(distance)
    return distances




# Function to create map
def folium__map__italy(df, color_marker, color_fill, marker_radius):
    m = folium.Map(location=[42, 12.6], zoom_start=6)
    for index, row in df.iterrows():
        folium.Circle(
            location=[row['lat'], row['lon']],
            radius=marker_radius,
            color=color_marker,
            fill=True,
            fill_color=color_fill,
            opacity=1,
            fill_opacity=0.5,
        ).add_to(m)
    return m






def create_map_with_jawg_style(center_lat, center_lon, zoom_start, jawg_access_token, jawg_style):
    # Jawg tile URL template
    jawg_url = 'https://{s}.tile.jawg.io/jawg-light/{z}/{x}/{y}{r}.png?access-token={accessToken}'
    jawg_url = f'https://{jawg_style}.tile.jawg.io/{jawg_style}/{{z}}/{{x}}/{{y}}{{r}}.png?access-token={jawg_access_token}'
    st.markdown(jawg_url)

    # Create a map object
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)

    # Add the Jawg tile layer
    folium.TileLayer(
        tiles=jawg_url,
        attr='&copy; <a href="https://www.jawg.io" target="_blank">Jawg Maps</a>',
        accessToken=jawg_access_token,  # Replace with your Jawg access token
        name=jawg_style,
        subdomains='abcd',
        control=False,
    ).add_to(m)

    return m




def generate_folium_map_with_geojson_popup(
        selected_region, geojson_province, geojson_region,
        center_lat, center_lon, zoom_start,
        color_region, color_province, fill_opacity_region, fill_opacity_province,
        map_tileset, jawg_style, jawg_access_token):


    if 'jawg' in map_tileset:
        m = create_map_with_jawg_style(center_lat, center_lon, zoom_start, jawg_access_token, jawg_style)

    else:
        # Create a Folium map with the specified center and zoom level
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start, tiles=map_tileset)


    # Filter function for provinces and regions GeoJSON data
    def filter_geojson_by_region(geojson_data, region_name, key):
        filtered_features = [feature for feature in geojson_data['features']
                             if feature['properties'][key] == region_name]
        return {'type': 'FeatureCollection', 'features': filtered_features}

    # Filter provinces and the region based on selected region
    filtered_provinces = filter_geojson_by_region(geojson_province, selected_region, 'reg_name')
    filtered_region = filter_geojson_by_region(geojson_region, selected_region, 'reg_name')

    # Define style functions for provinces and regions
    def style_province(feature):
        return {
            'fillColor': color_province,    # Fill color for provinces
            'color': color_province,        # Border color for provinces
            'weight': 2,                    # Border width for provinces
            'dashArray': '3, 3',            # Style of the border (optional)
            'fillOpacity': fill_opacity_province,    # Fill opacity for provinces
        }

    def style_region(feature):
        return {
            'fillColor': color_region,  # Fill color for regions
            'color': color_region,      # Border color for regions
            'weight': 4,                # Border width for regions
            'dashArray': '1, 5',            # Style of the border (optional)
            'fillOpacity': fill_opacity_region,      # Fill opacity for regions
        }

    # Check and add filtered GeoJSON layer for provinces
    if filtered_provinces['features']:
        folium.GeoJson(
            filtered_provinces,
            name='Provinces',
            style_function=style_province,
            tooltip=folium.GeoJsonTooltip(fields=['prov_name']),    # Tooltip for provinces
            popup=folium.GeoJsonPopup(fields=['prov_name'], sticky=False),        # Popup for provinces
        ).add_to(m)
    else:
        print(f"No provinces found for region: {selected_region}")

    # Check and add filtered GeoJSON layer for the selected region
    if filtered_region['features']:
        folium.GeoJson(
            filtered_region,
            name='Selected Region',
            style_function=style_region,
            tooltip=folium.GeoJsonTooltip(fields=['reg_name']),     # Tooltip for region
            popup=folium.GeoJsonPopup(fields=['reg_name']),         # Popup for region
        ).add_to(m)
    else:
        print(f"No region found with the name: {selected_region}")


    # Add a layer control panel
    folium.LayerControl().add_to(m)

    return m


# Function to add markers
def add_markers_to_map(m, latitude_col, longitude_col, location_col, marker_color, marker_icon, marker_size):

    # Add points for each location
    for lat, lon, location in zip(latitude_col, longitude_col, location_col):
        folium.Marker(
            [lat, lon],
            popup=location,
            icon=folium.Icon(color=marker_color, icon=marker_icon, size=marker_size)
            ).add_to(m)

    return m







def generate_folium_map_with_geojson_popup__italy(
        # selected_region, geojson_province, geojson_region,
        center_lat, center_lon, zoom_start,
        color_region, color_province, fill_opacity_region, fill_opacity_province,
        map_tileset, jawg_style, jawg_access_token):


    if 'jawg' in map_tileset:
        m = create_map_with_jawg_style(center_lat, center_lon, zoom_start, jawg_access_token, jawg_style)

    else:
        # Create a Folium map with the specified center and zoom level
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start, tiles=map_tileset)


    # Define style functions for provinces and regions
    def style_province(feature):
        return {
            'fillColor': color_province,    # Fill color for provinces
            'color': color_province,        # Border color for provinces
            'weight': 2,                    # Border width for provinces
            'dashArray': '3, 3',            # Style of the border (optional)
            'fillOpacity': fill_opacity_province,    # Fill opacity for provinces
        }

    def style_region(feature):
        return {
            'fillColor': color_region,  # Fill color for regions
            'color': color_region,      # Border color for regions
            'weight': 4,                # Border width for regions
            'dashArray': '1, 5',            # Style of the border (optional)
            'fillOpacity': fill_opacity_region,      # Fill opacity for regions
        }


    # Check and add filtered GeoJSON layer for the selected region
    if filtered_region['features']:
        folium.GeoJson(
            filtered_region,
            name='Selected Region',
            style_function=style_region,
            tooltip=folium.GeoJsonTooltip(fields=['reg_name']),     # Tooltip for region
            popup=folium.GeoJsonPopup(fields=['reg_name']),         # Popup for region
        ).add_to(m)
    else:
        print(f"No region found with the name: {selected_region}")


    # Add a layer control panel
    folium.LayerControl().add_to(m)

    return m




def generate_scatter_map_small(
        latitude_col, longitude_col, location_col, chart_height, marker_size, marker_color, zoom01, zoom02,mapbox_access_token):
    fig_small_01 = go.Figure()
    fig_small_01.add_traces(
        go.Scattermapbox(
            lat=latitude_col,
            lon=longitude_col,
            text=location_col,
            mode='markers',
            marker=go.scattermapbox.Marker(size=marker_size, color=marker_color),
            )
    )
    fig_small_01.update_layout(
        showlegend=False,
        height=chart_height,
        hovermode='closest',
        mapbox_style="light",
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(lat=latitude_col[0],lon=longitude_col[0]),
            zoom=zoom01,
        )
    )
    fig_small_02 = go.Figure(fig_small_01)
    fig_small_02.update_layout(
        mapbox=dict(zoom=zoom02)
    )

    return fig_small_01, fig_small_02








leaflet_styles = {
    'OpenStreetMap': {
        'url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'attribution': '© OpenStreetMap contributors'
    },
    'Stamen Terrain': {
        'url': 'https://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg',
        'attribution': 'Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    },
    'Stamen Toner': {
        'url': 'https://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',
        'attribution': 'Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    },
    'CartoDB Positron': {
        'url': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        'attribution': 'Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    },
    'CartoDB Dark_Matter': {
        'url': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',
        'attribution': 'Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    },
    'Esri WorldStreetMap': {
        'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        'attribution': 'Tiles © Esri — Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
    },
    'HikeBike': {
        'url': 'https://{s}.tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png',
        'attribution': '© Hike & Bike Map contributors'
    },
    'Hydda Full': {
        'url': 'https://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png',
        'attribution': 'Tiles courtesy of OpenStreetMap Sweden. Data by OpenStreetMap, under ODbL.'
    },
    'Jawg Streets': {
        'url': 'https://{s}.tile.jawg.io/jawg-streets/{z}/{x}/{y}{r}.png',
        'attribution': '© Jawg - Map data © OpenStreetMap contributors'
    },
    'MapBox': {
        'url': 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}',
        'attribution': 'Map data © OpenStreetMap contributors, CC BY-SA, Imagery © Mapbox'
    },
    'MapSurfer.NET': {
        'url': 'http://tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png',
        'attribution': 'Map data © OpenStreetMap contributors'
    },
    # ... (other styles)
    'Stamen Watercolor': {
        'url': 'https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg',
        'attribution': 'Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    },
    # ... (more styles including Thunderforest, etc.)
    # Add more styles as needed with their respective URLs and attributions
}

jawg_access_token = 'C8RWqxtIEMnrfwnoTXgxt2Ih8H91sYnuFsbgrvQFFEMevV93OLYPNZ9PafKNIhzC'  # Replace with your actual Jawg access token


st.session_state['leaflet_styles'] = leaflet_styles