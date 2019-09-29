# coding: utf-8

import cast

r'''
Proyecto 2: Escribir un analizador
==================================
En este proyecto, escribes el shell básico de un analizador para MiniC.
A continuación se incluye la forma BNF del lenguaje. Su tarea es escribir
las reglas de análisis y construir el AST para esta gramática usando SLY.
La siguiente gramática es parcial. Se agregan más características en
proyectos posteriores.

	program : decl_list
	
	decl_list : decl_list decl 
			| decl
					
	decl : var_decl 
			| fun_decl
			
	var_decl : type_spec IDENT ;
			| type_spec IDENT [ ] ;

	type_spec : VOID 
			| BOOL 
			| INT 
			| FLOAT

	fun_decl : type_spec IDENT ( params ) compound_stmt

	params : param_list 
			| VOID 
	
	param_list : param_list , param 
			| param

	param : type_spec IDENT 
			| type_spec IDENT [ ]
	
	compound_stmt : { local_decls stmt_list }
	
	local_decls : local_decls local_decl 
			| empty
			
	local_decl : type_spec IDENT ; 
			| type_spec IDENT [ ] ;

	stmt_list : stmt_list stmt 
			| empty
			
	stmt : expr_stmt 
			| compound_stmt 
			| if_stmt 
			| while_stmt 
			| return_stmt 
			| break_stmt 
	
	expr_stmt : expr ; 
			| ;

	while_stmt : WHILE ( expr ) stmt

	if_stmt : IF ( expr ) stmt 
			| IF ( expr ) stmt ELSE stmt

	return_stmt : RETURN ; 
			| RETURN expr ;
			
	break_stamt : BREAK ;

	expr : IDENT = expr | IDENT[ expr ] = expr
			| expr OR expr
			| expr AND expr
			| expr EQ expr | expr NE expr
			| expr LE expr | expr < expr | expr GE expr | expr > expr
			| expr + expr | expr - expr
			| expr * expr | expr / expr | expr % expr
			| ! expr | - expr | + expr
			| ( expr )
			| IDENT | IDENT[ expr ] | IDENT( args ) | IDENT . size
			| BOOL_LIT | INT_LIT | FLOAT_LIT | NEW type_spec [ expr ]

	arg_list : arg_list , expr 
			| expr 
	
	args : arg_list 
			| empty


Para hacer el proyecto, siga las instrucciones que siguen a continuación.
'''
# ----------------------------------------------------------------------
# Analizadores son definidos usando SLY.  Se hereda de la clase Parser
#
# vea http://sly.readthedocs.io/en/latest/
# ----------------------------------------------------------------------
import sly

# ----------------------------------------------------------------------
# El siguiente import carga la función error(lineno, msg) que se debe
# usar para informar todos los mensajes de error emitidos por su analizador. 
# Las pruebas unitarias y otras características del compilador se basarán 
# en esta función. Consulte el archivo errors.py para obtener más 
# documentación sobre el mecanismo de manejo de errores.
from errors import error

# ------------------------------------------------- ---------------------
# Importar la clase lexer. Su lista de tokens es necesaria para validar y 
# construir el objeto analizador.
from clex import Lexer

# ----------------------------------------------------------------------
# Obtener los nodos AST.
# Lea las instrucciones en ast.py 
from cast import *

