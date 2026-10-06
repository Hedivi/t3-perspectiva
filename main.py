from pathlib import Path
import cv2
from src.perspective import perspective_transform
import pandas as pd
import sys

def resize_height(image, height):
    scale = height / image.shape[0]
    width = int(image.shape[1] * scale)

    return cv2.resize(image, (width, height))

def show_comparison(original, result):
    # Mantém a proporção e deixa as duas com a mesma altura
    height = min(original.shape[0], result.shape[0])

    original_resized = resize_height(original, height)
    result_resized = resize_height(result, height)

    # Junta horizontalmente
    comparison = cv2.hconcat([
        original_resized,
        result_resized
    ])

    cv2.imshow("Original x Resultado", comparison)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

metadata_path = sys.argv[1]
input_dir = sys.argv[2]

df = pd.read_csv(metadata_path)

df = df[["bg_name", "image_path", "tl_x", "tl_y", "bl_x", "bl_y", "br_x", "br_y", "tr_x", "tr_y"]]
df = df[df["bg_name"] == 'background01']

df = df[df["image_path"].str.contains(r"/(letter001|magazine005)/", regex=True, na=False)]

frame_number = df["image_path"].str.extract(r"frame_(\d+)\.jpeg")[0].astype(int)

df = df[frame_number % 10 == 0]

df["image"] = df["image_path"].str.replace(r"^[^/]+/","",regex=True)

df = df.drop(columns=["bg_name", "image_path"])


input_dir = Path(input_dir)

for _, row in df.iterrows():
    
    image_path = input_dir / row['image']

    image = cv2.imread(image_path)
    

    if image is None:
        raise FileNotFoundError(f"A imagem não foi encontrada: {image_path}")

    points = [[row["tl_x"], row["tl_y"]], [row["tr_x"], row["tr_y"]], [row["bl_x"], row["bl_y"]], [row["br_x"], row["br_y"]]]
    
    result, H = perspective_transform(image, points)

    show_comparison(image, result)



