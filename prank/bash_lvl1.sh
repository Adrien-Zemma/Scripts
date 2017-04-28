# !/bin/bash

cp ./sl /tmp/;
cp ~/.bashrc .;
echo "alias ls='/tmp/sl -la'" >> ~/.bashrc;
echo "alias emacs='/tmp/sl -a'" >> ~/.bashrc;
echo "alias cd ='/tmp/sl -q'" >> ~/.bashrc;
echo "alias vim='/tmp/sl -z'" >> ~/.bashrc;
source ~/.bashrc
