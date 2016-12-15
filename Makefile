all:
		cp -a $(CURDIR)/konsole $(HOME)/.kde/share/apps/
		if test ! -e $(HOME)/.xmodmap; then ln -s $(CURDIR)/dotxmodmap $(HOME)/.xmodmap; fi
		if test ! -e $(HOME)/.tmux.conf; then ln -s $(CURDIR)/tmux/tmux.cont $(HOME)/.tmux.conf; fi
