# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:21:23 2024

@author: ArthurRodrigues
"""

import pandas as pd
from main import rawMagic


imports = ['02-05-24','03-05-24','06-05-24','30-04-24','26-04-24','25-04-24']
Period = []
for dates in imports:
    op = pd.read_csv(f'C:/Users/ArthurRodrigues/Downloads/opp{dates}.csv')
    Period.append(op)
    
opConcat = pd.concat(Period)
opens = opConcat.query(" `Is Closed`==0 ")

opConcatMagic = rawMagic(opens)    
