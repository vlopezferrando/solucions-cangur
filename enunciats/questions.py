#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PIL import Image

# Obrir imatge amb PIL i anotar els píxels negres
image = Image.open(sys.argv[1])
width, height = image.size
is_black = list(image.convert('L').point(lambda x: x < 128, '1').getdata())
has_black = [any(is_black[i*width:(i+1)*width]) for i in range(height)]
ultim_black = [width - is_black[(i+1)*width-1:i*width-1:-1].index(True)
               if has_black[i] else 0
               for i in range(height)]

# Trobar les línies separadores i els inicis i final de pàgina
linies = [i+2 for i in range(height)
          if float(sum(is_black[i*width:(i+1)*width])) / width > 0.7]
linies += [has_black.index(True, i*height/4)-5 for i in range(4)]
linies += [height + 5 - has_black[::-1].index(True) for i in range(4)]
linies = sorted(linies)

# Troba el marge esquerre, fixant-se en el primer pixel negre més a l'esquerra
marge_esquerre = min(i % width for i, b in enumerate(is_black) if b)

# Gestionar cada secció
questio = 0
for y1, y2 in zip(linies, linies[1:]):
    # Ignorar:
    #  - Seccions massa petites
    #  - Seccions que no tenen negre a les primeres files
    #  - Seccions que tenen menys de 40 línies de negre
    #  - Seccions que no tenen negre a partir del 70% d'amplada
    if y2-y1 > 10 \
            and sum(has_black[y1:y1+30]) > 0 \
            and sum(has_black[y1:y2]) > 40 \
            and max(ultim_black[y1:y2-2]) > 0.7*width:
        # Retallar i desar imatge
        questio += 1
        box = (marge_esquerre, y1, width - marge_esquerre, y2-2)
        image.crop(box).save('%02d.png' % questio)
