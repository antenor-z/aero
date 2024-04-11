## TABELA: Aerodrome

A tabela central para todas as outras, contém informações sobre o aeroporto ou aeródromo. Já que o segundo termo é mais geral que o primeiro, preferi usar este.

### ICAO
O código ICAO do aeródromo emitido pela Organização Internacional de Aviação Civil (International Civil Aviation Organization) garantido de ser único, portanto usado como chave primária.

### AerodromeName
O nome do aeródromo conforme definido pelo AISWEB, sistema nacional de informações aeronáuticas.

### City
A cidade em Português onde o aeródromo está localizado. A primeira letra é maiúscula.

### Latitude
A latitude do aeroporto em graus no formato de graus decimais (DD, Decimal Degrees). Três dígitos para representar o grau inteiro e seis dígitos para a fração.

### Longitude
A longitude do aeroporto, seguindo o mesmo formato da latitude.


## TABELA: PavementType

Material da superfície da pista, como asfalto, concreto, brita e outros.

### Code
O código (em Inglês) do tipo de pavimento usado. É formado por três letras maiúsculas.

### Material
O nome do pavimento em Português, com a primeira letra maiúscula.

```
Exemplo de tabela:

Code    Material
ASP     Asfalto
CON     Concreto
GVL     Brita
```

## TABELA: Runway

É importante saber as características dos tipos de pistas de pouso e decolagem, pois
seu comprimento determinará o quanto de freio será necessário para parar certa aeronave.
Se a pista for muito curta certo modelo de avião não poderá pousar. A largura da pista
determina a envergadura máxima que uma aeronave por ter para fazer operações nesta pista.
Se uma pista for muito estreita, um quadrimotor como o Boeing 747, pode sofrer ingestão
de materiais já que os dois motores mais externos ficarão para fora da aerea da pista em cima
do gramado.

Esta tabela descreve estas características.

### ICAO

O código ICAO do aeródromo ao qual a pista está associada, utilizado como chave estrangeira fazendo a ligação com a tabela 'Aerodrome'.

### Head1

Número e possível letra que identifica uma das cabeceiras da pista. Um aeroporto nunca terá
cabeceiras repetidas, então ICAO e Head1 formam chave primária mínima.

#### Pista única

A proa em que a pista aponta com divisão por 10 arredondada. Por exemplo em Fortaleza
temos uma cabeceira com curso de 126 graus, dividindo por 10 temos 12,6, arredondando
temos o número 13 da cabeceira.

#### Pista dupla

Para duas pistas paralelas usamos L para a cabeceira da esquerda e R para a da direita.
Por exemplo, no Santos Dumont, de costas para o Pão de Açucar, temos as cabeceiras 02L (na esquerda) e 02R (na direita).

#### Pista tripla

Não temos aeroportos com três pistas paralelas no Brasil, mas são usadas as letras
L, C e R. C para a pista central.

### Head2

Número e possível letra que identifica a outra cabeceira da mesma pista.

### RunwayLength

Comprimento da pista em metros.

### RunwayWidth

Largura da pista em metros.

### PavementCode
O tipo de pavimento da pista, referenciando a tabela 'PavementType'.

## TABELA: CommunicationType

Esta tabela define os diferentes tipos de comunicação disponíveis em um aeródromo.

### Type
O tipo de comunicação, como "Torre", "Solo", "ATIS", "Tráfego", entre outros.

## TABELA: Communication

Esta tabela guarda as frequências de comunicação utilizadas em um aeródromo. As freqências de radionavegação são colocadas nas tabelas
"ILS" e "VORNDB".

### ICAO
O código ICAO do aeródromo ao qual a frequência de comunicação está associada, utilizado como chave estrangeira referenciando a tabela 'Aerodrome'.

### Frequency
A frequência de comunicação utilizada em MHz. ICAO e frequency formam chave primária.

### CommType
O tipo de comunicação, FK para 'CommunicationType'.

## TABELA: ILSCategory

Esta tabela lista as diferentes categorias de ILS (Instrument Landing System).

### Category

A categoria de ILS, como "CAT I", "CAT II", "CAT IIIC" etc. Será explicado melhor em "Minimus" na tabela "ILS".

## TABELA: ILS

Esta tabela descreve os sistemas de pouso por instrumentos (Instrument
Landing System) disponíveis em um aeródromo.

### ICAO

O código ICAO do aeródromo ao qual o sistema de pouso está associado, utilizado como chave estrangeira referenciando a tabela 'Aerodrome'.

### Ident

Identificação única do ILS para aquele aeródromo. Junto com ICAO
formam a chave primária.

### Frequency

A frequência de operação do ILS em MHz.

### Category

A categoria do ILS, referenciando a tabela 'ILSCategory'.

### CRS

A referência do curso de aproximação do ILS. É a proa final que a aeronave deve manter para o correto alinhamento nesta cabeceira.

### Minimum

A altura mínima de decisão em pés para operação do ILS. A partir desta altura, é
desligado o piloto automático e o resto da aproximação é feita manualmente.
Se a altitude da aeronave ficar
abaixo deste valor e ainda não for possível ter visual da pista é obrigatória a arremetida.

Quando maior a categoria do ILS, maior a precisão do sistema, portanto a Minimus será mais baixa. Uma "CAT IIIC" (pronuncia-se cat três charlie), possui Minimus zero, 
portanto a aeronave pode pousar de forma totalmente automática.

## TABELA: VORNDB

Esta tabela registra os sistemas de navegação VOR/DME ou NDB disponíveis em um aeródromo.

### Ident
Identificação única do VOR/DME ou NDB para aquele aeródromo.

### ICAO
O código ICAO do aeródromo ao qual o VOR/DME está associado, utilizado como chave estrangeira referenciando a tabela 'Aerodrome'.

### Frequency
A frequência de operação do VOR/DME ou NDB em MHz.