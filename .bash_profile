echo "Running .bash_profile"

set -o vi
stty -ixon # To enable backwards cycling through reverse-i-search by using CTRL-S

command -v brew &> /dev/null && { brew update && brew upgrade; }

alias ls='ls -F'
alias la='ls -la'
alias haskell-language-server='haskell-language-server-9.10'
alias batcat='bat'
alias python='python3.12'
alias pip='pip3.12'
alias gl='git log --all --decorate --oneline --graph'
alias indent='gindent -kr -i4'
alias mv='mv -n'
alias grin='grep -rin'
alias 8='ping 8.8.8.8'
alias swagger='npx open-swagger-ui --open'
alias du-pretty='du -s --si'

eval "$(zoxide init bash)"

# MACOS ONLY
if [[ "$(uname -s)" == "Darwin" ]]; then
	alias grep='ggrep -P --color=always'
	eval "$(/opt/homebrew/bin/brew shellenv)"
	export CPPFLAGS="-I/opt/homebrew/opt/openjdk@21/include"
	export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"
	export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
	export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
	export PATH="/usr/libexec/:$PATH"
	export PATH="$HOME/.ghcup/bin/:$PATH"
	export PATH="$HOME/Desktop/code/brandeis_purity_test/scripts:$PATH"
	export PATH="$HOME/.local/bin:$PATH"
	export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
	export PATH="/opt/homebrew/opt/llvm@17/bin:$PATH"
	# Created by `pipx` on 2024-10-05 21:10:15
	# export PATH="$PATH:/Users/archerheffern/.local/bin"
	export CXX="/opt/homebrew/bin/g++-14"
	export CC="/opt/homebrew/bin/g++-14"
	export CC="/opt/homebrew/Cellar/gcc/14.2.0_1/bin/gcc-14"
	export CXX="/opt/homebrew/Cellar/gcc/14.2.0_1/bin/g++-14"
# ELSE
else
	alias fd='fdfind'
	alias grep='grep -P --color=always'
fi

CARGO_ENV="$HOME/.cargo/env"
if [[ -e $CARGO_ENV ]]; then
	source $CARGO_ENV
fi

EMDSK_ENV="/Users/archerheffern/Desktop/cloned/emsdk/emsdk_env.sh"
if [[ -f $EMSDK_ENV ]]; then
	source $EMSDK_ENV
fi

PS1='\w \$ '

if command -v tmux &> /dev/null && [ -n "$PS1" ] && [[ ! "$TERM" =~ screen ]] && [[ ! "$TERM" =~ tmux ]] && [ -z "$TMUX" ]; then
  exec tmux
fi
