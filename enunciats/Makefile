PDFS = $(shell find enunciats_pdfs -name *.pdf)
PNGS_ENUNCIATS = $(patsubst enunciats_pdfs%.pdf,enunciats_pngs%.png,$(PDFS))
PNGS_QUESTIONS = $(patsubst enunciats_pngs%.png,questions_pngs%/01.png,$(PNGS_ENUNCIATS))

all: $(PNGS_QUESTIONS)

questions_pngs/%/01.png: enunciats_pngs/%.png
	mkdir -p $(@D)
	cd $(@D) && python ../../questions.py ../../$<
	optipng -q $<

enunciats_pngs/%.png: enunciats_pdfs/%.pdf
	convert -type grayscale -append -density 150 $<[0-3] $@

