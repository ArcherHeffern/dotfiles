#!/usr/bin/env bash

set -euo pipefail

# TODO: Check if all packages are installed

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

# AScripts
if [ -e ~/code/AScripts/ ]; then
	read -p "Warning! This will override your current AScripts. Proceed? (y/n) " CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	rm -rf ~/code/AScripts/
	mkdir -p ~/code/
	git clone 'https://github.com/archerheffern/AScripts/' ~/code/AScripts/
fi

# MACOS ONLY
if [[ "$(uname -s)" == "Darwin" ]]; then
	# add updating brew to launchctl 
	if [ -e ~/Library/LaunchAgents/archer.homebrew.update.plist ]; then
		read -p "Warning! This will override your current Homebrew updater. Proceed? (y/n) " CONTINUE
	else
		CONTINUE=y
	fi

	if [ $CONTINUE != 'y' ]; then
		echo "Passing..."
	else

		mkdir -p ~/Scripts/
		[[ -e ~/Scripts/update_homebrew.sh ]] && rm ~/Scripts/update_homebrew.sh
		cp ./scripts/update_homebrew.sh ~/Scripts/update_homebrew.sh
		chmod +x ~/Scripts/update_homebrew.sh
		[[ -e ~/Library/LaunchAgents/archer.homebrew.update.plist ]] && rm ~/Library/LaunchAgents/archer.homebrew.update.plist
		cp ./scripts/archer.homebrew.update.plist ~/Library/LaunchAgents/archer.homebrew.update.plist
		launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/archer.homebrew.update.plist || : # In case already booted
		launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/archer.homebrew.update.plist
	fi

fi

echo 'Done. Next:'
echo 'Launch vim and run :PluginInstall'
echo 'Source the new bash_profile using `source ~/.bash_profile`'
