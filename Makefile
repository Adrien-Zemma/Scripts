##
## Makefile for tekadventure in /home/nodyn/Projects/Epitech/MUL/tekadventure
##
## Made by Neil Cecchini
## Login   <nodyn@epitech.eu>
##
## Started on  Mon Apr 10 15:01:01 2017 Neil Cecchini
## Last update Wed May 31 16:17:24 2017 adrien
##

CC	= gcc
CFLAGS	= -Wall -Wextra -g3
CPPFLAGS= -Iinclude
LDLIBS	= -lc_graph_prog_full -lm

NAME	= tekadventure
OBJ	= $(patsubst src/%.c,obj/%.o,$(SRC))
SRC	= src/animations.c \
	  src/graph/debug.c \
	  src/graph/main.c \
	  src/main.c \
	  src/dialogue/dialogue.c \
	  src/map.c \
	  src/player/create.c \
	  src/player/destroy.c \
	  src/player/update.c \
	  src/window.c

all: $(NAME)

re: fclean all

auto: re clean

run: auto
	@echo "running main binary..."
	@./$(NAME)

$(NAME): $(OBJ)
	@gcc -o $@ $(CFLAGS) $(CPPFLAGS) $^ $(LDLIBS)
	@echo "linked '$@'"

clean:
	@-rm -vf $(OBJ)
	@-rm -rf obj

fclean: clean
	@-rm -vf $(NAME)

obj/%.o: src/%.c
	@-mkdir -p $(shell dirname $@)
	@gcc -c -o $@ $(CFLAGS) $(CPPFLAGS) $< $(LDLIBS)
	@echo "built '$@'"

.PHONY: re auto run all clean fclean
