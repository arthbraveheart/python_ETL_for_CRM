# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 11:30:12 2024

@author: ArthurRodrigues

guideshop = {
    LP : { TÍTULO, CANAL}
    SIS: {TÍTULO, CANAL, Produto de Interesse}
    Franquia : Demais
    
    }
"""

from numpy import float64

guide_canal_dict = {
    
    'Outbound - Lojas Parceiras'       :'Loja Parceira',
    'Outbound - Store in Store'        :'Store in Store',
    'Outbound - Store in Store - Ativa':'Store in Store',
    
    }

guide_dict = {
    'SIS':{True : 'Store in Store'},
    'LP' :{True : 'Loja Parceira'}
              }

def set_guide(dataframe):
    data_frame  = dataframe[['Opp Name','Canal']]
    
    guide_contains      = { 'LP'  : data_frame['Opp Name'].str.contains(r'- LP -|LP\]|LP \]|-LP'),#|LP\]|LP \]| -LP| \[LP\]'),
                           
                            'SIS' : data_frame['Opp Name'].str.contains(r'SIS\]| - SIS|SIS \]|\[SIS -| SIS'),
                                                       }
    
    dataframe['Modelo'] = [guide_dict['LP'].get(i,'Franquia') for i in guide_contains['LP']]
    
    set_sis = (dataframe[dataframe['Modelo']=='Franquia'].index).to_list()
    dataframe.loc[set_sis,'Modelo'] = [guide_dict['SIS'].get(i,'Franquia') for i in guide_contains['SIS'][set_sis]]
    
    set_chanel = (dataframe[dataframe['Modelo']=='Franquia'].index).to_list()
    
    data_iter = data_frame.loc[set_chanel,:]
    dataframe.loc[set_chanel,'Modelo'] = [guide_canal_dict.get(j['Canal'],'Franquia') for i,j in data_iter.iterrows()]
    
    return dataframe


def set_product(dataframe):
    dataframe.loc[:,'Produto'] = dataframe.loc[:,'[EXP] Produto de Interesse'].fillna('0').apply(lambda x : float64(x.split(' - ')[-1].replace('R$','')))
    return dataframe