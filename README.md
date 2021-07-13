# Bot da CPI

Esse repositório contém pequenas ferramentas feitas em `Python` para baixar e processar os documentos públicos enviados para o Senado Federal.

### bot-dict

Ferramenta que gera os dicionários dos documentos de forma automática. Ela usa os módulos abaixo pra listar, baixar e extrair os dados.
Então, faz um dicionário de todas as palavras (em minúscula) que encontrou para cada arquivo.

```shell
  python bot-dict.py
```

### scrape

```shell
  python scrape.py
```

Extrai as informações da tabela de arquivos listados no site em um arquivo `json/docs.json`.

### download

```shell
  python download.py --pdf -s 1 -e 100

  --pdf: baixa apenas os arquivos pdf
  -s: (start) primeira id a ser baixada
  -e: (end) última id a ser baixada
```

Baixa os arquivos do site na pasta `pdf/`.
É possível limitar apenas aos arquivos PDF. Caso não esteja limitado, outros formatos são baixados na pasta `other/`.
Também é possível definir começo e fim, para baixar apenas uma faixa de documentos.

### extract

```shell
  python extract.py -s 1 -e 100
```

Extrai texto nativo do PDF em `text/` e texto interpretado de imagens via OCR em `ocr/`.
Também é possível definir começo e fim, para extrair apenas uma faixa de documentos.

### dict

```shell
  python dict.py -s 1 -e 100
```

Gera um dicionário, em `dict/` com todas as palavras que aparecem no texto (ambos text/ e ocr/).

### export

```shell
  python export.py
```

Compila todos os dicionários em um único arquivo, utilizado para a pesquisa no site.
