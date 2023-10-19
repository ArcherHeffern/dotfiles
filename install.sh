read -p "Warning! This will override your current vimrc. Proceed? (y/n)" CONTINUE
if [ $CONTINUE = "y" ]
then 
  cp -r ./colors ~/.vim/colors
  cp .vimrc ~/.vimrc
fi
