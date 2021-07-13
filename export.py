##
#   CPI Covid-19
#   Ferramenta para extrair conteúdo de texto dos documentos.
##

## CLI

import argparse

parser = argparse.ArgumentParser(description='CPI Covid-19: Ferramenta para exportar o dicionário geral dos documentos.')

args = parser.parse_args()

##

import os
import json

# Confere se o arquivo "docs.json" foi criado
if (not os.path.isfile('json/docs.json')):
    print("É necessário gerar o arquivo json/docs.json e os dicionários de cada documento. Leia o README.md.\n")
    quit()

data = []
with open('json/docs.json') as file:
    data = json.load(file)

#
print ("Importando dicionários...")
for d, doc in enumerate(data):
    # Ignora documentos privados
    if (len(doc['links']) == 0):
        print("\t\t! documento privado !")
        continue
    for link in doc['links']:
        path = doc['id']+'_'+(link[0]).replace('/','#')
        print('\t'+path)
        # Confere se o dicionário existe em disco
        if (not os.path.isfile('./dict/'+path+'.json')):
            print("\t\t! dicionário não gerado !")
            continue
        # Carrega o dicionŕio do disco
        doc_dict = None
        with open('./dict/'+path+'.json', 'r') as f:
            doc_dict = json.load(f)
        # Adiciona o dicionário aos dados
        if ('dict' not in data[d]): data[d]['dict'] = []
        data[d]['dict'] += doc_dict

with open('json/dict.json', 'w') as file:
    json.dump(data, file)
