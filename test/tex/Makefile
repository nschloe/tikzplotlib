# ./Makefile

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

LATEXMK:=latexmk
LATEXMK_OPTIONS:=-pdf

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

TARGET:=acid

# ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# 

default: main

main:
	@$(LATEXMK) $(LATEXMK_OPTIONS) $(TARGET)

.PHONY: clean

clean:
	$(LATEXMK) -C
	@rm -f $(TARGET)-blx.bib \
	missfont.log \
	x.log
	@rm -f *~
