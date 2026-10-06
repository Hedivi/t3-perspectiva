# Transformação Perspectiva para Retificação de Documentos

Trabalho desenvolvido para a disciplina de **Visão Computacional e
Percepção**, com o objetivo de implementar e avaliar uma aplicação
simples de transformação perspectiva utilizando Python e OpenCV.

A aplicação realiza a **retificação de documentos fotografados em
perspectiva**, transformando a região quadrilateral correspondente ao
documento em uma vista frontal retangular, semelhante à obtida por um
scanner.

## Objetivo

O objetivo do projeto é aplicar uma transformação perspectiva a imagens
de documentos capturadas em diferentes ângulos.

A partir das coordenadas dos quatro vértices do documento na imagem
original, é calculada uma matriz de homografia que mapeia o documento
para uma região retangular. A transformação é então aplicada utilizando
as funções `getPerspectiveTransform()` e `warpPerspective()` do OpenCV.

O projeto possui duas formas de execução:

1.  **Seleção manual:** o usuário seleciona os quatro vértices do
    documento utilizando o mouse.
2.  **Experimento com dataset:** as coordenadas dos vértices são obtidas
    automaticamente a partir dos metadados do dataset.

## Transformação perspectiva

Uma transformação perspectiva permite mapear pontos entre dois planos
por meio de uma matriz de homografia `H` de dimensão 3 × 3.

Para realizar a retificação, são utilizados quatro pontos da imagem
original:

-   superior esquerdo;
-   superior direito;
-   inferior direito;
-   inferior esquerdo.

Esses pontos são associados aos quatro vértices de uma região retangular
de destino.

A matriz de transformação é calculada utilizando:

``` python
H = cv2.getPerspectiveTransform(source, destination)
```

Em seguida, a transformação é aplicada à imagem:

``` python
result = cv2.warpPerspective(image, H, (width, height))
```

As dimensões da imagem de saída são calculadas a partir das distâncias
entre os vértices do documento original.

## Dataset

Para os experimentos foi utilizado o dataset **SmartDoc 2015 --
Challenge 1**, que contém imagens de documentos capturadas sob
diferentes condições e perspectivas.

Os metadados utilizados pelo programa fornecem as coordenadas dos quatro
vértices dos documentos em cada frame:

-   `tl_x`, `tl_y`: canto superior esquerdo;
-   `tr_x`, `tr_y`: canto superior direito;
-   `br_x`, `br_y`: canto inferior direito;
-   `bl_x`, `bl_y`: canto inferior esquerdo.

Neste experimento foram utilizadas imagens do `background01` e dos
documentos `letter001` e `magazine005`.

Para reduzir a quantidade de imagens processadas e obter amostras
distribuídas ao longo das sequências, foram selecionados somente frames
cujo número é múltiplo de 10.

## Estrutura do projeto

``` text
t3-perspectiva/
├── data/
│   ├── metadata.csv
│   └── seleciona.py
├── src/
│   ├── manual.py
│   └── perspective.py
├── output/
├── main.py
└── README.md
```

### `src/perspective.py`

Contém as funções responsáveis pela transformação perspectiva:

-   `order_points()`: organiza os quatro vértices na ordem superior
    esquerdo, superior direito, inferior direito e inferior esquerdo;
-   `calculate_output_size()`: calcula a largura e a altura da imagem
    retificada;
-   `perspective_transform()`: calcula a matriz de homografia e aplica a
    transformação perspectiva.

### `src/manual.py`

Implementa uma interface interativa para testar a transformação em uma
imagem individual.

O usuário seleciona os quatro vértices do documento utilizando o botão
esquerdo do mouse. Após a seleção, o programa calcula a transformação,
mostra a matriz de homografia e salva a imagem retificada.

### `main.py`

Executa o experimento utilizando os metadados do dataset.

O programa:

1.  lê o arquivo de metadados;
2.  seleciona as imagens utilizadas no experimento;
3.  recupera as coordenadas dos quatro vértices;
4.  carrega cada imagem;
5.  aplica a transformação perspectiva;
6.  cria uma comparação entre a imagem original e a imagem retificada;
7.  salva os resultados no diretório `output/`.

