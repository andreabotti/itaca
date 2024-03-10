# This file allows to modularise the streamlit app code, and import all necessary python libraries at once


# Data handling and general libraries
import io, re, os, sys, time, json, datetime, requests, urllib.request, base64

from datetime import datetime
import numpy as np, pandas as pd, geopandas as gpd
from meteostat import Stations, Hourly, Daily, Point


# Mapping
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
from scipy.spatial.distance import cdist


import streamlit as st
import folium
from streamlit_folium import folium_static, st_folium


# Plotting
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go, plotly.express as px
from plotly.subplots import make_subplots
from streamlit_plotly_events import plotly_events
import altair as alt
import leafmap.foliumap as leafmap
import chart_studio
chart_studio.tools.set_credentials_file(username='a.botti', api_key='aA5cNIJUz4yyMS9TLNhW');
