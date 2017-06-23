import os, sys
import argparse
import time
import getpass

from threading import Thread, RLock

lock = RLock()

class Makefile(object):
    """docstring for makefile."""
    def __init__(self):
        super(Makefile, self).__init__()
        self.name = ""
        self.ldlibs = ""
        self.srcs = []
        self.flags = []


    def add_src(self, s):
        for l in self.srcs:
            if s in l:
                return 1
        self.srcs.append(s)

    def add_flag(self, f):
        for l in self.flags:
            if f in l:
                return 1
        self.flags.append(f)
    def set_name(self, name):
        self.name = name

class Read_makefile(Thread, Makefile):
    """docstring for Read_makefile."""
    def __init__(self):
        Thread.__init__(self)
        Makefile.__init__(self)
        super(Read_makefile, self).__init__()
    def run(self):
        with lock:
            if os.path.exists("Makefile"):
                with open("Makefile", "r") as old_makefile:
                    text = old_makefile.read()
                    for ligne in text.split("\n"):
                        if ligne.startswith("NAME"):
                            if ligne.split("=")[1].startswith("\t") or ligne.split("=")[1].startswith(" "):
                                self.set_name(ligne.split("=")[1][1:])
                            else:
                                self.set_name = ligne.split("=")[1]
                        if ligne.startswith("CFLAGS") or ligne.startswith("CPPFLAGS"):
                            if ligne.split("=")[1].startswith("\t") or ligne.split("=")[1].startswith(" "):
                                self.add_flag(ligne.split("=")[1][1:])
                            else:
                                self.append(ligne.split("=")[1])
                        if ligne.startswith("LDLIBS"):
                            if ligne.split("=")[1].startswith("\t") or ligne.split("=")[1].startswith(" "):
                                ldlibs = ligne.split("=")[1][1:]
                            else:
                                ldlibs = ligne.split("=")[1]


class New_makefile(Makefile):
    """docstring for New_makefile."""
    def __init__(self, arg):
        super(New_makefile, self).__init__()
        self.arg = arg

class Parse(Thread):
    """docstring for parse arguments"""
    def __init__(self):
        super(Parse, self).__init__()
        Thread.__init__(self)

    def run(self):
        with lock:
            self.parser = argparse.ArgumentParser("Set args for Makefile-gen")
            self.parser.add_argument("-o", "--name", type=str, default="program",
                help="set the binary name")
            self.parser.add_argument("-f", "--flags", type=str, default="-I./include/",
                help="set compil flag(s)")
            self.parser.add_argument("-t", "--todo", action='store_false', default=False,
                help="disable todo option")
            self.parser.add_argument("-c", "--color", action='store_false', default=False,
                help="disable colors for a pretty Makefile :/")
            self.parser.add_argument("-C", "--current-dir", type=str, default="./",
                help="set dir to compile")
            self.parser.add_argument("-l", "--lib", type=str, default="",
                help="set lib to compile")
            self.parser.add_argument("-I", "--include", type=str, default="./include/",
                help="set include dir")
    def get_args(self):
        return self.parser.parse_args()

if __name__ == '__main__':
    r = Read_makefile()
    p = Parse()
    p.run()
    r.start()
    p.start()
    r.join()
    p.join()
    print(r.flags)
    print(p.get_args())
    """make_new = Makefile()
    make_old = Makefile()
    p = Parse()
    p.start()
    print(p.get_args())
    p.join()"""
