##
#   CPI Covid-19
#   Ferramenta para gerar o dicionário de documentos.
##

## CLI

import argparse

parser = argparse.ArgumentParser(description='CPI Covid-19: Ferramenta para gerar o dicionário de documentos.')
parser.add_argument('-s', metavar='START', type=int, nargs=1, default=[1],
                    help='Primeiro documento')
parser.add_argument('-e', metavar='END', type=int, nargs=1, default=[9999],
                    help='Último documento')

args = parser.parse_args()
START = args.s[0]
END = args.e[0]

##

import os
import json
import re
regex = re.compile('[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]')

# text
from pdfminer.high_level import extract_text as _extract_text
from pdfminer.layout import LAParams

# ocr
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi

# Confere se o arquivo "docs.json" foi criado
if (not os.path.isfile('json/docs.json')):
    print("É necessário gerar o arquivo json/docs.json.\nPara gerar é simples: python scrape.py")
    quit()

docs = []
with open('json/docs.json') as file:
    docs = json.load(file)

# Lê um arquivo e retorna o dicionário dele
def gen_dict(path):
    dict = set()

    with open(path, 'r') as file:
        for line in file:
            for word in line.split():
                word = regex.sub('', word).lower()
                if (not len(word)): continue
                dict.add(word)

    return dict

print ("Gerando dicionário dos documentos...")
for d in docs[START-1:END]:
    for link in d['links']:
        path = d['id']+'_'+(link[0]).replace('/','#')
        print('\t'+path)

        if (not os.path.isfile("./pdf/"+path+'.pdf')):
            continue
        if (os.path.isfile("./dict/"+path+'.json')):
            continue

        dict = set()
        if (os.path.isfile("./text/"+path+'.txt')):
            dict = dict.union(gen_dict("./text/"+path+'.txt'))

        if (os.path.isfile("./ocr/"+path+'.txt')):
            dict = dict.union(gen_dict("./ocr/"+path+'.txt'))

        with open('dict/'+path+'.json', 'w') as file:
            json.dump(list(dict), file, ensure_ascii=False)
