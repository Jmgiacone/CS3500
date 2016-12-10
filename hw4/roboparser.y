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
/* NOTE: Bison likes the start symbol to be the first rule */
routineSequence : /* empty */ { cout << "RULE: RoutineSequence ::= empty" << endl; }
                | routineDeclaration  { cout << "RULE: RoutineSequence ::= RoutineDeclaration" << endl; }
	        | routineDeclaration  routineSequence { cout << "RULE: RoutineSequence ::= RoutineDeclaration RoutineSequence" << endl; }
                ;

routineDeclaration : K_PROG T_IDENT K_BLIP statementSequence K_BLORP { cout << "RULE: RoutineDeclaration ::= prog identifier blip StatementSequence blorp" << endl; }
                   ;

statementSequence : statement { cout << "RULE: StatementSequence ::= Statement" << endl; } 
                  | statement statementSequence { cout << "RULE: StatementSequence ::= Statement StatementSequence" << endl; } 
             ;

statement : /* empty */   { cout << "RULE: Statement ::= empty" << endl; } 
	  | assignment    { cout << "RULE: Statement ::= Assignment" << endl; }
          | ifStatement   { cout << "RULE: Statement ::= IfStatement" << endl; }
          | loopStatement { cout << "RULE: Statement ::= LoopStatement" << endl; }
          | fwdStatement  { cout << "RULE: Statement ::= FwdStatement" << endl; }
          | rotStatement  { cout << "RULE: Statement ::= RotStatement" << endl; }
          ;

loopStatement : K_WHILE K_LPAREN expression K_RPAREN statementSequence K_ENDW { cout << "RULE: LoopStatement ::= while ( Expression ) StatementSequence endw" << endl;}
	      ;

ifStatement : K_IF K_LPAREN expression K_RPAREN statementSequence K_ENDIF { cout << "RULE: IfStatement ::= if ( Expression ) StatementSequence endif" << endl; }
	    | K_IF K_LPAREN expression K_RPAREN statementSequence K_ELSE statementSequence K_ENDIF {cout << "RULE: IfStatement ::= if ( Expression ) StatementSequence else StatementSequence endif" << endl; }
            ;

rotStatement : K_ROTATE K_LPAREN expression K_RPAREN K_BANG { cout << "RULE: RotStatement ::= rotate ( Expression ) !" << endl; }
             ;


fwdStatement : K_FORWARD K_LPAREN expression K_RPAREN K_BANG { cout << "RULE: FwdStatement ::= forward ( Expression ) !" << endl; }
             ;

assignment : T_IDENT K_IS expression K_BANG { cout << "RULE: Assignment ::= identifier is Expression !" << endl; }
           ;

factor : T_INTEGER { cout << "RULE: Factor ::= integer" << endl; }
       | T_DECIMAL { cout << "RULE: Factor ::= decimal" << endl; }
       | T_IDENT { cout << "RULE: Factor ::= identifier" << endl; }
       | K_LPAREN expression K_RPAREN { cout << "RULE: Factor ::= ( Expression )" << endl; }
       | K_NEG factor { cout << "RULE: Factor ::= ~ Factor" << endl; }
       ;

term : factor { cout << "RULE: Term ::= Factor" << endl; }
     | factor T_MULOPERATOR term { cout << "RULE: Term ::= Factor MulOperator Term" << endl; }
     ;

simpleExpression : term { cout << "RULE: SimpleExpression ::= Term" << endl; }
		 | term T_ADDOPERATOR simpleExpression { cout << "RULE: SimpleExpression ::= Term AddOperator SimpleExpression" << endl; }
                 ;

expression : simpleExpression { cout << "RULE: Expression ::= SimpleExpression" << endl;}
	   | simpleExpression T_RELATION simpleExpression { cout << "RULE: Expression ::= SimpleExpression Relation SimpleExpression" << endl; }
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
  int failcode = yyparse();


  if (failcode)
    cout << "INVALID!" << endl;
  else          
    cout << "CORRECT" << endl;
  return 0;
}

