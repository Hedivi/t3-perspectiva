import argparse
import cv2

from perspective import perspective_transform

points = []
display = None

def mouse_callback(event, x, y, flags, param):
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
