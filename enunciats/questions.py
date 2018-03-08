#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PIL import Image

# Obrir imatge amb PIL i anotar els píxels negres
image = Image.open(sys.argv[1])
width, height = image.size
is_black = list(image.convert('L').point(lambda x: x < 128, '1').getdata())
has_black = [any(is_black[i*width:(i+1)*width]) for i in range(height)]

# Trobar les línies separadores i els inicis i final de pàgina
linies = [i+2 for i in range(height)
          if float(sum(is_black[i*width:(i+1)*width])) / width > 0.8]
linies += [has_black.index(True, i*height/4)-5 for i in range(4)]
linies += [height + 5 - has_black[::-1].index(True) for i in range(4)]
linies = sorted(linies)

# Troba el marge esquerre, fixant-se en el primer pixel negre més a l'esquerra
marge_esquerre = min(i % width for i, b in enumerate(is_black) if b)

# Gestionar cada secció
seccio = 0
questio = 0
for y1, y2 in zip(linies, linies[1:]):
    # Ignorar seccions buides o massa petites
    if sum(has_black[y1:y2-2]) == 0 or y2-y1 < 10:
        continue

    # Ignorar seccions amb els títols dels blocs
    seccio += 1
    if seccio in [1, 2, 13, 24]:
        continue

    # Retallar i desar imatge
    questio += 1
    box = (marge_esquerre, y1, width - marge_esquerre, y2-2)
    image.crop(box).save('%02d.png' % questio)
