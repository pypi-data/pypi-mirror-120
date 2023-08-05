# cores_ptbr

Um pacote simples de cores em português escrito em Python.
Você pode ver o código [aqui](https://github.com/nugovit/cores_ptbr).

# Como usar?

Para usar esse pacote, basta importá-lo em seu código python:

```python
from coresptbr import cores
```

Esse pacote tem a função ```colorir()```, que retorna o valor dentro da função com algumas cores/estilos diferentes:

```python
cores.colorir('Hello, world!', 'mag', 'neg')
```

O código acima irá retornar a string 'Hello, World!' em negrito ('neg') e com texto em magenta ('mag').
A maioria das cores/estilos são escritos de forma abreviada. Segue abaixo a abreviação de cada uma:

```python
cores = {
    'neg': '1',      # Negrito
    'fraco': '2',    # Fraco
    'ita': '3',      # Itálico
    'sub': '4',      # Sublinhado
    'pis': '5',      # Piscar
    'inv': '7',      # Inverter
    'pre': '30',     # Preto
    'vm': '31',      # Vermelho
    'vd': '32',      # Verde
    'ama': '33',     # Amarelo
    'azu': '34',     # Azul
    'mag': '35',     # Magenta
    'cia': '36',     # Ciano
    'bra': '37',     # Branco
    'prec': '90',    # Preto-claro
    'vmc': '91',     # Vermelho-claro
    'vdc': '92',     # Verde-claro
    'amac': '93',    # Amarelo-claro
    'azuc': '94',    # Azul-claro
    'magc': '95',    # Magenta-claro
    'ciac': '96',    # Ciano-claro
    'brac': '97',    # Branco-claro (Por incrível que pareça existe.)
    'fpre': '40',    # Fundo preto
    'fvm': '41',     # Fundo vermelho
    'fvd': '42',     # Fundo verde
    'fama': '43',    # Fundo amarelo
    'fazu': '44',    # Fundo azul
    'fmag': '45',    # Fundo magenta
    'fcia': '46',    # Fundo ciano
    'fbra': '47',    # Fundo branco
    'fprec': '100',  # Fundo preto-claro
    'fvmc': '101',   # Fundo vermelho-claro
    'fvdc': '102',   # Fundo verde-claro
    'famac': '103',  # Fundo amarelo-claro
    'fazuc': '104',  # Fundo azul-claro
    'fmagc': '105',  # Fundo magenta-claro
    'fciac': '106',  # Fundo ciano-claro
    'fbrac': '107'   # Fundo branco-claro
}
```
É possível deduzir o nome das cores, basta colocar as primeiras três letras.
Branco -> ```'bra'```, Amarelo -> ```'ama'``` e assim por diante.
Vermelho e Verde são ```'vm'``` e ```'vd'``` por terem as mesmas três letras iniciais.
Para cores claras basta adicionar um 'c' na frente do nome da cor
(Amarelo-claro -> ```'amac'```).
Para colocar o fundo de uma cor basta adicionar um 'f' antes.
(Fundo verde -> ```'fvd'```, Fundo preto-claro -> ```'fprec'```).

A função ```colorir()``` permite no máximo 3 parâmetros de cor/estilo:

* Estilo do texto (1-7);
* Cor da letra (30-37, 90-97);
* Cor de fundo (40-47, 100-107);
