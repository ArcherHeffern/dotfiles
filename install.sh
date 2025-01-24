# VIMRC
if [ -e ~/.vimrc ]; then
	read -p "Warning! This will override your current vimrc. Proceed? (y/n)" CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	cp -r ./colors ~/.vim/colors
	cp .vimrc ~/.vimrc
fi

# BASH_PROFILE
if [ -e ~/.bash_profile ]; then
	read -p "Warning! This will override your current bash_profile. Proceed? (y/n)" CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	cp .bash_profile ~/.bash_profile
fi
echo "Done"

# TMUX
if [ -e ~/.tmux.conf ]; then
	read -p "Warning! This will override your current tmux.conf. Proceed? (y/n)" CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	cp .tmux.conf ~/.tmux.conf
fi
echo "Done"
