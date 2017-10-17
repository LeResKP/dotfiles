all:
	if test ! -e $(HOME)/.bashrc_lereskp; then echo '. $$HOME/.bashrc_lereskp' >> $(HOME)/.bashrc; ln -s $(CURDIR)/dotbashrc_lereskp ~/.bashrc_lereskp; fi
	if test ! -e $(HOME)/.gitshrc; then ln -s $(CURDIR)/dotgitshrc ~/.gitshrc; fi
	if test ! -e $(HOME)/.ackrc; then ln -s $(CURDIR)/dotackrc ~/.ackrc; fi
	if test ! -e $(HOME)/.tmux.conf; then ln -s $(CURDIR)/dottmux.conf ~/.tmux.conf; fi
	if test ! -e $(HOME)/.xmodmaprc; then ln -s $(CURDIR)/dotxmodmaprc ~/.xmodmaprc; fi
	if test ! -e $(HOME)/.gitconfig; then ln -s $(CURDIR)/dotgitconfig ~/.gitconfig; fi
