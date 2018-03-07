#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from PIL import Image

# Agafar les últimes 4 pàgines
# pdftk enunciat_2015_cat_1.pdf cat 17-end output enunciat_2015_val_1.pdf

# cd Cangur/2015_val/nivell2/enunciats_images
# ../../../imatges_enunciats.py ../enunciat_2015_val_2.pdf

# Llegir paràmetre del pdf amb els enunciats
parser = argparse.ArgumentParser()
parser.add_argument('pdf_enunciats')
args = parser.parse_args()


def obte_linies(pixels):
    # Get line with first black pixel
    y = next(i for i, line in enumerate(pixels) if line.count(0) > 0)
    l = [y-10 if y-10 >= 0 else 0]

    y = 0
    while y < len(pixels):
        if float(pixels[y].count(0)) / len(pixels[y]) > 0.8:
            marge_esquerre = pixels[y].index(0)
            l.append(y)
            y += 10
        else:
            y += 1

    # Get line with last black pixel
    y = next(i for i, line in reversed(list(enumerate(pixels))) if line.count(0) > 0)
    l.append(y+15 if y+15 < len(pixels) else len(pixels))
    return l, marge_esquerre

SECCIONS_IGNORAR = [1, 2, 13, 24]
seccio = 0
questio = 0

# Per cadascuna de les 4 pàgines
for pagina in range(4):
    # Convertir a png
    os.system('convert -density 150 %s[%d] enunciats.png' % (
        args.pdf_enunciats, pagina))

    # Obrir imatge amb PIL i obtindre píxels
    image = Image.open('enunciats.png')
    gray = image.convert('L')
    bw = gray.point(lambda x: 0 if x<128 else 255, '1')
    pixels = list(bw.getdata())
    width, height = image.size
    pixels = [pixels[i*width:(i+1)*width] for i in range(height)]

    # Troba les posicions de les línies
    linies, marge_esquerre = obte_linies(pixels)

    # Retallar i guardar les imatges
    for y1, y2 in zip(linies, linies[1:]):
        # Ignorar seccions buides
        if sum([linia.count(0) for linia in pixels[y1+5:y2-10]]) == 0:
            continue

        seccio += 1
        if seccio in SECCIONS_IGNORAR:
            continue
        questio += 1
        box = (marge_esquerre, y1+5, width - marge_esquerre, y2-10)
        crop = image.crop(box)
        crop.save('%02d.png' % questio)
        #os.system('optipng %02d.png' % questio)

os.system('rm -f enunciats.png')

