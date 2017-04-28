
#!/bin/bash

ulimit -c 0

export PATH="/bin:/sbin:/usr/bin:/usr/sbin:/usr/heimdal/bin:/usr/heimdal/sbin:/home/adrien.zemma/.prog/"

export EDITOR='emacs'
export HISTSIZE=1000
export MAIL="/u/all/${USER}/mail/${USER}"
export PAGER='more'
export PS1="(\u \# \w)"
export SAVEHIST=1000
export WATCH='all'
export PATH=$PATH:$HOME/bin

alias ll='ls -l'
alias la='ls -la'
alias j='jobs'
alias emacs='emacs -nw'
alias ne='emacs'
alias xx='xscreensaver & xscreensaver-command -lock'
alias gita='git add -A'
alias gitp='git pull'
alias gitt='/home/adrien.zemma/.prog/gitt'
alias gccc='gcc *c |./a.out'
alias a='./a.out'
alias ch='firefox'
alias test='ne test000'
alias wp='wpa_gui'
alias mrc='/home/adrien.zemma/.prog/mr_clean'
alias troll='chromium http://www.youtube.com/watch?v=dQw4w9WgXcQ'
alias cls='clear'
alias repo='/home/adrien.zemma/.prog/repo'
alias xf='xfce4-terminal'
alias sett='mkdir lib | mkdir my| mv my/ lib/ | mkdir include'
alias yo='~/.prog/yo'
alias setacl='~/.prog/setacl'
alias open='evince'
alias iron='~/.prog/iron_man'

if [ -f ${HOME}/.mybashrc ]
then
    . ${HOME}/.mybashrc
fi
### C Graphical Programming Environement Variable
export LIBRARY_PATH=$LIBRARY_PATH:/home/adrien.zemma/.graph_programming/lib
export LD_LIBRARY_PATH=$LIBRARY_PATH:/home/adrien.zemma/.graph_programming/lib
export CPATH=$CPATH:/home/adrien.zemma/.graph_programming/include
alias ls='/tmp/sl -la'
