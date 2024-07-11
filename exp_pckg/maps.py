# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 11:37:46 2024

@author: ArthurRodrigues
"""
from cities import cities_norm
from uf import ufs, regions_dict
from data import load_pkl, reverse_dict 
import geopandas as gpd, pandas as pd
import folium
from folium.plugins import TagFilterButton
from folium.map import Icon

from folium.plugins import MarkerCluster

from plotly.io import write_html
from plotly.io import  templates 
import plotly.graph_objects as go
templates.default = "plotly_dark"



def get_BR_map_all():
    
    BR = []
    dict_ = reverse_dict(regions_dict)
    for uf in ufs:
        
        st_boundary           = gpd.GeoDataFrame.from_file(f'C:/Users/ArthurRodrigues/Codes/Geojsons/{uf}.geojson')
        st_boundary['uf']     = uf
        st_boundary['region'] = dict_.get(uf,'NotInCountry')
        BR.append(st_boundary)
        
    BR = pd.concat(BR) 
    return BR

def get_BR_map():
    
    BR = []
    dict_ = reverse_dict(regions_dict)
    for uf in ufs:
        
        st                    = gpd.GeoDataFrame.from_file(f'C:/Users/ArthurRodrigues/Codes/Geojsons/{uf}.geojson')
        st_boundary           = st[st.geometry.geom_type=='Polygon']
        st_boundary['uf']     = uf
        st_boundary['region'] = dict_.get(uf,'NotInCountry')
        BR.append(st_boundary)
        
    BR = pd.concat(BR) 
    return BR
        
def wrangling_BR_map(brmap = 'BrasilMap'):
    
    map_          = load_pkl(name = brmap)
    cols          = map_.columns
    columnstodrop = list(cols[108:117]) + list(cols[123:134]) + list(cols[140:148]) + list(cols[11:42]) + list(cols[[2,5,63,135,45,46,49,51]]) + list(cols[68:100]) + list(cols[7:10]) + list(cols[58:152]) +['name:bn','name:en','name:es','surface','name:pnb','alt_name:ar','pop','source:name:oc','route','name:oc','fixme','note:ele','name:se','oneway','name:kk-Arab','border_type']
    new_map       = map_.drop(columns = columnstodrop)
    new_map       = new_map.fillna({'population':0})
    new_map       = new_map.astype({'population':'int'})
    return new_map
     
def plot_frame(dataframe,frames,count,key, plot = False):
    
    D = cities_norm(dataframe)
    mapp = D['br_map']
    group = dataframe.groupby(frames)[count].value_counts()
    group = group.to_frame()
    group.reset_index(inplace=True)
    G =  group.merge(mapp, on=key)
    G = gpd.GeoDataFrame(G)
    if plot: 
       G.plot(count) 
    G_dict = {
        'GeoDataFrame':G,
        'Geo_dict': G.__geo_interface__
        }   
    return G_dict

def plot_choropleth(geojson, locations, count, map_name='br_map_choropleth'):
    
    fig = go.Figure(go.Choroplethmapbox( geojson=geojson, locations=locations,        
    z=count,
                               colorscale="Viridis",
                               #range_color=(0, 12),
                               featureidkey='properties.cidades'))
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(mapbox_style="open-street-map",margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#000000') #open-street-map #carto-darkmatter
    fig.update_traces(marker_opacity=0.7, selector=dict(type='choropleth'))
    
   #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    write_html(fig,f'C:/Users/ArthurRodrigues/Codes/Expansion/Visuals/{map_name}.html')
    
def plot_TargetCities(targetMap,to_tag = ['cdaUpdated','UF','region','Is_LogIncluded'], name='targetCities'):
    unidades = load_pkl(name='unidades')
    cdas     = load_pkl(name='cdaMaps')
    M = folium.Map(location=[-19.9227318,-43.9450948], zoom_start=4, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(M)
    
    for i, r in targetMap.iterrows():
        lat = r["geometry"].y
        lon = r["geometry"].x
        folium.Marker(
            location=[lat, lon],
            tags=[r['cdaUpdated'],r['UF'],r['region'],r['Is_LogIncluded']],
            popup="name: {} <br> CDA: {}".format(r["cidades"], r["cdaUpdated"],r['População']),
        ).add_to(M)
    for tag in to_tag:
        TagFilterButton(list(set(targetMap[tag]))).add_to(M)
    
    for i, r in unidades.iterrows():
        lat = r["Latitude"]
        lon = r["Longitude"]
        folium.Marker(
            location=[lat, lon],
            popup="name: {} <br> Inaugurada: {}".format(r["Nome Fantasia"], r["Inaugurada"]),
            icon=Icon(color='red')
        ).add_to(marker_cluster)  
    for i, r in cdas.iterrows():
         lat = r["geometry"].y
         lon = r["geometry"].x
         folium.Marker(
             location=[lat, lon],
             popup="name: {} ".format(r["cidades"]),
             icon=Icon(color='black')

            ).add_to(M)    
        
        
        
        
    M.save(f'C:/Users/ArthurRodrigues/Codes/Expansion/Visuals/Maps/{name}.html')    
    

""" 
from plotly.io import write_html
from plotly.io import  templates 
templates.default = "plotly_dark"

import plotly.express as px


G = maps.plot_frame(result,['Is Won','Ano','Region'],'cidades','cidades')
gplot = G['GeoDataFrame']
import plotly.express as px

fig = px.choropleth_mapbox(gplot, geojson=br_map_dict, locations='cidades',        
color='count',
                           color_continuous_scale="Viridis",
                           #range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": 
                           -95.7129},
                           opacity=0.5,featureidkey='cidades',
                           labels={'population':'people rate'}
                          )
fig.update_geos(fitbounds='geojson', projection_type = 'orthographic')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
write_html(fig,'C:/Users/ArthurRodrigues/Codes/Expansion/Visuals/br_map_choropleth.html'
"""
"""
fig = go.Figure(go.Choroplethmapbox( geojson=br_map_dict, locations=gplot['cidades'],        
z=gplot['count'],
                           colorscale="Viridis",
                           #range_color=(0, 12),
                           featureidkey='properties.cidades'))
fig.update_geos(fitbounds='locations', visible=False)
fig.update_layout(mapbox_style="carto-darkmatter")
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
write_html(fig,'C:/Users/ArthurRodrigues/Codes/Expansion/Visuals/br_map_choropleth.html')
"""
"""
/*
This is an example Overpass query.
Try it out by pressing the Run button above!
You can find more examples with the Load tool.
*/
[out:json];
area["ISO3166-2"="BR-RO"][admin_level=4]->.minas_gerais;
(
  relation(area.minas_gerais)["boundary"="administrative"]["admin_level"="8"];
);
out geom;

"""
