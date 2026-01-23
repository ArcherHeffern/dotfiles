echo "Running .bash_profile"

eval "$(zoxide init bash)"
stty -ixon # To enable backwards cycling through reverse-i-search by using CTRL-S

source ~/.archer_profile

