# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:39:17 2024

@author: ArthurRodrigues
"""
from pandas import concat
from data import reverse_dict

uf_dict     = {
                        'MG':['MG','Minas Gerais','mg','minas gerais','MINAS GERAIS','Minas','Minas gerais','Mg'],
                        'SP':['SP','São Paulo','sp','Sao Paulo','sao paulo','Sp','SÃO PAULO','SAO PAULO'],
                        'RJ':['RJ','rj','Rio','Rio de Janeiro','rio de janeiro','Rio de janeiro','Rj','RIO DE JANEIRO'],
                        'ES':['ES','Espírito Santo','es','Espirito santo','Espirito Santo','espirito santo','espírito santo','Es','ESPÍRITO SANTO','ESPIRITO SANTO'],
                        'PR':['PR','Paraná','Parana','pr','parana','Pr','PARANÁ','PARANA'],
                        'SC':['SC','Santa Catarina','sc','Santa catarina','santa catarina','Sc','SANTA CATARINA'],
                        'RS':['RS','Rio Grande do Sul','Rio grande do sul','rio grande do sul','rs','Rs','RIO GRANDE DO SUL'],
                        'DF':['DF','Distrito Federal','Distrito federal','distrito federal','df','Df','DISTRITO FEDERAL'],
                        'GO':['GO','Goiás','Goias','Go','GOIÁS','GOIAS'],
                        'MS':['MS','Mato Grosso do Sul','ms','Mato grosso do sul','Ms','MATO GROSSO DO SUL'],
                        'MT':['MT','Mato Grosso','Mato grosso','mt','mato grosso','Mt','MATO GROSSO'],
                        'BA':['BA','Bahia','bahia','ba','Ba','BAHIA'],
                        'AL':['AL','Alagoas','alagoas','al','Al','ALAGOAS'],
                        'SE':['SE','Sergipe','sergipe','se','Se','SERGIPE'],
                        'PB':['PB','Paraíba','Paraiba','paraiba','pb','paraíba','Pb','PARAÍBA','PARAIBA'],
                        'PE':['PE','Pernambuco','pernambuco','pe','Pe','PERNAMBUCO'],
                        'CE':['CE','Ceará','Ceara','ce','ceara','ceará','Ce','CEARÁ','CEARA'],
                        'MA':['MA','Maranhão','Maranhao','maranhão','maranhao','ma','Ma','MARANHÃO','MARANHAO'],
                        'PA':['PA','Pará','Para','pará','para','pa','Pa','PARÁ','PARA'],
                        'AM':['AM','Amazonas','amazonas','am','Am','AMAZONAS'],
                        'RO':['RO','Rondônia','Rondonia','rondônia','rondonia','ro','Ro','RONDÔNIA','RONDONIA'],
                        'RR':['RR','Roraima','roraima','rr','Rr','RORAIMA'],
                        'TO':['TO','Tocantins','tocantins','to','To','TOCANTINS'],
                        'PI':['PI','Piauí','piauí','piaui','pi','Pi','PIAUÍ','PIAUI'],
                        'AP':['AP','Amapá','Amapa','amapá','amapa','ap','Ap','AMAPÁ','AMAPA'],
                        'AC':['AC','Acre','acre','ac','Ac','ACRE'],
                        'RN':['RN','Rio Grande do Norte','Rio grande do norte','rio grande do norte','rn','Rn','RIO GRANDE DO NORTE'],
                        }

ufs          = list(uf_dict.keys())

regions_dict = {
    'Sudeste'       :['MG','SP','RJ','ES'],
    'Sul'           :['PR','SC','RS'],
    'Centro-Oeste'  :['DF','GO','MT','MS'],
    'Norte'         :['AM','PA','RR','RO','AC','AP','TO'],
    'Nordeste'      :['BA','RN','AL','SE','PE','PB','PI','MA','CE'],
    }

to_replace = {'cda aparecida de goiania': 'cda go aparecida de goiania',
 'cda cariacica':'cda es cariacica',
 'cda divinopolis':'cda mg divinopolis',
 'cda duque de caxias':'cda rj duque de caxias',
 'cda guarulhos':'cda sp guarulhos',
 'cda ipatinga':'cda mg ipatinga',
 'cda jacarei':'cda sp jacarei',
 'cda marilia':'cda sp marilia',
 'cda montes claros':'cda mg montes claros',
 'cda muriae':'cda mg muriae',
 'cda nova lima':'cda mg nova lima',
 'cda resende':'cda rj resende',
 'cda ribeirao preto':'cda sp ribeirao preto',
 'cda sao jose dos pinhais':'cda pr sao jose dos pinhais',
 'cda sumare': 'cda sp sumare',
 'cda uberlandia':'cda mg uberlandia',
 'cda varginha':'cda mg varginha'
 }

def set_uf(dataframe):
    
    UF = []
    for uf in ufs:
        see = [dataframe['Opp Name'].str.contains(fr'{i}/|{i} /|^{i} -| {i} |- {i}$|-{i}$| {i}$|\({i}\)|/{i}$|/{i} ') for i in uf_dict[uf]]
        see.append(dataframe['Estado de abertura da franquia'] == uf)
        see = concat(see)
        see = see.to_frame()
        see_t = see[see[0] == True]
        see_t = see_t.reset_index()
        see_t = see_t.drop_duplicates('Opp ID')
        see_t[0] = uf
        see_t.set_index('Opp ID', inplace=True)
        UF.append(see_t)
    UF = concat(UF) 
    UF.reset_index(inplace=True)
    UF = UF.drop_duplicates('Opp ID')
 
    UF = UF.set_index('Opp ID')
 
    UF_dict = dict(UF[0])
    key     = dataframe.index
    dataframe['UF'] = [UF_dict.get(i,'UF') for i in key] 
    
    return dataframe
        
def set_region(dataframe):
    dict_               = reverse_dict(regions_dict)
    UF                  = dataframe['UF']
    dataframe['Region'] = [dict_.get(uf,'NotInCountry') for uf in UF ]
    return dataframe    
 


