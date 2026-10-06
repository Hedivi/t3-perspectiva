import cv2
import numpy as np


def order_points(points):

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
    Calcula largura e altura da imagem retificada
    a partir das distâncias entre os quatro vértices.
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
    Retifica a região delimitada pelos quatro pontos
    usando transformação perspectiva.
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
