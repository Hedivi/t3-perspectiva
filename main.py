"""
Executa o exeperimento de retificação de documentos utilizando 
transformação perspectiva.

O script seleciona imagens específicas do dataset a partir de um arquivo
de metadados, obtém as coordenadas dos quatro vértices dos documentos e 
aplica uma transformação perspectiva para gerar uma vista frontal do 
documento.

Para cada imagem processada, é criada uma comparação lado a lado entre a
imagem original e o resultado da transformação. As comparações são 
exibidas e salvas no diretório de saída.
"""

from pathlib import Path
import cv2
from src.perspective import perspective_transform
import pandas as pd
import sys

def resize_height(image, height):
    """
    Redimensiona uma imagem para uma altura específica mantendo sua 
    proporção.

    Args:
        image (numpy.ndarray): Imagem que será redimensionada.
        height (int): Altura desejada, em pixels.

    Returns:
        numpy.ndarray: Imagem redimensionada mantendo a proporção 
        original.
    """
    
    scale = height / image.shape[0]
    width = int(image.shape[1] * scale)

    return cv2.resize(image, (width, height))


def show_and_save_comparison(image_name, original, result):
    """
    Exibe e salva uma comparação entre a imagem original e a retificada.

    As duas imagens são redimensionadas para possuir a mesma altura e,
    posteriormente, concatenadas horizontalmente. A imagem resultante é
    exibida em uma janela e salva no diretório ``output``.

    A estrutura de diretórios presente em ``image_name`` é preservada
    dentro do diretório de saída.

    Args:
        image_name (str): Caminho relativo usado como nome da imagem de 
        saída.
        original (numpy.ndarray): Imagem original antes da transformação.
        result (numpy.ndarray): Imagem obtida após a transformação 
        perspectiva.

    Returns:
        None
    """
        
    height = min(original.shape[0], result.shape[0])

    original_resized = resize_height(original, height)
    result_resized = resize_height(result, height)

    comparison = cv2.hconcat([original_resized, result_resized])

    cv2.imshow("Original x Resultado", comparison)
    cv2.waitKey(0)

    image_save_path = Path("output") / image_name
    image_save_path.parent.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(image_save_path), comparison)
    

def read_points (metadata_path):
    """
    Lê e filtra os metadados utilizados no experimento.

    O arquivo CSV é filtrado para manter apenas imagens do 
    ``background01`` pertencentes aos documentos ``letter001`` e 
    ``magazine005``. Além disso, são selecionados somente os frames cujo 
    número é múltiplo de 10.

    As colunas mantidas contêm o caminho relativo da imagem e as 
    coordenadas dos quatro vértices do documento.

    Args:
        metadata_path (str or pathlib.Path): Caminho para o arquivo CSV
            contendo os metadados do dataset.

    Returns:
        pandas.DataFrame: DataFrame contendo as imagens selecionadas e as
        coordenadas dos quatro vértices de cada documento.
    """

    df = pd.read_csv(metadata_path)

    df = df[["bg_name", "image_path", "tl_x", "tl_y", "bl_x", "bl_y", "br_x", "br_y", "tr_x", "tr_y"]]
    df = df[df["bg_name"] == 'background01']

    df = df[df["image_path"].str.contains(r"/(letter001|magazine005)/", regex=True, na=False)]

    frame_number = df["image_path"].str.extract(r"frame_(\d+)\.jpeg")[0].astype(int)

    df = df[frame_number % 10 == 0]

    df["image"] = df["image_path"].str.replace(r"^[^/]+/","",regex=True)

    df = df.drop(columns=["bg_name", "image_path"])

    return df


def main(metadata_path, input_dir):
    """
    Executa o fluxo principal do experimento.

    Os caminhos para o arquivo de metadados e para o diretório das 
    imagens são recebidos pela linha de comando. Para cada imagem
    selecionada, o script lê as coordenadas dos quatro vértices, aplica a
    transformação perspectiva e gera uma comparação entre a imagem 
    original e a imagem retificada.

    Returns:
        None
    """

    df = read_points(metadata_path)

    input_dir = Path(input_dir)

    for _, row in df.iterrows():
        
        image_path = input_dir / row['image']

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(f"A imagem não foi encontrada: {image_path}")

        points = [[row["tl_x"], row["tl_y"]], [row["tr_x"], row["tr_y"]], [row["bl_x"], row["bl_y"]], [row["br_x"], row["br_y"]]]
        
        result, H = perspective_transform(image, points)

        show_and_save_comparison(row['image'], image, result)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    """
    Executa o fluxo principal do experimento.

    Uso:
        python3 main.py <metadata.csv> <diretorio_imagens>

    Argumentos:
        metadata.csv:
            Arquivo contendo os caminhos e as coordenadas dos documentos.

        diretorio_imagens:
            Diretório raiz contendo as imagens do dataset.
    """

    main(sys.argv[1], sys.argv[2])



