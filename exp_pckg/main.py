# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:16:06 2024

@author: ArthurRodrigues
"""

import data as d ,loss as l , stages as st, outbound as out, guideshop as guide, uf,etapas as e, canais as c, cities as ct, campaigns as camp, tools as t
import time
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

def magic():
    data     = d.get_data()
    data     = l.set_loss(data)
    bfl_dict = st.stage_before_loss(data)
    data     = st.set_stages_before_loss(data,bfl_dict)
    data     = camp.set_campaign(data)
    data     = out.set_drive(data)
    data     = guide.set_guide(data)
    data     = guide.set_product(data)
    data     = uf.set_uf(data)
    data     = ct.set_cities(data)
    data     = uf.set_region(data)
    data     = e.set_etapa(data)
    data     = e.set_util(data)
    data     = c.set_groups(data)
    data     = d.set_link(data)
    data     = t.objToStr(data)
    d.export(data, name='opp')
    d.save_pkl(data,name='opp')
    return data

def routine():
    data      = magic()
    citi      = d.load_pkl(name='cex')#ct.cities_MKT(data) #d.load_pkl(name='citi') #ct.cities_MKT(data)
    campanhas = camp._campaignDF(data)
    d.export(campanhas, name='campanhas')
    d.save_pkl(campanhas,name='campanhas')
    #citi_camp = campanhas.merge(citi['cidades'], on='KEY')#campanhas.merge(citi, on='KEY')#citi['cidades'], on='KEY')
    br_map    = ct.cities_norm(data)['br_map']  #d.load_pkl(name='BrasilNewMap')

    M         = ct.cities_merge(data, on='KEY')
    
    G = {
        'br_map'    : br_map,
        'citi'      : citi,
        'opp'       : data,
        'campanhas' : campanhas,
        #'citi_camp' : citi_camp,
        'merges'    : M
        }
    return G

def rawMagic(dataframe):
    data     = dataframe.copy()
    data     = l.set_loss(data)
    bfl_dict = st.stage_before_loss(data)
    data     = st.set_stages_before_loss(data,bfl_dict)
    data     = camp.set_campaign(data)
    data     = out.set_drive(data)
    data     = guide.set_guide(data)
    data     = uf.set_uf(data)
    #data     = ct.set_cities(data)
    #data     = uf.set_region(data)
    data     = e.set_etapa(data)
    data     = e.set_util(data)
    #data     = c.set_groups(data)
    data     = d.set_link(data)
    return data

def updateDB(dataframe):
    import sqlalchemy as sql

    connDict = {
        'USER':'postgres',
        'PASSWORD':'123456',
        'HOST': 'localhost',
        'DATABASE':'Oportunidades'
        }
    #conn_string = f"postgresql+psycopg2://{connDict['USER']}:{connDict['PASSWORD']}@{connDict['HOST']}/{connDict['DATABASE']}"


    def connection(dictConn = connDict): 
        conn_string = f"postgresql+psycopg2://{connDict['USER']}:{connDict['PASSWORD']}@{connDict['HOST']}/{connDict['DATABASE']}"
        db = sql.create_engine(conn_string ) 
        conn = db.connect()
        return conn 


    tableName=connDict['DATABASE'] 
    dataframe['VERSION'] = time.strftime("%d-%m-%Y")
    dataframe = t.setDtypes(dataframe)
    dataframe.to_sql(name=tableName,con=connection(), if_exists='append', index=False)
    connection().commit()
        
        