### `data/seleciona.py`

Script auxiliar utilizado para identificar frames cujo número é múltiplo
de 10.

## Dependências

O projeto foi desenvolvido em Python e utiliza as seguintes bibliotecas:

``` text
numpy
pandas
opencv-python
```

As dependências podem ser instaladas com:

``` bash
pip install numpy pandas opencv-python
```

Recomenda-se a utilização de um ambiente virtual:

``` bash
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas opencv-python
```

## Execução manual

Para realizar a transformação de uma imagem escolhendo manualmente os
quatro vértices:

``` bash
python3 src/manual.py <imagem>
```

Por exemplo:

``` bash
python3 src/manual.py data/documento.jpeg
```

Também é possível especificar o caminho da imagem de saída:

``` bash
python3 src/manual.py data/documento.jpeg -o output/documento.jpeg
```

Uma janela será aberta com a imagem.

Selecione os **quatro cantos do documento** utilizando o botão esquerdo
do mouse. A ordem de seleção não é importante.

Após selecionar os quatro pontos:

-   pressione **ENTER** para executar a transformação;
-   pressione **ESC** para cancelar.

O programa também apresenta no terminal as coordenadas selecionadas e a
matriz de homografia calculada.

## Execução do experimento

O experimento principal recebe dois argumentos:

``` bash
python3 main.py <metadata.csv> <diretorio_imagens>
```

Por exemplo:

``` bash
python3 main.py data/metadata.csv data/frames
```

O primeiro argumento corresponde ao arquivo CSV contendo os metadados e
as coordenadas dos vértices. O segundo corresponde ao diretório raiz no
qual estão armazenadas as imagens do dataset.

Para cada frame selecionado, o programa aplica a transformação e
apresenta uma comparação:

``` text
Imagem original | Imagem retificada
```

As comparações também são armazenadas no diretório:

``` text
output/
```

A estrutura dos documentos é preservada, resultando, por exemplo, em:

``` text
output/
├── letter001/
│   ├── frame_0010.jpeg
│   ├── frame_0020.jpeg
│   └── ...
└── magazine005/
    ├── frame_0010.jpeg
    ├── frame_0020.jpeg
    └── ...
```

## Metodologia

Para cada imagem selecionada, as coordenadas dos quatro vértices do
documento são obtidas a partir dos metadados.

Os pontos são convertidos para `float32` e organizados na seguinte
ordem:

``` text
TL -------- TR
|            |
|            |
|            |
BL -------- BR
```

A largura da imagem de destino é determinada pela maior distância entre
as bordas superior e inferior. A altura é determinada pela maior
distância entre as bordas esquerda e direita.

Com essas dimensões, são definidos os quatro pontos do retângulo de
destino:

``` text
(0, 0) ---------------- (width - 1, 0)
  |                            |
  |                            |
  |                            |
(0, height - 1) ----- (width - 1, height - 1)
```

A correspondência entre os quatro pontos da imagem original e os quatro
pontos do retângulo permite calcular a matriz de transformação
perspectiva.

Por fim, `cv2.warpPerspective()` realiza o mapeamento dos pixels da
imagem original para a imagem retificada.

## Resultados

A aplicação permite corrigir a distorção perspectiva presente nas
imagens dos documentos, produzindo uma representação frontal e
retangular da região selecionada.

Para facilitar a avaliação visual, o experimento gera imagens contendo o
frame original e o resultado da retificação lado a lado.

Os resultados obtidos são armazenados no diretório `output/`.

## Tecnologias utilizadas

-   Python
-   OpenCV
-   NumPy
-   Pandas

## Autores

Trabalho desenvolvido por:

-   Heloísa Dias Viotto
-   \[Nome do integrante\]
-   \[Nome do integrante\]

Universidade Federal do Paraná (UFPR)\
Disciplina de Visão Computacional e Percepção

## Referências

-   OpenCV. *Geometric Image Transformations*. OpenCV Documentation.
-   SmartDoc 2015 Challenge 1 Dataset.
