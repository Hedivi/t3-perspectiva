"""
Funções auxiliares para aplicação de transformação perspectiva em 
imagens.

Este módulo recebe quatro pontos que delimitam uma região quadrilateral 
da imagem, organiza os pontos de acordo com sua posição espacial, calcula
as dimensões da imagem de saída e aplica uma transformação perspectiva 
para obter uma vista retificada da região selecionada.
"""

import cv2
import numpy as np


def order_points(points):
    """
    Ordena quatro pontos de acordo com sua posição na imagem.

    Os pontos são organizados na seguinte ordem: superior esquerdo,
    superior direito, inferior direito e inferior esquerdo. A ordenação
    é realizada utilizando a soma e a diferença das coordenadas de cada
    ponto.

    Args:
        points (array-like): Conjunto contendo exatamente quatro pontos
            bidimensionais no formato (x, y).

    Returns:
        numpy.ndarray: Array de formato (4, 2), do tipo float32, contendo
        os pontos na ordem:
        [superior esquerdo, superior direito,
        inferior direito, inferior esquerdo].

    Raises:
        ValueError: Se o conjunto fornecido não possuir exatamente quatro
            pontos com duas coordenadas cada.
    """

    points = np.asarray(points, dtype=np.float32)

    if points.shape != (4, 2):
        raise ValueError("São necessários exatamente 4 pontos (x, y).")

    ordered = np.zeros((4, 2), dtype=np.float32)

    sums = points.sum(axis=1)
    diffs = np.diff(points, axis=1).reshape(-1)

    ordered[0] = points[np.argmin(sums)]
    ordered[1] = points[np.argmin(diffs)]
    ordered[2] = points[np.argmax(sums)]
    ordered[3] = points[np.argmax(diffs)]

    return ordered


def calculate_output_size(points):
    """
    Calcula as dimensões da imagem após a retificação.

    A largura é determinada pela maior distância entre os vértices
    superiores e inferiores. De forma semelhante, a altura é determinada
    pela maior distância entre os vértices esquerdos e direitos.

    Os pontos devem estar ordenados como superior esquerdo, superior
    direito, inferior direito e inferior esquerdo.

    Args:
        points (numpy.ndarray): Array de formato (4, 2) contendo os 
            quatro vértices ordenados da região que será retificada.

    Returns:
        tuple[int, int]: Largura e altura, em pixels, da imagem de saída,
        respectivamente.
    """

    top_left, top_right, bottom_right, bottom_left = points

    width_top = np.linalg.norm(top_right - top_left)
    width_bottom = np.linalg.norm(bottom_right - bottom_left)

    height_left = np.linalg.norm(bottom_left - top_left)
    height_right = np.linalg.norm(bottom_right - top_right)

    width = int(round(max(width_top, width_bottom)))
    height = int(round(max(height_left, height_right)))

    return width, height


def perspective_transform(image, points):
    """
    Aplica uma transformação perspectiva à região delimitada pelos 
    pontos.

    Os quatro pontos fornecidos são inicialmente ordenados e utilizados
    para calcular as dimensões da imagem de saída. Em seguida, é definida
    uma região retangular de destino e calculada a matriz de 
    transformação perspectiva que relaciona os pontos da imagem original 
    aos pontos de destino.

    A transformação é aplicada à imagem utilizando a matriz obtida,
    produzindo uma vista retificada da região selecionada.

    Args:
        image (numpy.ndarray): Imagem original na qual será aplicada a
            transformação perspectiva.
        points (array-like): Quatro pontos no formato (x, y) que 
        delimitam a região da imagem que será retificada.

    Returns:
        tuple:
            - numpy.ndarray: Imagem resultante após a transformação
              perspectiva.
            - numpy.ndarray: Matriz de homografia 3x3 utilizada na
              transformação.

    Raises:
        ValueError: Se os pontos resultarem em uma região com largura ou
            altura inválida.
    """

    source = order_points(points)

    width, height = calculate_output_size(source)

    if width <= 1 or height <= 1:
        raise ValueError("Os pontos selecionados formam uma região inválida.")

    destination = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                            [0, height - 1]], dtype=np.float32)

    H = cv2.getPerspectiveTransform(source, destination)

    result = cv2.warpPerspective(image, H, (width, height))

    return result, H
