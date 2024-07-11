# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:48:50 2024

@author: ArthurRodrigues
"""
from pandas import concat
from tools import extract_


def set_campaign(dataframe):
    see_ex = extract_(dataframe,'Campaign Name','\[(.*?)\]')
    dataframe['Campaign Name Resume'] = see_ex[1]
    return dataframe

def _campaignDF(dataframe):
    
    result_frames = dataframe[['KEY','Is Won','Is Closed','Canal','Campaign Name', 'Campaign Name Resume','Como soube que a ABC é uma franquia?', 'Como Soube Resumo','Persona','Motivo Perda [EXP]', 'Close Date', 'Date','Ano','Mês','Dia','Is Loss','Drive','Modelo','UF','cidades','Region','Etapa','Deal','Frame','Área','Grupo','[EXP] Data da Perda']]
    origem_lead = dataframe['[EXP] First Session'].dropna()
    origem_split = origem_lead.str.split(r'\&', expand=True)
    cols = ['source','medium','campaign','term','content','date','landingPage']
    for i,j in enumerate(cols):
        origem_split[j] = origem_split[i].str.split('=', expand=True)[1]
    campaign_split = origem_split['campaign'].str.split('-', expand=True)
    origem_split_campaignExpand = concat([origem_split,campaign_split], axis=1).iloc[:,13:] 
    campaignDF = concat([result_frames,origem_split_campaignExpand], axis=1)
    return campaignDF
    