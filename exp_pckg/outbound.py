# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 07:45:22 2024

@author: ArthurRodrigues
"""

outbound_canal_dict = {
    'Outbound - Ativa'                 :'Outbound',
    'Outbound - Store in Store'        :'Outbound',
    'Outbound - Lojas Parceiras'       :'Outbound',
    'Outbound - Store in Store - Ativa':'Outbound',
    'Outbound - Indicação Equipe'      :'Outbound',
    'Evento/Feira'                     :'Outbound',
    'Feira ABF Rio 2019'               :'Outbound',
    'Feicon 2024'                      :'Outbound',
    'Ativa - Júnior'                   :'Outbound',
    'Ativa - Pólen'                    :'Outbound',
    'Ativa - Mauro'                    :'Outbound',
    'Ativa - Hugo'                     :'Outbound',
    'Ativa - Gustavo'                  :'Outbound',
    'Ativa - Varredura praças google'  :'Outbound',
    'Mala Direta'                      :'Outbound'
    }

out_dict = {True : 'Outbound'}


def set_drive(dataframe):
    data_frame  = dataframe[['Opp Name','Canal']]
    
    dataframe['Drive'] = [outbound_canal_dict.get(j['Canal'],j['Opp Name']) for i,j in data_frame.iterrows()]
    out_contains = dataframe['Drive'].str.contains(r'OUTBOUND|Outbound|\[OUT\]|\[OUTB\]|OUTBUND|OUBOUND')
    dataframe['Drive'] = [out_dict.get(i,'Inbound') for i in out_contains]
    
    return dataframe



