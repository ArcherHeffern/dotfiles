#!/usr/bin/env bash

set -euo pipefail

# VIMRC
if [ -e ~/.vimrc ]; then
	read -p "Warning! This will override your current vimrc. Proceed? (y/n) " CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	mkdir -p ~/.vim/
	cp -r ./colors ~/.vim/colors
	cp .vimrc ~/.vimrc
fi

# BASH_PROFILE
if [ -e ~/.bash_profile ]; then
	read -p "Warning! This will override your current bash_profile. Proceed? (y/n) " CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	cp .bash_profile ~/.bash_profile
fi

# TMUX
if [ -e ~/.tmux.conf ]; then
	read -p "Warning! This will override your current tmux.conf. Proceed? (y/n) " CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	cp .tmux.conf ~/.tmux.conf
fi

echo 'Done. Next:'
echo 'Launch vim and run :PluginInstall'
echo 'Source the new bash_profile using `source ~/.bash_profile`'
