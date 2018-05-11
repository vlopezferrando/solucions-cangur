all: $(patsubst pdfs/%.pdf,pngs/%/01.png,$(wildcard pdfs/*))

pngs/%/01.png: %.png
	mkdir -p $(@D)
	cd $(@D) && python ../../questions.py ../../$<
	optipng -q $(@D)/*

%.png: pdfs/%.pdf
	convert -append -density 150 $<[0-3] $@
