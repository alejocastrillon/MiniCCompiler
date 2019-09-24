# Nodos Abstract Syntax Tree (AST)
class AST(object):
	_nodes = { }
	
	@classmethod
	def __init_subclass__(cls):
		AST._nodes[cls.__name__] = cls
		
		if not hasattr(cls, '__annotations__'):
			return
			
		fields = list(cls.__annotations__.items())
		
		def __init__(self, *args, **kwargs):
			if len(args) != len(fields):
				raise TypeError(f'{len(fields)} argumentos esperados')
			for (name, ty), arg in zip(fields, args):
				if isinstance(ty, list):
					if not isinstance(arg, list):
						raise TypeError(f'{name} debe ser una lista')
					if not all(isinstance(item, ty[0]) for item in arg):
						raise TypeError(f'Todos los tipos de {name} deben ser {ty[0]}')
				elif not isinstance(arg, ty):
					raise TypeError(f'{name} debe ser {ty}')
				setattr(self, name, arg)
				
			for name, val in kwargs.items():
				setattr(self, name, val)
				
		cls.__init__ = __init__
		cls._fields = [name for name,_ in fields]
		
	def __repr__(self):
		vals = [ getattr(self, name) for name in self._fields ]
		argstr = ', '.join(f'{name}={type(val).__name__ if isinstance(val, AST) else repr(val)}'
		for name, val in zip(self._fields, vals))
		return f'{type(self).__name__}({argstr})'

# Nodos Abstract del AST
class Statement(AST):
	pass
	
class Expression(AST):
	pass
	
class Literal(Expression):
	'''
	Un valor literal como 2, 2.5, o "dos"
	'''
	pass

class Location(AST):
	pass

# Nodos Reales del AST

class NumLiteral(Literal):
	value : float
		
class Binop(Expression):
	'''
	Un operador binario como 2 + 3 o x * y
	'''
	op    : str
	left  : Expression
	right : Expression

class UnitaryOperator(Expression):
    op: str
    value: Expression

class SimpleLocation(Location):
	name : str
	
class ReadLocation(Expression):
	location : Location

class WriteLocation(Statement):
	location : Location
	value    : Expression

class IfStmt(Statement):
    expr: Expression
    stmt: Statement

class WhileStmt(Statement):
    expr: Expression
    stmt: Statement

class VarAssignmentExpr(Expression):
    expr1: Expression
    expr2: Expression

class NullStmt(Expression):

class ArrayAssignmentExpr(Expression):
    expr1: Expression
    expr2: Expression
    expr3: Expression

# ----------------------------------------------------------------------

# Las siguientes clases para visitar y reescribir el AST se toman del 
# módulo ast de Python.

# NO MODIFIQUE
class NodeVisitor(object):
	'''
	Clase para visitar los nodos del árbol de análisis sintáctico. 
	Esto se modela después de una clase similar en la biblioteca estándar 
	ast.NodeVisitor. Para cada nodo, el método de visit(node) llama a 
	un método visit_NodeName(node) que debe implementarse en subclases. 
	El método generic_visit() se llama para todos los nodos donde no hay 
	ningún método de matching_NodeName() coincidente.
	
	Este es un ejemplo de un visitante que examina un operador binario:
	
	class VisitOps(NodeVisitor):
		visit_BinOp(self,node):
			print('Binary operator', node.op)
			self.visit(node.left)
			self.visit(node.right)
			visit_UnaryOp(self,node):
			print('Unary operator', node.op)
			self.visit(node.expr)
	
	tree = parse(txt)
	VisitOps().visit(tree)
	'''
	def visit(self, node):
		'''
		Enecuta un metodo de la forma visit_NodeName(node) donde
		NodeName es el nombre de la clase de un nodo particular.
		'''
		if isinstance(node, list):
			for item in node:
				self.visit(item)
		elif isinstance(node, AST):
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, self.generic_visit)
			visitor(node)
			
	def generic_visit(self,node):
		'''
		Metodo ejecutado si no se encuentra el metodo visit_.
		Este examina el nodo para ver si tiene _fields, una lista,
		o puede ser atravesado.
		'''
		for field in getattr(node, '_fields'):
			value = getattr(node, field, None)
			self.visit(value)
			
	@classmethod
	def __init_subclass__(cls):
		'''
		Revision de sanidad. Se asegura que las clases visitor usen los
		nombres adecuados.
		'''
		for key in vars(cls):
			if key.startswith('visit_'):
				assert key[6:] in globals(), f"{key} no coincide con nodos AST"