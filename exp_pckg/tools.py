# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:02:43 2024

@author: ArthurRodrigues
"""
from unidecode import unidecode
import regex as re
import numpy as np
from plotly.io import write_html
from plotly.io import  templates
from geopandas import GeoDataFrame 
import plotly.graph_objects as go
import plotly.express as px
templates.default = "plotly_dark"


def replace_(dataframe, series, column_key, column_target):
    if dataframe.index.name != series.index.name:
        try:
            dataframe.set_index(column_key, inplace=True)
        except:
            print('Already on DataFrame Index')
    else: 
        target      = series.dropna().astype('string')
        target      = target.str.strip()
        target_dict = dict(target)
        
        to_replace = dataframe[column_target]
        to_replace = [target_dict.get(i,j) for i,j in zip(to_replace.index.values, to_replace )]
        dataframe[column_target] = to_replace
    return dataframe


def str_norm_(dataframe,column_name):
    to_norm = dataframe[column_name]
    to_norm = to_norm.astype('str')
    to_norm = to_norm.str.lower()
    to_norm = to_norm.str.strip()
    to_norm = to_norm.apply(lambda x: unidecode(x))
    dataframe[column_name] = to_norm

        
def extract_(dataframe, column_name, pattern):
    target = dataframe[column_name]
    extracted = target.str.extract(fr'({pattern})', flags=re.IGNORECASE)
    return extracted


def _acumulate(dataframe,levels):
   for level in levels:
        n     = len(level) + level[0] +1
        
        for i in level:
            dataframe.iloc[i]= (dataframe.iloc[i:n]).sum()
            
   return dataframe    


def setDTypes(dataframe,dict_):
    dataframe = dataframe.astype(dict_)
    

def _plotBox(dataframe=None,to_group=None,to_count=None,to_see=None,color=None,log=True,name=None):
    canal = ((dataframe.groupby(to_group)[to_count].value_counts()).to_frame()).reset_index()
    fig2 = px.box(canal, y=np.log(canal['count'].values), x=to_see, color=color, points='all')
    write_html(fig2, f'C:/Users/ArthurRodrigues/Codes/Expansion/Visuals/box_chart{name}.html')
 
    
def _plotGpdChoropleth(dataframe, to_see, catch, to_count):
    choroplethMap = (((dataframe.query(f"{to_see} == @catch")).groupby(['KEY','geometry'])[to_count].value_counts()).to_frame()).reset_index()
    choroplethMap = GeoDataFrame(choroplethMap)
    choroplethMap['countLog'] = choroplethMap['count'].apply(lambda x: np.log(x))
    choroplethMap.plot('countLog')

    
def keyMaker(dataframe,colKeys,colKeyName):
    toMake = dataframe[colKeys].apply(lambda x: x.replace('-',' '))
    dataframe[colKeyName] = [tuple(r[:]) for i,r in toMake.iterrows()]

    
def objToStr(dataframe):    
    trues     = [dataframe.dtypes == 'O']
    dataframe = dataframe.astype({col: 'string' for col in trues[0][trues[0] == True].index})
    return dataframe
    
def setDtypes(dataframe):
    dataframe = objToStr(dataframe)
    dataframe = dataframe.set_index('Close[M]').to_timestamp().reset_index()
    dataframe = dataframe.set_index('Date[M]').to_timestamp().reset_index()

    return dataframe

    
