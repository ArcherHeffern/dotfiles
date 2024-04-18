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

if [ -e ~/.tmux.conf ]; then
	read -p "Warning! This will override your current tmux.conf. Proceed? (y/n)" CONTINUE
else
	CONTINUE=y
fi

if [ $CONTINUE != 'y' ]; then
	echo "Passing..."
else
	cp .tmux.conf ~/tmux.conf
fi
echo "Done"
