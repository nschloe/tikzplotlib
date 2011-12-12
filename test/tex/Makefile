# ./Makefile

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

LATEX:=pdflatex
LATEX_OPTIONS:=

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

TARGET:=acid

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# 

default: main

main:
	@$(LATEX) $(LATEX_OPTIONS) $(TARGET)

.PHONY: clean

clean:
	@rm -f \
	    $(TARGET)-blx.bib \
	    $(TARGET).pdf \
	    $(TARGET).log \
	    $(TARGET).aux \
	    missfont.log \
	    x.log
	@rm -f *~
