# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:45:22 2024

@author: ArthurRodrigues
"""
from data import load_pkl, save_pkl
from tools import str_norm_, extract_, replace_
from pandas import read_excel
import numpy as np

#opp    = load_pkl(name='opp')
citi   = load_pkl(name='cex')
br_map = load_pkl(name='BrasilNewMap') 

global citi_name
citi_name = 'cidades'

def cities_norm(opp):
    
    opp.reset_index(inplace=True)
    
    opp.rename(columns = {'Cidade de abertura da franquia': citi_name}, inplace=True)
    citi.rename(columns = {'Municípios': citi_name}, inplace=True)
    br_map.rename(columns = {'name': citi_name}, inplace=True)
    
    str_norm_(opp, citi_name)
    str_norm_(citi, citi_name)
    str_norm_(br_map, citi_name)
    
    opp[citi_name]  = opp[citi_name].str.strip(r'[/-^ ]')
    opp[citi_name]  = opp[citi_name].str.strip()
    
    
    
    opp['KEY'] = list(zip(opp['cidades'].apply(lambda x: x.replace('-',' ')),opp['UF']))
    citi['KEY'] = list(zip(citi['cidades'].apply(lambda x: x.replace('-',' ')),citi['UF']))
    br_map['KEY'] = list(zip(br_map['cidades'].apply(lambda x: x.replace('-',' ')),br_map['uf']))
    
    opp['KEY'] = opp['KEY'].astype('string')
    citi['KEY'] = citi['KEY'].astype('string')
    br_map['KEY'] = br_map['KEY'].astype('string')
    
    G = {
        'br_map' : br_map,
        'citi'   : citi,
        'opp'    : opp,
        }
    return G



def set_cities(opp):
    
    C = cities_norm(opp)
    manyCities = load_pkl(name='manyCities')
    cidades = br_map['cidades'].to_list() + citi['cidades'].to_list() + manyCities['cidades'].to_list()
    cidade  = '(.*?)'
 
    pat = '/ ' + cidade + ' -' + '|' + '/' + cidade + ' -' + '|'+ '/ ' + cidade + '-' + '|'+ '/' + cidade + '-'
    
    opp = C['opp']
    
    str_norm_(opp,'Opp Name')
    
    
    opp['citi_opname']  = extract_(opp[opp['cidades']=='nan'],'Opp Name',pat)[1]
    
    citi_opname         = opp[opp['citi_opname']!='nan'][['Opp ID','citi_opname']].dropna()
    citi_opname['citi'] = citi_opname['citi_opname'] 
    
    citi_concat         = citi_opname[['Opp ID','citi']] 
    citi_concat['citi'] = citi_concat['citi'].str.strip(r'[/-^ ]')
    citi_concat['citi'] = citi_concat['citi'].str.strip()
    
    citi_concat.drop_duplicates(subset=['Opp ID'], inplace=True)
    
    citi_concat.set_index('Opp ID', inplace=True)
    opp.set_index('Opp ID', inplace=True)
    
    opp = replace_(opp,citi_concat['citi'],'Opp ID','cidades')
 # --------------------------------------------------------------- explore 0   
    result         = opp 
    see_nan        = result[result['cidades']=='nan'][['Opp Name','cidades','UF']]
    pat_0          = '- ' + cidade + '$' + '|' + '- ' + cidade + ' -' + '|'+ '- ' + cidade + ' '
    extracted_0    = extract_(see_nan,'Opp Name',pat_0)
    extracted_0[1] = extracted_0[1].str.split('-', expand=True)[0]
    
    opp            = replace_(opp,extracted_0[1],'Opp ID','cidades')
 # --------------------------------------------------------------- explore 1  
    result         = opp 
    see_nan        = result[['Opp Name','cidades','UF']]
    pat_1          = cidade + ',' + '|' + cidade + ' \(' + '|'+  cidade + ' ,' + '|'+  cidade + ' ou ' + '|'+ cidade + '-' + '|'+ cidade + ' e'
    extracted_1    = extract_(see_nan,'cidades',pat_1)
    extracted_1[1] = extracted_1[1].str.split('-', expand=True)[0]
    
    opp            = replace_(opp,extracted_1[1],'Opp ID','cidades')
 # ---------------------------------------------------------------  explore 2 
    result         = opp 
    citinotfound   = result[result['UF']=='UF']['cidades'].str.split(r' ou ', expand=True)[0]
    citinotfound   = citinotfound.str.split(r' e ', expand=True)[0]
    citinotfound   = citinotfound.str.split(r'  e ', expand=True)[0]
    citinotfound   = citinotfound.str.split(r'\(', expand=True)[0]
    citinotfound   = citinotfound.str.split(r'(.*?)\(', expand=True)[0]
    citinotfound   = citinotfound.str.strip()
    
    opp            = replace_(opp,citinotfound,'Opp ID','cidades')
    opp['cidades'] = opp['cidades'].apply(lambda x: x.replace('-',' '))
    opp['cidades'] = opp['cidades'].apply(lambda x: x.split('/ ')[-1])
    opp['cidades'] = opp['cidades'].apply(lambda x: x.split(' ou ')[-1])
    opp['cidades'] = opp['cidades'].replace({'sp':'sao paulo','rj':'rio de janeiro','bh': 'belo horizonte','jf':'juiz de fora'})
    opp['cidades'] = opp['cidades'].replace({'':'notFound','nan':'notFound'})
# ---------------------------------------------------------------  explore 3 

    opp['citi']   = opp['cidades']
    
    ufs           = C['br_map']['uf'].to_list() + C['citi']['UF'].to_list() + manyCities['uf'].to_list()
    uf_dict       = {cidade:uf for uf,cidade in zip(ufs,cidades)} 
    target3       = opp[opp['UF']=='UF'][['UF','citi']]
    target3['UF'] = [uf_dict.get(cidade['citi'], 'UF') for i,cidade in target3.iterrows()] 
    target_dict   = dict(target3['UF'].dropna())
    opp['UF']     = [target_dict.get(i, cidade['UF']) for i,cidade in opp.iterrows()]
    
    
    return opp
    
    

def cities_merge(opp, on=citi_name):
    opp_citi       = opp.merge(citi, on=on)
    opp_brmap      = opp.merge(br_map, on=on)
    citi_brmap     = citi.merge(br_map, on=on) 
    opp_citi_brmap = opp_citi.merge(br_map, on=on)
    
    G = {
        'OC':opp_citi,
        'OB':opp_brmap,
        'CB': citi_brmap,
        'OCB':opp_citi_brmap,
        }
    return G



def cities_MKT(dataframe):
    
    guides            = load_pkl(name='unidades') 
    guides_desligadas = load_pkl(name='unidadesDesligadas') 
    target_per_region = load_pkl(name='target_MKT_cidades') #irwa
    atendidas         = load_pkl(name='atendidas')
    N                 = cities_norm(dataframe)
    cidades           = N['citi']
    #br_map            = N['br_map']
    str_norm_(cidades,'Região')
    str_norm_(cidades,'Cidade Polo')
    str_norm_(cidades,'CD/CDA')
    
    guides_key           = set(list(zip(guides['cidades'].apply(lambda x: x.replace('-',' ')),guides['UF'])))
    guidesDesligadas_key = set(list(zip(guides_desligadas['cidades'].apply(lambda x: x.replace('-',' ')),guides_desligadas['UF'])))
    dontHaveNewGuide     = set(guidesDesligadas_key) - set(guides_key)
    NotInLog             = list(set(cidades['KEY'])-set(atendidas['KEY']))
    #NotInExp            = list(set(atendidas['KEY'])-set(cidades['KEY'])) 
    excluded = (cidades.set_index('KEY'))\
                   .loc[NotInLog,:]
    atendidas_cidades     = atendidas.merge(cidades, on='KEY')
    atendidas_cidadepolo  = atendidas_cidades['Cidade Polo'].unique()
    atendidas_region      = atendidas_cidades['Região'].unique()
    
    update_dict = {upkey:1 for upkey in atendidas_cidades['KEY']}
    
    excluded_polo_dict = dict(excluded['Cidade Polo'])
    included_keys = [key for key in excluded_polo_dict.keys() if excluded_polo_dict[key] in atendidas_cidadepolo]
    
    is_polo_included = {inkey:1 for inkey in included_keys}
    is_polo_included.update(update_dict)
    cidades['Is_PoloIncluded'] = [is_polo_included.get(key,0) for key in cidades['KEY']]

    #included_region = cidades.loc[included_keys,:]
    
    included_keys   = atendidas_cidades['KEY']
    is_log_included = {inkey:1 for inkey in included_keys}
    cidades['Is_LogIncluded'] = [is_log_included.get(key,0) for key in cidades['KEY']]
    
        
    
    excluded_region_dict = dict(excluded['Região'])
    included_keys = [key for key in excluded_region_dict.keys() if excluded_region_dict[key] in atendidas_region]
    
    is_region_included = {inkey:1 for inkey in included_keys}
    is_region_included.update(update_dict)
    cidades['Is_RegionIncluded'] = [is_region_included.get(key,0) for key in cidades['KEY']]
    
    
    is_guide_included = {inkey:1 for inkey in guides_key}
    cidades['haveGuide'] = [is_guide_included.get(key,0) for key in cidades['KEY']]
    
    is_guide_included = {inkey:1 for inkey in guidesDesligadas_key}
    cidades['guidesDesligadas'] = [is_guide_included.get(key,0) for key in cidades['KEY']]
    
    is_guide_included = {inkey:1 for inkey in dontHaveNewGuide}
    cidades['dontHaveNewGuide'] = [is_guide_included.get(key,0) for key in cidades['KEY']]

    cidades['haveCDA'] = 1*cidades['CD/CDA'].str.contains('(cda)|(cdm)') 
    cidades['cdCity']  = cidades['CD/CDA'].apply(lambda x : x.split(' ',2)[-1])
    atendidas['cdCity']  = atendidas['CDA'].apply(lambda x : x.split(' ',2)[-1])
    str_norm_(cidades,'cdCity')
    cidades['Is_cdF']  = 1*cidades['CD/CDA'].str.contains('\.')
    
    atendidas_cdKey = set(zip(atendidas['KEY'],atendidas['cdCity']))
    cidades_cdKey = set(zip(cidades['KEY'],cidades['cdCity']))
    cda_toUpdateAll = atendidas_cdKey - cidades_cdKey
    
    cidades['cdaUpdated'] = cidades['CD/CDA']
    
    atendidas['cdKey'] = list(zip(atendidas['KEY'],atendidas['cdCity']))
    cidades['cdKey']   = list(zip(cidades['KEY'],cidades['cdCity']))
    
    cda_wrong_catALL = cidades[['KEY','CD/CDA']]\
                       .merge(\
                       atendidas.query("cdKey in @cda_toUpdateAll")[['KEY','CDA']], on='KEY')
    
    cidades            = replace_(cidades.set_index('KEY'),cda_wrong_catALL.set_index('KEY')['CDA'],'KEY','cdaUpdated')
    cidades['Is_cdFupdated']  = 1*cidades['cdaUpdated'].str.contains('\.')
    
    set_dtypes = {
        'cdCity':'string',
        'cdaUpdated':'string',
        'cdKey':'string',
        'Is_cdFupdated':np.int64,
        'Is_Target':np.int64,
        }
    cidades = cidades.astype(set_dtypes)
    
    Citi_MKT = {
        'Target_per_Region': target_per_region,
        'cidades': cidades,
        }
    
    return Citi_MKT
    
def set_targetMKT():
    target = read_excel('C:/Users/ArthurRodrigues/Codes/Expansion/Report/OPP/CExUpdatedTrue.xlsx', sheet_name='TARGET')    
    save_pkl(target, name='targetMKT')
    return target
    








