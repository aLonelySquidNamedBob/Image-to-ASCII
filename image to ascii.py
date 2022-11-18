from unittest import result
from PIL import Image, ImageDraw
import numpy as np
import tkinter as tk
from tkinter import filedialog

def compress(image, t_cols, t_lignes):
    image_sortie = np.zeros((t_lignes, t_cols, 3), dtype = np.uint8)
    for col in range(t_cols):
        for ligne in range(t_lignes):
            for i in range(3):
                # try:
                image_sortie[ligne, col, i] = image[int(ligne * ratio_lignes), int(col * ratio_cols), i]
                # except:
                #     Exception.
                #     print(f"index: {int(ligne * ratio_lignes)}, ratio: {ratio_lignes}, line: {ligne}, total lines: {t_cols}")
                #     quit()
    return image_sortie

def find_min_max(image):
    i_min, i_max = 255,0
    for ligne in range(target_lignes):
        for col in range(target_lignes):
            r,v,b =[int(x) for x in image[ligne, col]]
            i = (r+v+b)/3
            i_min = min(i_min, i)
            i_max = max(i_max, i)
    return i_min, i_max

def bw(image):
    image_sortie = np.copy(image)
    for ligne in range(target_lignes):
        for col in range(target_cols):
            luminance = 0.2126 * image[ligne, col, 0] + 0.7152 * image[ligne, col, 1] + 0.0722 * image[ligne, col, 2]
            image_sortie[ligne, col] = luminance
    return image_sortie

def to_ascii(image):
    chars = " .:-=+*#%@"
    # chars = chars[::-1]
    table = []
    for ligne in range(target_lignes):
        table.append([])
        for col in range(target_cols):
            brightness = image[ligne, col, 0] / 255
            table[ligne].append(chars[int(brightness * (len(chars) - 1))])
    return table

def main():
    global ratio_lignes, ratio_cols, target_lignes, target_cols

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    if file_path == None:
        raise TypeError("Please select an image")

    image_entrée = np.asarray(Image.open(file_path))
    nb_lignes, nb_colonnes, _ = image_entrée.shape
    ratio = nb_colonnes / nb_lignes
    target_lignes = 70
    target_cols = int(target_lignes * ratio * 2.4)

    ratio_lignes = nb_lignes / target_lignes
    ratio_cols = nb_colonnes / target_cols

    image = compress(image_entrée, target_cols, target_lignes)
    image = bw(image)
    result = to_ascii(image)
    for i in result:
        for j in i:
            print(j, end='')
        print('')

if __name__ == "__main__":
    main()