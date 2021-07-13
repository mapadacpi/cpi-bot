##
#   CPI Covid-19
#   Ferramenta para salvar a lista de documentos em um JSON.
##

URL = "https://legis.senado.leg.br/comissoes/docsRecCPI?codcol=2441"

from lxml import html
import requests
import os
import json

print ("Baixando lista de documentos do Senado...")
page = requests.get(URL)
tree = html.fromstring(page.content)

print ("Listando entradas...")

# Corpo da tabela
tbody = tree.xpath('//tbody')[0]
# Lista as linhas da tabela
rows = tree.xpath('.//tr')

# Prepara uma estrutura de dados para guardar as informações da tabela
data = []

# Lê cada linha
print ("Parseando entradas...")
for item in rows:
    # Guarda as informações de cada coluna da tabela separadamente
    cols = item.xpath('.//td')
    if (len(cols) == 0): continue

    entry = {
        "id": cols[0].text,
        "links": [(l.text,l.attrib['href']) for l in cols[1].xpath('.//a')],
        "date": cols[2].text.strip(),
        "sender": cols[3].text.strip(),
        "origin": cols[4].text.strip(),
        "description": [d.strip() for d in cols[5].xpath('.//p/text()')],
        "answer_to": [(l.text,l.attrib['href']) for l in cols[6].xpath('.//a')],
    }

    data.append(entry)

print ("Salvando arquivo JSON de documentos em json/docs.json")
with open('json/docs.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
