all:
	if test ! -e $(HOME)/.bashrc_lereskp; then echo '. $$HOME/.bashrc_lereskp' >> $(HOME)/.bashrc; ln -s $(CURDIR)/dotbashrc_lereskp ~/.bashrc_lereskp; fi
