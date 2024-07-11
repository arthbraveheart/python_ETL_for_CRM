# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:45:22 2024

@author: ArthurRodrigues
"""
from unidecode import unidecode
from pandas import concat
from data import load_pkl

opp    = load_pkl(name='opp')
citi   = load_pkl(name='citi')
br_map = load_pkl(name='BrasilNewMap') 

global citi_name
citi_name = 'cidades'

def cities_norm():
    
    opp.reset_index(inplace=True)
    
    opp.rename(columns = {'Cidade de abertura da franquia': citi_name}, inplace=True)
    citi.rename(columns = {'Municípios': citi_name}, inplace=True)
    br_map.rename(columns = {'name': citi_name}, inplace=True)
    
    opp[citi_name] = opp[citi_name].astype('str')
    citi[citi_name] = citi[citi_name].astype('str')
    br_map[citi_name] = br_map[citi_name].astype('str')
    
    opp[citi_name] = opp[citi_name].str.lower()
    citi[citi_name] = citi[citi_name].str.lower()
    br_map[citi_name] = br_map[citi_name].str.lower()
    
    opp[citi_name] = opp[citi_name].str.strip()
    citi[citi_name] = citi[citi_name].str.strip()
    br_map[citi_name] = br_map[citi_name].str.strip()
    
    opp[citi_name] = opp[citi_name].apply(lambda x: unidecode(x))
    citi[citi_name] = citi[citi_name].apply(lambda x: unidecode(x))
    br_map[citi_name] = br_map[citi_name].apply(lambda x: unidecode(x))
    
    opp[citi_name]  = opp[citi_name].str.strip(r'[/-^ ]')
    opp[citi_name]  = opp[citi_name].str.strip()
    
    G = {
        'br_map' : br_map,
        'citi'   : citi,
        'opp'    : opp,
        }
    return G



def set_cities():
    import regex as re
    C = cities_norm()
    cidades = C['br_map']['cidades'].to_list() + C['citi']['cidades'].to_list()
    pat  = ''
    pat1 = ''
    for cidade in cidades[:-1]:
        pat += ' ' + cidade + ' ' + '|' + '^' + cidade + '|' + cidade + '$' + '|'+'/ ' + cidade + ' -' + '|' + '/' + cidade + ' -' + '|'+ '/ ' + cidade + '-' + '|'+ '/' + cidade + '-' + '|'                
        pat1+= cidade + '|' + ' ' + cidade + ' ' + '|' + '^' + cidade + '|' + cidade + '$' + '|'+'/ ' + cidade + ' -' + '|' + '/' + cidade + ' -' + '|'+ '/ ' + cidade + '-' + '|'+ '/' + cidade + '-' + '|'                

    pat  +=cidades[-1]
    pat1 +=cidades[-1]
    
    opp = C['opp']
    
    opp['Opp Name'] = opp['Opp Name'].astype('str')
    opp['Opp Name'] = opp['Opp Name'].str.lower()
    opp['Opp Name'] = opp['Opp Name'].apply(lambda x: unidecode(x))
    
    target1 = opp['Opp Name']#opp[opp['cidades']=='nan']['Opp Name']
    target2 = opp['cidades'] #opp[opp['cidades']=='nan']['cidades'] #just to fix any error
    
    opp['citi_opname'] = target1.str.extract(fr'({pat})', flags=re.IGNORECASE)
    opp['citi_cidades'] = target2.str.extract(fr'({pat1})', flags=re.IGNORECASE)

    citi_opname = opp[opp['citi_opname']!='nan'][['Opp ID','citi_opname']].dropna()
    citi_cidades = opp[opp['citi_cidades']!='nan'][['Opp ID','citi_cidades']].dropna()
    
    citi_opname['citi'] = citi_opname['citi_opname']
    citi_cidades['citi'] = citi_cidades['citi_cidades']
    
    citi_concat = concat([citi_cidades[['Opp ID','citi']] , citi_opname[['Opp ID','citi']]], axis=0)
    citi_concat['citi'] = citi_concat['citi'].str.strip(r'[/-^ ]')
    citi_concat['citi'] = citi_concat['citi'].str.strip()
    
    
    citi_concat.drop_duplicates(subset=['Opp ID'], inplace=True)
    
    citi_concat.set_index('Opp ID', inplace=True)
    opp.set_index('Opp ID', inplace=True)
    
    citi_dict = dict(citi_concat['citi'])
    
    opp['citi'] = [citi_dict.get(i,'NotFound') for i in opp.index.values]
    
    ufs       = C['br_map']['uf'].to_list() + C['citi']['UF'].to_list()
    uf_dict   = {cidade:uf for uf,cidade in zip(ufs,cidades)}
    target3   = opp[opp['UF']=='UF'][['UF','citi']]
    target3['UF']       = [uf_dict.get(cidade,'UF') for cidade in target3['citi'].to_list()]
    opp[opp['UF']=='UF']['UF'] = target3['UF']
    
    return opp
    
    
    

def cities_merge():
    opp_citi   = opp.merge(citi, on=citi_name)
    opp_brmap  = opp.merge(br_map, on=citi_name)
    citi_brmap = citi.merge(br_map, on=citi_name) 
    opp_citi_brmap = opp_citi.merge(br_map, on=citi_name)
    
    G = {
        'OC':opp_citi,
        'OB':opp_brmap,
        'CB': citi_brmap,
        'OCB':opp_citi_brmap,
        }
    return G


