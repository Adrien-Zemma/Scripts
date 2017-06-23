#!/usr/bin/python3.6
import os
import re
import sys
import glob
import pwd
import time
import getpass
import argparse

class Make:
    def __init__(self, args):
        self.NAME = args.name
        self.CC = ""
        self.RM = "rm -f"
        self.CURDIR = args.current_dir
        self.TODO = "TODO = -@fgrep --color --exclude=.git --exclude=*.o --exclude=Makefile --exclude=tags --exclude=cscope* -H -e TODO -e FIXME -r $(CURDIR) || true"
        self.SRCS = []
        self.OBJ = "$(SRCS:.c=.o)"
        self.FLAGS = []
        self.LDLIBS = ""
        self.color = args.color
        self.re = "re:\t fclean all\n"
        self.all = "all:\t$(NAME)"
        self.name = "$(NAME):\t$(OBJ)\n\t\t@$(CC) $(CFLAGS) -o $(NAME) $(OBJ) $(LDLIBS)\n\t\t@$(TODO)\n"
        self.clean = "clean:\t\n\t\t@echo \"clean OK\"\n\t\t@$(RM) $(OBJ)\n"
        self.fclean = "fclean:\t\n\t\t@echo \"fclean OK\"\n\t\t@$(RM) $(OBJ)\n\t\t@$(RM) $(NAME)\n"
        self.regle = "%.o: %.c \n\t\t@gcc -c -o $@ $(CFLAGS) $<\n\t\t@echo \"[OK] built '$@'\"\n"
        self.fclean_c = "fclean:\t\n\t\t@echo -e \"\\033[1;46m fclean OK \\033[0m\"\n\t\t@$(RM) $(OBJ)\n\t\t@$(RM) $(NAME)\n"
        self.regle_c = "%.o: %.c \n\t\t@gcc -c -o $@ $(CFLAGS) $<\n\t\t@echo -e \"[\\033[0;32m OK \\033[0m] built '$@'\"\n"
        self.clean_c = "clean:\t\n\t\t@echo -e \"\\033[1;46m clean OK \\033[0m\"\n\t\t@$(RM) $(OBJ)"
        self.phony = ".PHONY:\tre all clean fclean\n"

        if args.flags is not None:
            self.add_flag("-W -Wall -Werror -I./include/")
        else:
            self.add_flag(args.flags)

    def add_flag(self, str):
        for l in self.FLAGS:
            if str in l:
                return 1
        self.FLAGS.append(str)

    def add_srcs(self, str):
        self.SRCS.append(str)


def set_parse():
    parser = argparse.ArgumentParser("Set args for Makefile-gen")
    parser.add_argument("-o", "--name", type=str, default="programme",
                        help="set the binary name")
    parser.add_argument("-f", "--flags", type=str, default="-I./include/",
                        help="set compil flag(s)")
    parser.add_argument("-t", "--todo", action='store_false', default=False,
                        help="disable todo option")
    parser.add_argument("-c", "--color", action='store_false', default=False,
                        help="disable colors for a pretty Makefile :/")
    parser.add_argument("-C", "--current-dir", type=str, default="./",
                        help="set dir to compile")
    parser.add_argument("-l", "--lib", type=str, default="",
                        help="set lib to compile")
    args = parser.parse_args()
    print(args)
    return (args)

def parse_arg():
    args = set_parse()
    Makefile = Make(args)
    return (Makefile)

def get_file(Makefile):
    for dossier, sous_dossiers, fichiers in os.walk(Makefile.CURDIR):
        for fichier in fichiers:
            if fichier.endswith(".c") or fichier.endswith(".cpp"):
                Makefile.SRCS.append(os.path.join(dossier, fichier))
    if len(Makefile.SRCS) >= 1:
        if Makefile.SRCS[0].endswith(".c"):
            Makefile.CC = "gcc"
        elif Makefile.SRCS[1].endswith(".cpp"):
            Makefile.CC = "g++"
    else:
        print("No files found")
        sys.exit(1)
    if Makefile.FLAGS is None:
        sys.exit(84)
    return (Makefile)

def get_old(Makefile):
    if os.path.exists("Makefile"):
        with open("Makefile", "r") as old_makefile:
            text = old_makefile.read()
            for ligne in text.split("\n"):
                if ligne.startswith("NAME"):
                    if ligne.split("=")[1].startswith("\t") or ligne.split("=")[1].startswith(" "):
                        Makefile.NAME = ligne.split("=")[1][1:]
                    else:
                        Makefile.NAME = ligne.split("=")[1]
                if ligne.startswith("CFLAGS") or ligne.startswith("CPPFLAGS"):
                    if ligne.split("=")[1].startswith("\t") or ligne.split("=")[1].startswith(" "):
                        Makefile.add_flag(ligne.split("=")[1][1:])
                    else:
                        Makefile.FLAGS.append(ligne.split("=")[1])
                if ligne.startswith("LDLIBS"):
                    if ligne.split("=")[1].startswith("\t") or ligne.split("=")[1].startswith(" "):
                        Makefile.LDLIBS = ligne.split("=")[1][1:]
                    else:
                        Makefile.LDLIBS = ligne.split("=")[1]

    return(Makefile)

def write_in_file(Makefile):
        with open("Makefile", "w") as files:
            files.write("CC\t=\t" + Makefile.CC + "\n")
            if len(Makefile.FLAGS) >= 1:
                files.write("CFLAGS\t=\t" + Makefile.FLAGS[0] + "\n")
            elif len(Makefile.FLAGS) == 0:
                files.write("CFLAGS\t=\t" + "\n")
            if len(Makefile.FLAGS) >= 2:
                for arg in range(1, len(Makefile.FLAGS)):
                    files.write("CFLAGS\t+=\t" + Makefile.FLAGS[arg] + "\n")
            files.write("LDLIBS\t=" + Makefile.LDLIBS+"\n")
            files.write("\n")
            files.write("NAME\t=\t" + Makefile.NAME + "\n")
            files.write("OBJ\t=\t" + Makefile.OBJ + "\n")
            sorted(Makefile.SRCS)
            files.write("SRCS\t=\t" + str(Makefile.SRCS[0]))
            i = 0
            if len(Makefile.SRCS) == 1:
                files.write("\n")
            else:
                files.write(" \\\n")
                while i < len(Makefile.SRCS) - 1:
                    i = i + 1
                    if i == len(Makefile.SRCS) - 1:
                        files.write("\t\t" + str(Makefile.SRCS[i]) + "\n")
                    else:
                        files.write("\t\t" + str(Makefile.SRCS[i]) + " \\\n")
            files.write("\n" + Makefile.all + "\n")
            files.write("\n" + Makefile.name + "\n")
            files.write(Makefile.re)
            if Makefile.color is False:
                files.write("\n" + Makefile.clean_c + "\n")
                files.write("\n" + Makefile.fclean_c + "\n")
                files.write("\n" + Makefile.regle_c + "\n")
            else:
                files.write("\n" + Makefile.clean + "\n")
                files.write("\n" + Makefile.fclean + "\n")
                files.write("\n" + Makefile.regle + "\n")
            files.write(Makefile.phony)


if __name__ == '__main__':
    Makefile = parse_arg()
    Makefile = get_old(Makefile)
    Makefile = get_file(Makefile)
    write_in_file(Makefile)