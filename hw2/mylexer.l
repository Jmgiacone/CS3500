		               /* ---- PROLOGUE ---- */
%{
#include <iostream>
using std::cout;
using std::endl;
#define YY_DECL extern "C" int yylex()

int numLines = 0;
int numTokens = 0;
%}
		              /* ---- DEFINITIONS ---- */
%option noyywrap
COMMENT         \%.*$
DIGIT		[0-9]
INT_CONST       ("+"|"-")?{DIGIT}+
DEC_CONST       {INT_CONST}\.{DIGIT}+
SCI_CONST       {DEC_CONST}E("+"|"-")?0*[1-9]+{DIGIT}+
HEX_CONST       [A-F0-9]+H
BIN_CONST       (0|1)+B
PHN_CONST       ({DIGIT}{3}\.{DIGIT}{3}\.{DIGIT}{4}|\({DIGIT}{3}\){DIGIT}{3}-{DIGIT}{4}|{DIGIT}{3}-{DIGIT}{3}-{DIGIT}{4})
KEYWORD         (if|else|func|let|print|while)
IDENT           [a-zA-Z][a-zA-Z0-9]*
STR_CONST       \"[a-zA-Z0-9 ]*\"
OPERATOR        ("+"|"-"|"*"|"/"|"<"|">"|"&")
UNKNOWN         [^{INT_CONST}|{DEC_CONST}|{SCI_CONST}|{HEX_CONST}|{BIN_CONST}|{PHN_CONST}|{KEYWORD}|{IDENT}|{STR_CONST}|{OPERATOR}]

%%  		              /* ---- REGULAR EXPRESSIONS ---- */

\n                 { numLines++; }
{COMMENT}          ;
[ \t]              ;
{INT_CONST}        { cout << "#" << numTokens << ": TOKEN: INTCONST   LEXEME: " << yytext << endl; numTokens++; }
{DEC_CONST}        { cout << "#" << numTokens << ": TOKEN: DECCONST   LEXEME: " << yytext << endl; numTokens++; }
{SCI_CONST}        { cout << "#" << numTokens << ": TOKEN: SCICONST   LEXEME: " << yytext << endl; numTokens++; }
{HEX_CONST}        { cout << "#" << numTokens << ": TOKEN: HEXCONST   LEXEME: " << yytext << endl; numTokens++; }
{BIN_CONST}        { cout << "#" << numTokens << ": TOKEN: BINCONST   LEXEME: " << yytext << endl; numTokens++; }
{PHN_CONST}        { cout << "#" << numTokens << ": TOKEN: PHCONST    LEXEME: " << yytext << endl; numTokens++; }
{KEYWORD}          { cout << "#" << numTokens << ": TOKEN: KEYWORD    LEXEME: " << yytext << endl; numTokens++; }
{IDENT}            { cout << "#" << numTokens << ": TOKEN: IDENT      LEXEME: " << yytext << endl; numTokens++; }
{STR_CONST}        { cout << "#" << numTokens << ": TOKEN: STRCONST   LEXEME: " << yytext << endl; numTokens++; }
{OPERATOR}         { cout << "#" << numTokens << ": TOKEN: OPERATOR   LEXEME: " << yytext << endl; numTokens++; }
{UNKNOWN}          { cout << "#" << numTokens << ": TOKEN: ?          LEXEME: " << yytext << endl; numTokens++; }

%%  		              /* ---- EPILOGUE ---- */

int main()
{
    yylex();
    cout << numLines << " lines processed." << endl;
    return 0;
}
