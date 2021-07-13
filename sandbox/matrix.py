##
#   CPI Covid-19
#   Ferramenta para criar mapa de palavras do documento
#
#   O mapa consiste em duas estruturas:
#   - Uma lista de palavras (dicionário)
#   - Uma matriz de sucessão: quantas vezes a palavra Y apareceu depois da palavra X
##

import pickle
import os
import re
regex = re.compile('[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]')

def map_text(path, out):
    map = {}

    with open(path, 'r') as file:
        last = None
        for line in file:
            for word in line.split():
                word = regex.sub('', word).lower()
                if (not len(word)): continue
                if (word not in map):
                    map[word] = {}
                    map[word]['count'] = 0
                    map[word]['next'] = {}
                map[word]['count'] += 1
                if (last != None):
                    if (word not in map[last]['next']):
                        map[last]['next'][word] = 0
                    map[last]['next'][word] += 1
                last = word

    dict = list(map.keys())
    if (not len(dict)): return

    matrix = [[0 for x in range(len(dict))] for y in range(len(dict))]
    for d in range(len(dict)):
        for next, count in map[dict[d]]['next'].items():
            dn = dict.index(next)
            matrix[d][dn] = count

    data = {}
    data['dict'] = dict
    data['matrix'] = matrix
    with open(out, 'wb') as file:
        pickle.dump(data, file)

texts = sorted(os.listdir("./text"))
for text in texts:
    print("Gerando mapa do arquivo " + text)
    map_text("./text/"+text, "./map/"+text.split('.txt')[0]+'.pickle')
