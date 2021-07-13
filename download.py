##
#   CPI Covid-19
#   Ferramenta para baixar todos os documentos publicamente disponíveis.
##

## CLI

import argparse

parser = argparse.ArgumentParser(description='CPI Covid-19: Ferramenta para baixar todos os documentos publicamente disponíveis.')
parser.add_argument('--pdf', action='store_true',
                    help='Baixar apenas arquivos PDF')
parser.add_argument('-s', metavar='START', type=int, nargs=1, default=[1],
                    help='Primeiro documento')
parser.add_argument('-e', metavar='END', type=int, nargs=1, default=[9999],
                    help='Último documento')

args = parser.parse_args()
PDF_ONLY = args.pdf
START = args.s[0]
END = args.e[0]

##

URL = "https://legis.senado.leg.br/comissoes/docsRecCPI?codcol=2441"

from lxml import html
import requests
import os
import json

# Confere se o arquivo "docs.json" foi criado
if (not os.path.isfile('json/docs.json')):
    print("É necessário gerar o arquivo json/docs.json.\nPara gerar é simples: python scrape.py")
    quit()

data = []
with open('json/docs.json') as file:
    data = json.load(file)

print ("Baixando arquivos de documentos...")
for d in data[START-1:END]:
    for link in d['links']:
        path = d['id']+'_'+(link[0]).replace('/','#')
        # Confere se é PDF
        headers = requests.head(link[1]).headers
        if (headers['Content-Type'] == 'application/pdf'):
            path = 'pdf/' + path + '.pdf'
        else:
            if (PDF_ONLY):
                continue
            else:
                path = 'other/' + path
        print('\t'+path)

        # Caso o arquivo não exista em disco, baixa
        if (not os.path.isfile(path)):
            raw = requests.get(link[1])
            with open(path, 'wb') as f:
                f.write(raw.content)
