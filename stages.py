# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:22:25 2024

@author: ArthurRodrigues
"""
from loss import set_loss 

def stage_date_in(dataframe):
    cols = dataframe.columns
    pipe = dataframe[cols[54:72]]
    pipe = pipe.fillna('2017-01-01 00:00:00')
    return pipe

def stage_before_loss(dataframe):
    dataframe.set_index('Opp ID',inplace=True)
    dataframe   = set_loss(dataframe)
    is_loss     = dataframe[dataframe['Is Loss'] == 1]
    pipe_loss   = stage_date_in(is_loss)
    before_loss = dict(pipe_loss.idxmax(axis=1))
    return before_loss

def set_stages_before_loss(dataframe,before_loss_dict):
    is_loss                    = dataframe[dataframe['Is Loss'] == 1]
    is_loss['Deal Stage Name'] = [before_loss_dict.get(i,j['Deal Stage Name']) for i,j in is_loss.iterrows()]
    dataframe['Deal Stage Name'][dataframe['Is Loss'] == 1] = is_loss['Deal Stage Name']
    return dataframe

