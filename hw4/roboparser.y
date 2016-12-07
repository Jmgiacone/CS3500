%{
#include <iostream>
using std::cout;
using std::endl;


// Things from Flex that Bison needs to know
extern int yylex();
extern int line_num;
extern char* yytext;


// Prototype for Bison's error message function 
int yyerror(const char *p);
%}


//-- TOKEN DEFINITIONS --
// what tokens to expect from Flex 
%token T_INTEGER
%token T_DECIMAL
%token T_IDENT
%token T_RELATION
%token T_ADDOPERATOR
%token T_MULOPERATOR
%token K_IS
%token K_NEG
%token K_LPAREN
%token K_RPAREN
%token K_BANG
%token K_FORWARD
%token K_ROTATE
%token K_IF
%token K_ENDIF
%token K_ELSE
%token K_WHILE
%token K_ENDW
%token K_PROG
%token K_BLIP
%token K_BLORP



%%
//-- GRAMMAR RULES ---------------------------------------------
/* NOTE: Bison likes the start symbol to be the first rule
 */
routineSeq : routineDec { cout << "RULE: routineSeq ::= routineDec" << endl; }
	   | routineDec routineDec { cout << "RULE: routineSeq ::= routineDec routineDec" << endl; }
           ;

routineDec : K_PROG T_IDENT K_BLIP K_BLORP { cout << "RULE: routineDec ::= prog ident blip" << endl; }
	   | K_PROG T_IDENT K_BLIP statementSequence K_BLORP { cout << "RULE: routineDec ::= prog ident blip statementSequence blorp" << endl; }
           ;

statementSequence : statement { cout << "RULE: statementSeq ::= statement" << endl; } 
                  | statement statementSequence { cout << "RULE: statementSeq ::= statement statementSeq" << endl; } 
             ;

statement : /* empty */   { cout << "RULE: statement ::= empty" << endl; } 
	  | assignment    { cout << "RULE: statement ::= assignment" << endl; }
          | ifStatement   { cout << "RULE: statement ::= ifStatement" << endl; }
          | loopStatement { cout << "RULE: statement ::= loopStatement" << endl; }
          | fwdStatement  { cout << "RULE: statement ::= fwdStatement" << endl; }
          | rotStatement  { cout << "RULE: statement ::= rotStatement" << endl; }
          ;

loopStatement : K_WHILE K_LPAREN expression K_RPAREN statementSequence K_ENDW { cout << "RULE: loopStatement ::= while ( expression ) statementSequence endw" << endl;}
	      ;

ifStatement : K_IF K_LPAREN expression K_RPAREN statementSequence K_ENDIF { cout << "RULE: ifStatement ::= if ( expression ) statementSequence endif" << endl; }
	    | K_IF K_LPAREN expression K_RPAREN statementSequence K_ELSE statementSequence K_ENDIF {cout << "RULE: ifStatement ::= if ( expression ) statementSequence else statementSequence endif" << endl; }
            ;

rotStatement : K_ROTATE K_LPAREN expression K_RPAREN K_BANG { cout << "RULE: rotStatement ::= rotate ( expression )" << endl; }
             ;

fwdStatement : K_FORWARD K_LPAREN expression K_RPAREN K_BANG { cout << "RULE: fwdStatement ::= forward ( expression ) !" << endl; }
             ;

assignment : T_IDENT K_IS expression K_BANG { cout << "RULE: Assignment ::= ident is expresion !" << endl; }
           ;

factor : T_INTEGER { cout << "RULE: factor ::= T_INTEGER" << endl; }
       | T_DECIMAL { cout << "RULE: factor ::= T_DECIMAL" << endl; }
       | T_IDENT { cout << "RULE: factor ::= T_IDENT" << endl; }
       | K_LPAREN expression K_RPAREN { cout << "RULE: factor ::= ( expression )" << endl; }
       | K_NEG factor { cout << "RULE: factor := ~factor" << endl; }
       ;

term : factor { cout << "RULE: term ::= factor" << endl; }
     | factor T_MULOPERATOR factor { cout << "RULE: term ::= factor MUL_OPERATOR factor" << endl; }
     ;

simpleExpression : term { cout << "RULE: simpleExpression ::= term" << endl; }
		 | term T_ADDOPERATOR term { cout << "RULE: simpleExpression ::= term add_operator term" << endl; }
                 ;

expression : simpleExpression { cout << "RULE: expression ::= simpleExpression" << endl;}
	   | simpleExpression T_RELATION simpleExpression { cout << "RULE: expression ::= simpleExpression relation simpleExpression" << endl; }
           ;

%%
//-- FUNCTION DEFINITIONS -------------------------------------
int yyerror(const char *p)
{
  cout << "ERROR: In line " << line_num << " with token \'" 
       << yytext << "\'" << endl;
}


int main()
{
  int failcode;
  cout << "Hello Flex + Bison" << endl;
  failcode = yyparse();


  if (failcode)
    cout << "INVALID!" << endl;
  else          
    cout << "CORRECT" << endl;
  return 0;
}

