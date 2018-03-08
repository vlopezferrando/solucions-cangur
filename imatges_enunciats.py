#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from PIL import Image


def obte_linies(pixels):
    # Get line with first black pixel
    y = next(i for i, line in enumerate(pixels) if line.count(0) > 0)
    l = [y-10 if y-10 >= 0 else 0]

    while y < len(pixels):
        if float(pixels[y].count(0)) / len(pixels[y]) > 0.8:
            marge_esquerre = pixels[y].index(0)
            l.append(y)
            y += 10
        else:
            y += 1

    # Get line with last black pixel
    y = next(i for i, line in reversed(
        list(enumerate(pixels))) if line.count(0) > 0)
    l.append(y+15 if y+15 < len(pixels) else len(pixels))
    return l, marge_esquerre

SECCIONS_IGNORAR = [1, 2, 13, 24]
seccio = 0
questio = 0

# Per cadascuna de les 4 pàgines
for pagina in range(4):
    # Convertir a png
    os.system('convert -type grayscale -density 150 %s[%d] enunciats.png' % (
        sys.argv[1], pagina))

    # Obrir imatge amb PIL i obtindre píxels
    image = Image.open('enunciats.png')
    width, height = image.size
    is_black = list(image.convert('L').point(
        lambda x: 0 if x < 128 else 255, '1').getdata())
    pixels = [is_black[i*width:(i+1)*width] for i in range(height)]

    # Troba les posicions de les línies
    linies, marge_esquerre = obte_linies(pixels)

    # Retallar i guardar les imatges
    for y1, y2 in zip(linies, linies[1:]):
        # Ignorar seccions buides
        if sum([linia.count(0) for linia in pixels[y1+5:y2-10]]) == 0:
            continue

        # Ignorar seccions amb els títols dels blocs
        seccio += 1
        if seccio in SECCIONS_IGNORAR:
            continue
        questio += 1
        box = (marge_esquerre, y1+5, width - marge_esquerre, y2-10)
        image.crop(box).save('%02d.png' % questio)
        os.system('optipng -q %02d.png' % questio)

os.system('rm -f enunciats.png')
