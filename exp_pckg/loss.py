# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:09:50 2024

@author: ArthurRodrigues

Here, we found two cores:
    - Create a column that define if the opp 'is loss'
    - Set the stage before the opp turned 'loss'
    
"""

def set_loss(dataframe):
    
    isloss = {'SB - Loss':1}
    dataframe['Is Loss'] = [isloss.get(i,0) for i in dataframe['Deal Stage Name']]
    
    return dataframe

