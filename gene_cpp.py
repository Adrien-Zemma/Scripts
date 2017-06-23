#!/usr/bin/python3.6
import os
import re
import sys
import glob
import pwd
import time
import getpass

class Make:
    def __init__(self):
        self.NAME = "programme"
        self.CC = ""
        self.RM = "rm -f"
        self.CURDIR = "./"
        self.TODO = "TODO = -@fgrep --color --exclude=.git --exclude=*.o --exclude=Makefile --exclude=tags --exclude=cscope* -H -e TODO -e FIXME -r $(CURDIR) || true"
        self.SRCS = []
        self.OBJ = "$(SRCS:.c=.o)"
        self.FLAGS = []
        self.LDLIBS = ""
        self.color = 1
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

def parse_arg(Makefile):
    compte = len(sys.argv)
    if compte >= 2:
        i = 1
        while i < compte:
            if (sys.argv[i][0] == "-"):
                if sys.argv[i] == "-o" and i + 1 < compte:
                    Makefile.NAME = sys.argv[i + 1]
                elif sys.argv[i] == "-f" and i + 1 < compte:
                    Makefile.CFLAGS = sys.argv[i + 1]
                elif sys.argv[i] == "-t" and i + 1 < compte and sys.argv[i + 1] == "off":
                    Makefile.TODO = ""
                elif sys.argv[i] == "-c":
                    Makefile.color = 0
                elif sys.argv[i] == "-F" and i + 1 < compte:
                    Makefile.CURDIR = sys.argv[i + 1]
                elif sys.argv[i] == "-l" and i + 1 < compte:
                    Makefile.LDLIBS = sys.argv[i + 1]
                elif sys.argv[i] == "-i" and i + 1 < compte:
                    Makefile.FLAGS.append("-I./" + sys.argv[i + 1])
            i = i + 1
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
        print("aucun fichier trouvé")
        exit()
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
                        Makefile.FLAGS.append(ligne.split("=")[1][1:])
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
            if Makefile.color:
                files.write("\n" + Makefile.clean_c + "\n")
                files.write("\n" + Makefile.fclean_c + "\n")
                files.write("\n" + Makefile.regle_c + "\n")
            else:
                files.write("\n" + Makefile.clean + "\n")
                files.write("\n" + Makefile.fclean + "\n")
                files.write("\n" + Makefile.regle + "\n")
            files.write(Makefile.phony)

def main():
    Makefile = Make()
    Makefile = get_old(Makefile)
    Makefile = parse_arg(Makefile)
    Makefile = get_file(Makefile)
    write_in_file(Makefile)


main()
