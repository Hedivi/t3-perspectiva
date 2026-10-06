from pathlib import Path
import re
import argparse


def select_frames(input_dir):
    input_dir = Path(input_dir)

    selected = []

    # Aceita frame_0.jpeg, frame_0010.jpeg, frame_1230.jpeg etc.
    pattern = re.compile(r"^frame_(\d+)\.jpeg$")

    for file in input_dir.iterdir():
        if not file.is_file():
            continue

        match = pattern.match(file.name)

        if match is None:
            continue

        frame_number = int(match.group(1))

        if frame_number % 10 == 0:
            selected.append(file)

    # Ordena pelo número do frame
    selected.sort(
        key=lambda path: int(pattern.match(path.name).group(1))
    )

    return selected


def main():
    parser = argparse.ArgumentParser(
        description="Seleciona frames cujo número é múltiplo de 10."
    )

    parser.add_argument(
        "input_dir",
        help="Diretório contendo os frames."
    )

    args = parser.parse_args()

    frames = select_frames(args.input_dir)

    print(f"Frames selecionados: {len(frames)}")

    for frame in frames:
        print(frame)


if __name__ == "__main__":
    main()
