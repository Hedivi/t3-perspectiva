"""
Interface interativa para correção de perspectiva de documentos.

Este script permite selecionar manualmente os quatro vértices de um
documento presente em uma imagem. Os pontos são selecionados com cliques
do mouse e utilizados para calcular e aplicar uma transformação 
perspectiva.

Após a seleção dos quatro pontos, o programa gera uma vista retificada do
documento, exibe a matriz de homografia calculada e salva a imagem 
resultante.

Uso:
    python3 manual.py <imagem> [-o <imagem_saida>]

Exemplo:
    python3 manual.py data/documento.jpeg -o output/documento.jpeg
"""

import argparse
import cv2

from perspective import perspective_transform

points = []
display = None

def mouse_callback(event, x, y, flags, param):
    """
    Registra os pontos selecionados pelo usuário com o mouse.

    A função é utilizada como callback da janela do OpenCV. A cada clique
    com o botão esquerdo do mouse, as coordenadas do ponto são 
    armazenadas. No máximo quatro pontos podem ser selecionados.

    Cada ponto selecionado é destacado por um círculo vermelho e 
    identificado numericamente na imagem exibida.

    Args:
        event (int): Tipo de evento do mouse detectado pelo OpenCV.
        x (int): Coordenada horizontal do cursor na imagem.
        y (int): Coordenada vertical do cursor na imagem.
        flags (int): Indicadores adicionais relacionados ao evento do 
            mouse.
        param: Parâmetro opcional associado ao callback. Não utilizado 
            nesta implementação.

    Returns:
        None
    """

    global points
    global display

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if len(points) >= 4:
        return

    points.append((x, y))

    cv2.circle(display, (x, y), 6, (0, 0, 255), -1)

    cv2.putText(display, str(len(points)), (x + 10, y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Imagem", display)


def main():
    """
    Executa a seleção manual e a transformação perspectiva.

    O caminho da imagem de entrada é recebido pela linha de comando. O
    usuário deve selecionar quatro pontos correspondentes aos vértices do
    documento utilizando o botão esquerdo do mouse.

    Após selecionar os quatro pontos, a tecla ENTER confirma a seleção e
    inicia a transformação perspectiva. A tecla ESC encerra o programa 
    sem realizar a transformação.

    A imagem retificada é salva no caminho especificado pelo argumento
    ``--output`` e exibida em uma nova janela. As coordenadas 
    selecionadas e a matriz de homografia também são apresentadas no 
    terminal.

    Argumentos de linha de comando:
        image (str): Caminho para a imagem que será processada.
        -o, --output (str): Caminho para salvar a imagem retificada.
            O valor padrão é ``output.png``.

    Raises:
        FileNotFoundError: Se a imagem de entrada não puder ser 
            carregada.
        ValueError: Se o usuário não selecionar exatamente quatro pontos.

    Returns:
        None
    """

    parser = argparse.ArgumentParser(
            description="Correção de perspectiva de documentos.")

    parser.add_argument("image", help="Imagem de entrada.")

    parser.add_argument("-o", "--output", default="output.png", 
                        help="Imagem de saída.")

    args = parser.parse_args()

    image = cv2.imread(args.image)

    if image is None:
        raise FileNotFoundError(f"A imagem não abriu: {args.image}")

    global display
    display = image.copy()

    cv2.namedWindow("Imagem")

    cv2.setMouseCallback("Imagem", mouse_callback)

    print()
    print("Selecione os quatro cantos do documento.")
    print("A ordem dos pontos não importa.")
    print("Pressione ENTER após selecionar os quatro pontos.")
    print()

    while True:

        cv2.imshow("Imagem", display)

        key = cv2.waitKey(20) & 0xFF

        if key in (13, 10):  # Enter
            break

        if key == 27:  # ESC
            cv2.destroyAllWindows()
            return

    cv2.destroyAllWindows()

    if len(points) != 4:
        raise ValueError(f"Foram selecionados {len(points)} pontos. "
                         "São necessários exatamente 4.")

    result, H = perspective_transform(image, points)

    print("Pontos selecionados:")
    for point in points:
        print(point)

    print("\nMatriz de homografia:")
    print(H)

    cv2.imwrite(args.output, result)

    print(f"\nResultado salvo em: {args.output}")

    cv2.imshow("Resultado", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
