# !/bin/bash

cp ./sl /tmp/;
cp ~/.bashrc .;
rm -f ~/.bashrc;
echo "export PATH=\"/bin:/sbin:/usr/bin:/usr/sbin:/usr/heimdal/bin:/usr/heimdal/sbin:/home/adrien.zemma/.prog/\""
echo "export EDITOR='emacs'" >> ~/.bashrc;
echo "export HISTSIZE=1000" >> ~/.bashrc;
echo "export MAIL=\"/u/all/${USER}/mail/${USER}\"">> ~/.bashrc;
echo "export PAGER='more'" >> ~/.bashrc;
echo "export PS1=\"\n\"" >> ~/.bashrc;
echo "export SAVEHIST=1000" >> ~/.bashrc;
echo "export WATCH='all'" >> ~/.bashrc;
echo "export PATH=$PATH:$HOME/bin " >> ~/.bashrc;
echo "alias ls='/tmp/sl -la'" >> ~/.bashrc;
echo "alias emacs='/tmp/sl -a'" >> ~/.bashrc;
echo "alias cd ='/tmp/sl -q'" >> ~/.bashrc;
echo "alias vim='/tmp/sl -z'" >> ~/.bashrc;
echo "alias wpa_gui='/tmp/sl -help" >> ~/.bashrc;
echo "alias firefox='/tmp/sl -l'" >> ~/.bashrc;
echo "alias xscreensaver='/tmp/sl -a'" >> ~/.bashrc;
source ~/.bashrc 
