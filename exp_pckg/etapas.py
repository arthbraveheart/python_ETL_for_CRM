# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:47:11 2024

@author: ArthurRodrigues


"""

etapas_dict={'MQL - (Inbound) Novos Candidatos MQL':        ['0 - MQL','MQL','MQL'],
             'MQL - Tentativa de contato':                  ['0 - MQL','MQL','MQL'],
             'MQL - (Prioritários) Qualificação':           ['0 - MQL','MQL','MQL'],
             'MQL - Comitê (Pipeline)':                     ['0 - MQL','MQL','MQL'],
             '(Outbound) Prioritários':                     ['0 - MQL','MQL','MQL'],
             '(Outbound) Comitê':                           ['0 - MQL','MQL','MQL'],
             '(Outbound) Backlog':                          ['0 - MQL','MQL','MQL'],
             'Outbound agendamento':                        ['0 - MQL','MQL','MQL'],
             'Outbound Generalista A':                      ['0 - MQL','MQL','MQL'],
             'Outbound Especialistas':                      ['0 - MQL','MQL','MQL'],
             'SQL - !Aprovados':                            ['1 - Apresentação','SQL','SQL'],
             'SQL - Apresentação':                          ['1 - Apresentação','SQL','SQL'],
             'SQL - Apresentação reagendada':               ['1 - Apresentação','SQL','SQL'],
             'SQL - Apresentação feita':                    ['1 - Apresentação','SQL','SQL'],
             'SQL - !Comitê SQL':                           ['1 - Apresentação','SQL','SQL'],
             'SQL - Stand By':                              ['1 - Apresentação','SQL','SQL'],
             'SQL - Estudo de Viabilidade':                 ['2 - Estudo de Viabilidade','SQL','SQL-Jr'],
             'SQL - FUP':                                   ['3 - Desenvolvimento','SQL','SQL-Jr'],
             'SQL - Alinhamento Final e Teste de Perfil':   ['3 - Desenvolvimento','SQL','SQL-Jr'],
             'SQL - Franqueado + Estudo':                   ['3 - Desenvolvimento','SQL','SQL-Jr'],
             'SQL - Comitê (final)':                        ['3 - Desenvolvimento','SQL','SQL-Jr'],
             'SQL - Pré-contrato enviado':                  ['4 - Final','SQL','SQL-Jr'],
             'SQL - LP - Aguardando Documentação':          ['LP - Final','SQL','SQL' ],
             'SQL - LP - Pré-contrato enviado':             ['LP - Final','SQL','SQL']

             }


mqlutil_dict = {
    'Duplicado - Preenchimento formulário':'Inutil',
    'Duplicado':'Inutil',
    'Falta de retorno resposta ou contato':'Inutil',
    'Número / Email inválido':'Inutil',
    'Engano':'Inutil',
    'Fornecedor':'Inutil',
    'Teste':'Inutil',
    'Duplicado - SharpSpring':'Inutil',
    'Cliente - Venda de produto':'Inutil',
    'Falta de Contato':'Inutil'
      }

def set_etapa(dataframe):
    
    isstage = etapas_dict
    dataframe['Deal Stage Name'] = dataframe['Deal Stage Name'].str.strip() 
    dataframe['Deal Stage Name'].replace({'SQL - Comitê SQL':'SQL - !Comitê SQL', 'SQL - Aprovados':'SQL - !Aprovados'}, inplace=True)
    dataframe['Etapa'] = [isstage.get(i,'Nova Etapa')[0] for i in dataframe['Deal Stage Name']]
    dataframe['Deal']  = [isstage.get(i,'Nova Etapa')[1] for i in dataframe['Deal Stage Name']]
    dataframe['Frame'] = [isstage.get(i,'Nova Etapa')[2] for i in dataframe['Deal Stage Name']]
    return dataframe



def set_util(dataframe):
    notutil = mqlutil_dict
    dataframe['Utils'] = [notutil.get(i,'Util') for i in dataframe['Motivo Perda [EXP]']]
    return dataframe
    
    
    
    
    