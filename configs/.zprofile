echo "Running .zprofile"

eval "$(zoxide init zsh)"
bindkey -v
bindkey '^R' history-incremental-search-backward

source ~/.archer_profile
