import pandas as pd
import numpy as np
import os
import sys
import folium
from folium import FeatureGroup, LayerControl
from commonFunctions import PopupHorizontally, ReverseLatLon
import geopandas as gpd
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
# icon object will be rendered using "https://github.com/lennardv2/Leaflet.awesome-markers"
# documentation of shapely: "https://shapely.readthedocs.io/en/stable/manual.html"
# information of railway track: "https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_0.html"


def main():


    # create base map
    folium_map = folium.Map(location=[35.466188, 139.622715], zoom_start=10)
    df_gjs = gpd.read_file('csv/N02-21_RailroadSection.geojson', encoding='SHIFT-JIS')

    # create feature group
    tokaidoStas = FeatureGroup(name="東海道本線(東京-熱海)")
    # polyline for railway track
    for i, row in df_gjs.iterrows():
        if row["N02_003"] == "東海道線" and row["N02_004"] == "東日本旅客鉄道":
            revLocations = ReverseLatLon(np.array(row["geometry"].coords))
            folium.PolyLine(locations=revLocations, color='orange', weigth=15).add_to(folium_map)
    # station markers
    df = pd.read_csv('csv/tokaidostas.csv', usecols=['jpname', 'name', 'latitude', 'longitude'], encoding='utf-8')
    for i, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=PopupHorizontally(row['jpname']),
            max_width=500,
            icon=folium.Icon(color='orange', icon='check')
        ).add_to(tokaidoStas)
    tokaidoStas.add_to(folium_map)

    # create feature group
    yokosukaStas = FeatureGroup(name="横須賀線", show=False)
    # polyline for railway track
    for i, row in df_gjs.iterrows():
        if row["N02_003"] == "横須賀線" and row["N02_004"] == "東日本旅客鉄道":
            revLocations = ReverseLatLon(np.array(row["geometry"].coords))
            folium.PolyLine(locations=revLocations, color='darkblue', weigth=15).add_to(folium_map)
    # station markers
    df = pd.read_csv('csv/yokosukastas.csv', usecols=['jpname', 'name', 'latitude', 'longitude'], encoding='utf-8')
    for i, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=PopupHorizontally(row['jpname']),
            max_width=500,
            icon=folium.Icon(color='darkblue', icon='check')
        ).add_to(yokosukaStas)
    yokosukaStas.add_to(folium_map)

    # create feature group
    keihintohokunegishiStas = FeatureGroup(name="京浜東北・根岸線", show=False)
    # polyline for railway track
    for i, row in df_gjs.iterrows():
        if (row["N02_003"] == "東北線" or row["N02_003"] == "根岸線") and row["N02_004"] == "東日本旅客鉄道":
            revLocations = ReverseLatLon(np.array(row["geometry"].coords))
            folium.PolyLine(locations=revLocations, color='blue', weigth=15).add_to(folium_map)
    # station markers
    df = pd.read_csv('csv/keihintohokunegishistas.csv', usecols=['jpname', 'name', 'latitude', 'longitude'], encoding='utf-8')
    for i, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=PopupHorizontally(row['jpname']),
            max_width=500,
            icon=folium.Icon(color='blue', icon='check')
        ).add_to(keihintohokunegishiStas)
    keihintohokunegishiStas.add_to(folium_map)

    # add layer
    LayerControl().add_to(folium_map)

    # save map
    folium_map.save('stationMap.html')


if __name__ == "__main__":
    main()
