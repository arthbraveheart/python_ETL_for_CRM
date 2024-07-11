# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 01:06:16 2024

@author: ArthurRodrigues
"""



"""

cda_update = set(atendidas['cdCity'])&set(cidades.query("Is_cdF==1")['cdCity'])
see = atendidas.query("cdCity in @cda_dontCEx")
see['cdCity'].value_counts()
see_keys = atendidas.query("cdCity in @cda_dontCEx")['KEY']
cda_cityToUpdate = set(cidades['KEY'])&set(see_keys)
cda_wrong = cidades.query("KEY in @cda_cityToUpdate")['CD/CDA'].value_counts()
cda_wrong_cat = atendidas[['KEY','CDA']]\cidades.query("KEY in @cda_cityToUpdate")['CD/CDA'].value_counts()


cda_wrong_cat = atendidas[['KEY','CDA']]\
.merge(\
cidades.query("KEY in @cda_cityToUpdate")[['KEY','CD/CDA']], on='KEY')

atendidas_cdKey = set(zip(atendidas['KEY'],atendidas['cdCity']))
cidades_cdKey = set(zip(cidades['KEY'],cidades['cdCity']))
cda_toUpdateAll = atendidas_cdKey - cidades_cdKey

"""
"""



atendidas_cdKey = set(zip(atendidas['KEY'],atendidas['cdCity']))
cidades_cdKey = set(zip(cidades['KEY'],cidades['cdCity']))
cda_toUpdateAll = atendidas_cdKey - cidades_cdKey

cidades['cdaUpdated'] = cidades['CD/CDA']
cidades =                           
tools.replace(cidades,cda_wrong_cat['CDA'],'KEY','cdaUpdated')

atendidas['cdKey'] = list(zip(atendidas['KEY'],atendidas['cdCity']))
cidades['cdKey'] = list(zip(cidades['KEY'],cidades['cdCity']))

cda_wrong_catALL = atendidas[['KEY','CDA']]\
.merge(\
cidades.query("cdKey in @cda_toUpdateAll")[['KEY','CD/CDA']], on='KEY')

cidades=tools.replace_(cidades.set_index('KEY'),cda_wrong_catALL.set_index('KEY'['CDA'],'KEY','cdaUpdated')

"""
"""



"""
