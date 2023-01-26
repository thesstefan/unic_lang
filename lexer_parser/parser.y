%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1
%}

%token COMMA		  
%token OPEN_SQUARE_BRACKET
%token CLOSED_SQUARE_BRACKET
%token OPEN_ROUND_BRACKET    
%token CLOSED_ROUND_BRACKET
%token OPEN_BRACE		  
%token CLOSED_BRACE		  
%token COLON				  
%token SEMICOLON			 
%token PLUS			  
%token MINUS				  
%token MULTIPLY             
%token DIVIDE				  
%token MOD                 
%token ASSIGNMENT_OP        
%token BOOL                  
%token CHAR                  
%token INTEGER               
%token INT                   
%token STRING                
%token STR                  
%token RELATION_OP        
%token LET                  
%token IF                   
%token ELSE                 
%token WHILE                 
%token INPUT                 
%token OUTPUT               
%token VEC                 
%token RETURN              
%token ID               
%token CHARACTER			 

%start Program

%% 
Program : Stmt | Stmt Program ;
Stmt : Simplestmt | Structstmt ;
Simplestmt : Decllist | Assignment | Iostmt | Returnstmt ;
Returnstmt : RETURN SEMICOLON ;
Assignment : Identifier ASSIGNMENT_OP Expression SEMICOLON ;
Structstmt : Ifstmt | Whilestmt ;
Whilestmt : WHILE OPEN_ROUND_BRACKET Condition CLOSED_ROUND_BRACKET OPEN_BRACE Program CLOSED_BRACE ;
Ifstmt : IF OPEN_ROUND_BRACKET Condition CLOSED_ROUND_BRACKET OPEN_BRACE Program CLOSED_BRACE | IF OPEN_ROUND_BRACKET 
	 Condition CLOSED_ROUND_BRACKET OPEN_BRACE Program CLOSED_BRACE ELSE OPEN_BRACE Program CLOSED_BRACE ;
Condition : Expression RELATION_OP Expression ;
Iostmt : INPUT OPEN_ROUND_BRACKET Identifier CLOSED_ROUND_BRACKET SEMICOLON | OUTPUT OPEN_ROUND_BRACKET IdentifierList 
	 CLOSED_ROUND_BRACKET SEMICOLON | OUTPUT OPEN_ROUND_BRACKET STRING COMMA IdentifierList CLOSED_ROUND_BRACKET SEMICOLON ;
Factor : Identifier | OPEN_ROUND_BRACKET Expression CLOSED_ROUND_BRACKET ;
Term : Factor | Factor MULTIPLY Term | Factor DIVIDE Term | Factor MOD Term ;
Expression : Term | Term PLUS Expression | Term MINUS Expression ;
Decllist : Declaration | Declaration COMMA Decllist ;
Declaration : LET Identifier COLON Type SEMICOLON ;
Type : Type1 | Arraydecl ;
Arraydecl : VEC OPEN_ROUND_BRACKET INT SEMICOLON Type1 CLOSED_ROUND_BRACKET SEMICOLON ;
Type1 : BOOL | CHAR | INT | STRING ;
IdentifierList : Identifier | Identifier COMMA IdentifierList ;
Identifier : ID | CHARACTER | STR | INTEGER ;

%%

yyerror(char *s)
{	
	printf("%s\n", s);
}

extern FILE* yyin;

int main(int argc, char **argv)
{
	if ( argc > 1 ) {
	    yyin = fopen(argv[1], "r");
	}
	if ( !yyparse() ) {
	    fprintf(stderr, "SUCCESS\n");
	}
} 
