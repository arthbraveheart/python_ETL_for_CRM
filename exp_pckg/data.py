# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:29:46 2024

@author: ArthurRodrigues
"""
import time
from pandas import read_csv, to_datetime, read_excel
from numpy  import array

def get_data():
    
    # import raw data from Sharp
    opp     = read_csv('C:/Users/ArthurRodrigues/Codes/Expansion/Report/OPP/oportunidades.csv')
    
    # by-hand index cols that are irrelevant
    listt   = list(range(29,59))+ list(range(60,69))+ list(range(79,86))+ list(range(87,128))+ list(range(130,132))+ list(range(133,140))+ list(range(169,172))+ list(range(176,178))+ [143,173]
    dropthis   = list(array(listt) - 1)
    
    # dropping them
    opp.drop(opp.columns[dropthis], axis=1, inplace=True)

    # turn into date type columns of interest   
    opp['Date Created'] = to_datetime(opp['Date Created'], format='%Y-%m-%d %H:%M:%S')
    opp['Close Date']   = to_datetime(opp['Close Date'], format='%Y-%m-%d %H:%M:%S')
    
    # creating columns with Date Created expanded
    opp['Close[M]']= opp['Close Date'].dt.to_period('M')
    dates          = opp['Date Created']
    opp['Date[M]'] = dates.dt.to_period('M')
    opp['Date']= dates.dt.date
    opp['Ano'] = dates.dt.year
    opp['Mês'] = dates.dt.month
    opp['Dia'] = dates.dt.day
    
    #rearrange the sequence of columns to fit on pipe flux
    pipe = opp.columns
    
    column_to_move = '[EXP] First Session'
    new_position   = 74

    # Get list of column names
    columns = list(pipe)

    # Remove the column from its current position
    columns.remove(column_to_move)

    # Insert the column at the new position
    columns.insert(new_position, column_to_move)
    
    # replace
    opp = opp[columns]
    
    #Data da Perda normalization
    
    opp['[EXP] Data da Perda'].replace({'Invalid date':time.strftime('%Y-%m-%d %H:%M:%S')},inplace=True)
    opp['[EXP] Data da Perda'].fillna(time.strftime('%Y-%m-%d %H:%M:%S'), inplace=True)
    opp['[EXP] Data da Perda']   = to_datetime(opp['[EXP] Data da Perda'], format='%Y-%m-%d %H:%M:%S')
    
    #LTV
    opp['ltvOpen'] =  opp['[EXP] Data da Perda'] - opp['Date Created']
    opp['ltvGanho'] = opp['Close Date']          - opp['Date Created']
    
    return opp 



def export(dataframe,name='opp'):
    path = 'C:/Users/ArthurRodrigues/Codes/Expansion/Report/OPP/'
    dataframe.to_csv(path + f'{name}.csv')
    print('\t#  Done\n\t# New Opp exported to ' + path + '\n\n')
    
    
def export_detail(dataframe, name='datail'):
    detail = dataframe[['Opp Name','SDR Responsável (Franquia)','Link']]
    path = 'C:/Users/ArthurRodrigues/Codes/Expansion/Report/'
    detail.to_excel(path + f'{name}.xlsx')
    print('\t#  Done\n\t# Opp exported to ' + path + '\n\n')    
    
def set_link(dataframe):
    url = 'https://abc-atacadobrasileirodaconstruos.marketingautomation.services/pipeline/sales?opportunity='
    dataframe['Link'] = [url + f'{i}' for i in dataframe.index] 
    return dataframe

def save_pkl(obj, path='C:/Users/ArthurRodrigues/Codes/Variables/', name='object'):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
        file.close()
       
def load_pkl(path='C:/Users/ArthurRodrigues/Codes/Variables/', name='object'):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        file.close()
    return data       

def reverse_dict(dict_): 
    dict_reverse = {}
    for key, value in dict_.items():
        for value_inside in value:
            dict_reverse.update({value_inside:key})
    return dict_reverse  

def get_citi():
    
    citi = read_excel('C:/Users/ArthurRodrigues/Codes/Expansion/Marketing/Cidades Expansão 2024.xlsx')
    save_pkl(citi,name='citi')
    return citi
    