class Parser(sly.Parser):
	debugfile = 'parser.txt'

	tokens = Lexer.tokens
	
	precedence = (
	)

	@_("decl_list")
	def program(self, p):
		pass
	@_("decl_list decl")
	def decl_list(self, p):
		pass

	@_("decl")
	def decl_list(self, p):
		pass

	@_("var_decl")
	def decl(self, p):
		pass

	@_("fun_decl")
	def decl(self, p):
		pass  
			 
	@_("type_spec IDENT ';'")
	def var_decl(self, p):
		pass

	@_("type_spec IDENT '[' ']' ';'")
	def var_decl(self, p):
		pass

	@_("VOID", "BOOL", "INT", "FLOAT")
	def type_spec(self, p):
		pass

	@_("type_spec IDENT '(' params ')' compound_stmt")
	def fun_decl(self, p):
		pass

	@_("param_list")
	def params(self, p):
		pass

	@_("VOID")
	def params(self, p):
		pass

	@_("param_list , param")
	def param_list(self, p):
		pass

	@_("param")
	def param_list(self, p):
		pass

	@_("type_spec IDENT")
	def param(self, p):
		pass
	
	@_("type_spec IDENT '[' ']'")
	def param(self, p):
		pass

	@_("'{' local_decls stmt_list '}'")
	def compound_stmt(self, p):
		pass

	@_("local_decls local_decl")
	def local_decls(self, p):
		pass

	@_("empty")
	def local_decls(self, p):
		pass
			| 
	@_("type_spec IDENT ';'")
	def local_decl(self, p):
		pass

	@_("type_spec IDENT '[' ']' ';'")
	def local_decl(self, p):
		pass

	@_("stmt_list stmt")
	def stmt_list(self, p):
		pass

	@_("empty")
	def stmt_list(self, p):
		pass

	@_("expr_stmt")
	def stmt(self, p):
		pass

	@_("compound_stmt")
	def stmt(self, p):
		pass 

	@_("if_stmt")
	def stmt(self, p):
		pass 

	@_("while_stmt")
	def stmt(self, p):
		pass 

	@_("return_stmt")
	def stmt(self, p):
		pass 

	@_("break_stmt")
	def stmt(self, p):
		pass  

	@_("expr ';'")
	def expr_stmt(self, p):
		pass

	@_("';'")
	def expr_stmt(self, p):
		pass
	
	@_("WHILE '(' expr ')' stmt")
	def while_stmt(self, p):
		pass

	@_("IF '(' expr ')' stmt")
	def if_stmt(self, p):
		pass

	@_("IF '(' expr ')' stmt ELSE stmt")
	def if_stmt(self, p):
		pass

	@_("RETURN ';'")
	def return_stmt(self, p):
		pass

	@_("RETURN expr ';'")
	def return_stmt(self, p):
		pass
			
	@_("BREAK ';'")
	def break_stmt(self, p):
		pass 
	
	

	# ----------------------------------------------------------------------
	# NO MODIFIQUE
	#
	# manejo de errores catch-all. Se llama a la siguiente función en 
	# cualquier entrada incorrecta. p es el token ofensivo o None si 
	# el final de archivo (EOF).
	def error(self, t):
		if p:
			error(p.lineno, "Error de sintaxis en la entrada en el token '%s'" % p.value)
		else:
			error('EOF','Error de sintaxis. No mas entrada.')

	@_("IF '(' expr ') stmt")
	def ifstmt(self, p):
		return IfStmt(p.expr, p.stmt)

	@_("WHILE '(' expr ')' stmt")
	def whilestmt(self, p):
		return WhileStmt(p.expr, p.stmt)

	@_("expr + expr", "expr - expr", "expr * expr", "expr / expr")
	def binOperator(self, p):
		return Binop(p[1], p.expr0, p.expr1)

	@_("+expr", "-expr", "!expr")
	def unitaryOperator(self, p):
		return UnitaryOperator(p[0], p.expr)

	@_("expr = expr")
	def varAssignment(self, p):
		return VarAssignmentExpression(p.expr0, p.expr1)

	@_(";")
	def expr(self, p):
		return NullStatement()

	@_("expr '[' expr ']' = expr")
	def arrayAsignment(self, p):
		return ArrayAssignmentExpression(p.expr0, p.expr1, p.expr2)
	
			
# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA A CONTINUACIÓN
# ----------------------------------------------------------------------

def parse(source):
	'''
	Parser el código fuente en un AST. Devuelve la parte superior del árbol AST.
	'''
	lexer  = Lexer()
	parser = Parser()
	ast = parser.parse(lexer.tokenize(source))
	return ast
	
def main():
	'''
	Programa principal. Usado para probar.
	'''
	import sys
	
	if len(sys.argv) != 2:
		sys.stderr.write('Uso: python -m minic.parser filename\n')
		raise SystemExit(1)

	# Parse y crea el AST
	ast = parse(open(sys.argv[1]).read())

	# Genera el árbol de análisis sintáctico resultante
	for depth, node in flatten(ast):
		print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))
		
if __name__ == '__main__':
	main()
