# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 08:43:04 2024

@author: ArthurRodrigues
"""
from pandas import pivot_table
from tools import _acumulate
from data import load_pkl

def report_jr(dataframe):
    data = dataframe
    group1 = data[data['Modelo']!='Loja Parceira'].groupby([data['Ano'],data['Mês'],data['Drive']])['Frame'].value_counts()

    group2 = data[data['Is Loss']==0][data['Is Closed']==0][data['Deal']=='SQL'][data['Modelo']!='Loja Parceira']['UF'].value_counts()
    group3 = data[data['Is Loss']==0][data['Is Closed']==0][data['Deal']=='SQL'][data['Modelo']!='Loja Parceira']['Etapa'].value_counts()
    
    geral = pivot_table(dataframe, values='Opp Name', index=['Etapa'], columns=['Date[M]'], aggfunc='count',fill_value=0)
    geral = _acumulate(geral,[[0,1,2,3]])
    
    #report = pivot_table(dataframe, values='Opp Name', index=['Modelo','Etapa'], columns=['Date[M]'], aggfunc='count',fill_value=0)
    #report = _acumulate(report,[[0,1,2,3],[5,6,7,8],[11,12,13,14]])
    #report = report.stack()
    
    report2 = pivot_table(dataframe, values='Opp Name', index=['Vision','Etapa'], columns=['Is Loss','Date[M]'], aggfunc='count',fill_value=0)
    report2 = _acumulate(report2,[[0,1,],[3,4,5,6,],[8,9,10,11,12,],[14,15,16,17,],[19,20,21,22,23,]])
    report2 = report2.stack()
    
    ganhos_report = pivot_table(dataframe, values='Opp Name', index=['Modelo','Is Won'], columns=['Close[M]'], aggfunc='count',fill_value=0)
    ganhos_report = ganhos_report[ganhos_report.index.get_level_values('Is Won').isin([1])]
    
    
    G = {
        'Funil' : group1,
        'UF'    : group2,
        'Etapas': group3,
     #   'Resumo Geral Etapas': report,
        'Resumo Geral Etapas vs Visions':report2,
        'Resumo Geral Ganhos': ganhos_report,
        'Geral Etapas' : geral,
        }
    return G

def some_info(dataframe):
    data = dataframe
    # Where the Loss opp come from?
    where = data[data['Is Loss']==1]['Deal Stage Name'].value_counts()
    print(where)
    print('='*50)
    
    #[In/Out]bound
    howmany = data['Drive'].value_counts()
    print(howmany)
    print('='*50)
    
    #Wich guides we have?
    wich = data['Modelo'].value_counts()
    print(wich)
    print('='*50)
    
    #empty states
    emptyuf = data['UF'].value_counts()
    print(emptyuf['UF'])
    print('='*50)
    
    #distribuição etapas
    steps = data['Etapa'].value_counts()
    print(steps)
    print('='*50)

    G = {
        'Loss'       :where,
        'OutInBound' :howmany,
        'Guides'     :wich,
        'EmptyUF'    :emptyuf,
        'Stages'     :steps,
        }
    return G

results = load_pkl(name='opp')
R = report_jr(results)
rge = R['Resumo Geral Etapas vs Visions']
