# coding: utf-8
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
from lexer import Lexer

# ----------------------------------------------------------------------
# Obtener los nodos AST.
# Lea las instrucciones en ast.py 
from cast import *

class Parser(sly.Parser):
	debugfile = 'parser.txt'

	tokens = Lexer.tokens
	
	precedence = (
		('nonassoc', 'LOWER'),
		('nonassoc', ELSE),
			('right', '='),
			('left', OR),
			('left', AND),
			('left', EQ, NE),
			('left', LE,'<', GE,'>'),
			('left', DE, ME, PE, TE, MDE, ),
			('left', '-','+'),
			('left','*','/','%'),
			('right', '!', 'UMINUS', 'UPLUS'),
			('left','(',')','[',']','.'),
	)


	@_('decl_list')
	def program(self, p):
		return Program(p.decl_list)
		
	@_('decl_list decl')
	def decl_list(self, p):
		p.decl_list.append(p.decl)
		return p.decl_list
		
	@_('decl')
	def decl_list(self, p):
		return [p[0]]
		
	@_('var_decl','fun_decl','const_decl')
	def decl(self,p):
		return p[0]
		
	@_('CONST IDENT "=" expr ";"')
	def const_decl(self,p):
		return ConstDeclaration(p.IDENT, p.expr,lineno=p.lineno)
		
	@_('type_spec IDENT ";" ')
	def var_decl(self,p):
		return VarDeclaration(p.IDENT,p.type_spec, None,lineno=p.lineno)
		
	@_('type_spec IDENT "=" expr ";"')
	def var_decl(self,p):
		return VarDeclaration(p.IDENT,p.type_spec, p.expr,lineno=p.lineno)
		
	@_('type_spec IDENT "[" "]" ";" ')
	def var_decl(self,p):
		return ArrayDeclaration(p.IDENT,p.type_spec,lineno=p.lineno)
		
	@_('BOOL', 'INT', 'FLOAT', 'VOID','CHAR')
	def type_spec(self,p):
		return SimpleType(p[0],lineno=p.lineno)
		
	@_('type_spec IDENT "(" params ")" compound_stmt')
	def fun_decl(self,p):
		return FuncDeclaration(p.IDENT,p.params,p.type_spec,p[5],lineno=p.lineno)
		
	@_('param_list')
	def params(self,p):
		return p.param_list
		
	@_('VOID')
	def params(self,p):
		return []
		
	@_('param_list "," param')
	def param_list(self,p):
		p.param_list.append(p.param)
		return p.param_list
		
	@_('param')
	def param_list(self,p):
		return [p.param]
		
	@_('type_spec IDENT')
	def param(self,p):
		return FuncParameter(p[1],p[0],lineno=p.lineno)
		
	@_('type_spec IDENT "[" "]"')
	def param(self,p):
		return FuncParameter(p[1],p[0],lineno=p.lineno)
		
	@_('"{" local_decls stmt_list "}"')
	def compound_stmt(self,p):
		return Compound_Stmt(p.local_decls,p.stmt_list,lineno=p.lineno)
		
	@_('local_decls local_decl')
	def local_decls(self,p):
		p.local_decls.append(p.local_decl)
		return p.local_decls
		
	@_('empty')
	def local_decls(self,p):
		return []
		
	@_('type_spec IDENT ";" ')
	def local_decl(self,p):
		return LocalDecl(p[1],p[0],None,lineno=p.lineno)
		
	@_('type_spec IDENT "=" expr ";"')
	def local_decl(self,p):
		return LocalDecl(p[1],p[0],p.expr,lineno=p.lineno)
		
	@_('type_spec IDENT "[" "]" ";" ')
	def local_decl(self,p):
		return ArrayLocalDecl(p[1],p[0],None,lineno=p.lineno)
		
	@_('stmt_list stmt')
	def stmt_list(self,p):
		p.stmt_list.append(p.stmt)
		return p.stmt_list
		
	@_('empty')
	def stmt_list(self,p):
		return []
		
	@_( 'expr_stmt', 'compound_stmt', 'if_stmt', 'while_stmt', 'for_stmt', 'return_stmt', 'break_stmt')
	def stmt(self,p):
		return p[0]
		
	@_('expr ";" ')
	def expr_stmt(self,p):
		return p[0]
		
	@_('";"')
	def expr_stmt(self,p):
		return Null_Stmt(None)
		
	@_('WHILE "(" expr ")"  compound_stmt ')
	def while_stmt(self,p):
		return While_Stmt(p.expr,p.compound_stmt ,lineno=p.lineno)

	@_("FOR '(' var_decl expr_stmt expr ')' compound_stmt ")
	def for_stmt(self):
		return ForStmt(p.var_decl, p.expr_stmt, p.expr, p.compound_stmt, lineno=p.lineno)
		
	@_('IF "(" expr ")" stmt ELSE  stmt')
	def if_stmt(self,p):
		return If_Stmt(p.expr,p[4],p[6],lineno=p.lineno)
		
	@_('IF "(" expr ")"  stmt %prec LOWER')
	def if_stmt(self,p):
		return If_Stmt(p.expr,p.stmt,None,lineno=p.lineno)
		
	@_('RETURN ";" ')
	def return_stmt(self,p):
		return Return_Stmt(None,lineno=p.lineno)
		
	@_('RETURN expr ";" ')
	def return_stmt(self,p):
		return Return_Stmt(p[1],lineno=p.lineno)
		
	@_('BREAK ";" ')
	def break_stmt(self,p):
		return Break_Stmt(None,lineno=p.lineno)
		
	@_('IDENT')
	def location(self,p):
		return SimpleLocation(p[0],lineno=p.lineno)
		
	@_('IDENT "[" expr "]"')
	def location(self,p):
		return ArraySimpleLocation(p[0],p[2],lineno=p.lineno)
		
	@_('location "=" expr')
	def expr(self,p):
		return WriteLocation(p[0],p.expr,lineno=p.lineno)
		
	@_('expr OR expr', 'expr AND expr', 'expr EQ expr', 'expr NE expr', 'expr LE expr', 'expr "<" expr', 'expr GE expr', 'expr ">" expr','expr ME expr','expr PE expr','expr DE expr','expr TE expr','expr MDE expr')
	def expr(self,p):
		return BinOp(p[1],p[0],p[2],lineno=p.lineno)
		
	@_('expr "+" expr', 'expr "-" expr', 'expr "*" expr', 'expr "/" expr', 'expr "%" expr')
	def expr(self,p):
		return BinOp(p[1],p[0],p[2],lineno=p.lineno)
		
	@_('"-" expr %prec UMINUS','"+" expr %prec UPLUS','"!" expr','ADD expr %prec UMINUS','SUB expr %prec UPLUS')
	def expr(self,p):
		return UnaryOp(p[0],p[1],lineno=p.lineno)

	@_('expr ADD %prec UMINUS','expr SUB %prec UPLUS')
	def expr(self,p):
		return UnaryOp(p[1],p[0],lineno=p.lineno)
		
	@_('"(" expr ")"')
	def expr(self,p):
		return p.expr
		
	@_('location')
	def expr(self,p):
		return ReadLocation(p[0])
		
	@_('IDENT "(" args ")"')
	def expr(self,p):
		return FuncCall(p.IDENT,p.args,lineno=p.lineno)
		
	@_('IDENT "." SIZE')
	def expr(self,p):
		pass
		
	@_('BOOL_LIT')
	def expr(self,p):
		return BoolLiteral(p.BOOL_LIT,lineno=p.lineno)
		
	@_('INT_LIT')
	def expr(self,p):
		return IntegerLiteral(p.INT_LIT,lineno=p.lineno)
		
	@_('FLOAT_LIT')
	def expr(self,p):
		return FloatLiteral(p.FLOAT_LIT,lineno=p.lineno)
		
	@_('CHAR_LIT')
	def expr(self,p):
		return CharLiteral(p[0],lineno=p.lineno)

	@_('STRING_LIT')
	def expr(self,p):
		return StringLiteral(p[0],lineno=p.lineno)
		
	@_('NEW type_spec "[" expr "]"')
	def expr(self,p):
		return NewArrayExpr(p[1], p[3],lineno=p.lineno)
		
	@_('arg_list "," expr')
	def arg_list(self,p):
		p[0].append(p[2])
		return p[0]
		
	@_('expr')
	def arg_list(self,p):
		return [p[0]]
		
	@_('arg_list')
	def args(self,p):
		return p[0]
		
	@_('empty')
	def args(self,p):
		return []
		
	@_(' ')
	def empty(self,p):
		return Null_Stmt(None)

	# ----------------------------------------------------------------------
	# NO MODIFIQUE
	#
	# manejo de errores catch-all. Se llama a la siguiente función en 
	# cualquier entrada incorrecta. p es el token ofensivo o None si 
	# el final de archivo (EOF).
	def error(self, p):
		if p:
			error(p.lineno, "Error de sintaxis en la entrada en el token '%s'" % p.value)
		else:
			error('EOF','Error de sintaxis. No mas entrada.')
			
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
