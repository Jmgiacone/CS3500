#!/bin/bash

flex mylexer.l
g++ lex.yy.c -lfl -o lexer.ex
./lexer.ex < sampleinput.txt > myoutput.txt
diff myoutput.txt sampleoutput.txt
rm myoutput.txt
