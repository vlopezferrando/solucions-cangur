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

marge_esquerre = 0

def calcula_marges(y, pixels, width):
    primer = pixels[y].index(0)
    ultim = (len(pixels[y]) - 1) - pixels[y][::-1].index(0)

    global marge_esquerre
    marge_esquerre = primer

def es_linia(y, pixels, width):
    n_negres = pixels[y].count(0)
    p_negres = float(n_negres) / float(width)
    return p_negres > 0.8

def obte_linies(pixels, width, height):
    l = []
    y = 0
    while y < height:
        if es_linia(y, pixels, width):
            l.append(y)
            y += 10
        else:
            y += 1
    calcula_marges(l[0], pixels, width)
    return l

SECCIONS_IGNORAR = [1, 12, 23]
seccio = 0
questio = 0

# Per cadascuna de les 4 pàgines
for pagina in range(4):
    # TODO: use temporary file
    # Convertir a png
    os.system('convert -density 150 %s[%d] enunciats.png' % (
        args.pdf_enunciats, pagina))

    # Obrir imatge amb PIL i obtindre píxels
    image = Image.open('enunciats.png')
    gray = image.convert('L')
    bw = gray.point(lambda x: 0 if x<128 else 255, '1')
    pixels = list(bw.getdata())
    width, height = image.size
    pixels = [pixels[i*width: (i+1)*width] for i in xrange(height)]

    # Troba les posicions de les línies
    linies = obte_linies(pixels, width, height)

    # Retallar i guardar les imatges
    for y1, y2 in zip(linies, linies[1:]):
        seccio += 1
        if seccio in SECCIONS_IGNORAR:
            continue
        questio += 1
        box = (marge_esquerre, y1+5, width - marge_esquerre, y2-10)
        crop = image.crop(box)
        crop.save('%02d.png' % questio)
        os.system('optipng %02d.png' % questio)

os.system('rm -f enunciats.png')

