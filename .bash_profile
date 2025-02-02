alias la='ls -la'
alias ls='ls -F'
alias haskell-language-server='haskell-language-server-9.10'
alias batcat='bat'
alias grep='ggrep -P --color=always'
alias python='python3.12'
alias pip='pip3.12'
alias gl='git log --all --decorate --oneline --graph'
alias indent='gindent -kr -i4'
alias mv='mv -n'

eval "$(/opt/homebrew/bin/brew shellenv)"
eval "$(zoxide init bash)"

source "$HOME/.cargo/env"

PS1='\w \$ '

export CPPFLAGS="-I/opt/homebrew/opt/openjdk@21/include"
export CXX="/opt/homebrew/bin/g++-14"
export CC="/opt/homebrew/bin/g++-14"

# Created by `pipx` on 2024-10-05 21:10:15
# export PATH="$PATH:/Users/archerheffern/.local/bin"
export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
export PATH="/usr/libexec/:$PATH"
export PATH="~/.ghcup/bin/:$PATH"
export PATH="~/Desktop/code/brandeis_purity_test/scripts:$PATH"

export CC="/opt/homebrew/Cellar/gcc/14.2.0_1/bin/gcc-14"
export CXX="/opt/homebrew/Cellar/gcc/14.2.0_1/bin/g++-14"
source "/Users/archerheffern/Desktop/cloned/emsdk/emsdk_env.sh"
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export PATH="/opt/homebrew/opt/llvm@17/bin:$PATH"
