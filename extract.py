##
#   CPI Covid-19
#   Ferramenta para extrair conteúdo de texto dos documentos.
##

## CLI

import argparse

parser = argparse.ArgumentParser(description='CPI Covid-19: Ferramenta para extrair conteúdo de texto dos documentos.')
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

data = []
with open('json/docs.json') as file:
    data = json.load(file)

# Extrai texto nativo do PDF
def extract_text(path, out):
    laparams = LAParams(line_margin = 1, boxes_flow = None, detect_vertical = True)
    text = _extract_text(path, laparams = laparams)
    with open(out, 'w') as file:
        file.write(text)

# Converte o PDF para imagens e interpreta o texto dessas imagens com OCR
def extract_ocr(path, out):
    pdfFile = wi(filename = path, resolution = 300)
    image = pdfFile.convert('jpeg')

    print('\t\t' + str(len(image.sequence)) + ' páginas')

    imageBlobs = []
    for img in image.sequence:
        imgPage = wi(image = img)
        imageBlobs.append(imgPage.make_blob('jpeg'))

    extract = ""
    for i, imgBlob in enumerate(imageBlobs):
        print('\t\t' + 'pg. ' + str(i+1))
        image = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(image, lang = 'por')
        extract += text

    if (not len(extract)): return
    with open(out, 'w') as file:
        file.write(extract)

#
print ("Extraindo texto dos arquivos pdf...")
for d in data[START-1:END]:
    for link in d['links']:
        path = d['id']+'_'+(link[0]).replace('/','#')
        print('\t'+path)
        if (os.path.isfile("./pdf/"+path+'.pdf')):
            if (not os.path.isfile("./text/"+path+'.txt')):
                print('\t\tTexto...')
                extract_text("./pdf/"+path+'.pdf', "./text/"+path+'.txt')

            if (not os.path.isfile("./ocr/"+path+'.txt')):
                print('\t\tOCR...')
                extract_ocr("./pdf/"+path+'.pdf', "./ocr/"+path+'.txt')
