import pydot;
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

class Type_Spec(AST):
	pass

class Location(AST):
	pass

# Nodos concretos del AST
class Program(Statement):
	'''
	program : decl_list
	'''
	decl_list: [Statement]

class Write_Stmt(Statement):
	'''
	statement : write(expression) ;
	'''
	value : Expression

class IntegerLiteral(Literal):
	value : int

class FloatLiteral(Literal):
	value : float

class BoolLiteral(Literal):
	value : str

class CharLiteral(Literal):
	value : str

class StringLiteral(Literal):
	value : str

class Size(Literal):
	value : int

class If_Stmt(Statement):
	condition   : Expression
	true_block  : Statement
	false_block : (Statement,type(None))

class While_Stmt(Statement):
	condition : Expression
	body      : Statement

class ForStmt(Statement):
	initialStmt : Statement
	testExpr : Expression
	updpStmt : Expression
	body : Statement

class BinOp(Expression):
	'''
	Un operador binario como 2 + 3 o x * y
	'''
	op    : str
	left  : Expression
	right : Expression

	def getClass():
		return self.__class__.__name__

class UnaryOp(Expression):
	'''
	Un operador unario como -2 o +3
	'''
	op    : str
	right : Expression

class FuncCall(Expression):
	name      : str
	arguments : [Expression]

class ConstDeclaration(Statement):
	'''
	const name := value ;
	'''
	name  : str
	value : Expression

class FuncParameter(AST):
	name : str
	type_spec : Type_Spec

class FuncDeclaration(Statement):
	name     : str
	params   : [FuncParameter]
	type_spec : Type_Spec
	body     : Statement

class Return_Stmt(Statement):
	value : Expression

class SimpleType(Type_Spec):
	name : str

class LocalDecl(Statement):
	name : str
	type_spec : Type_Spec
	value    : (Expression, type(None))    # Optional


class ArrayLocalDecl(Statement):
	name : str
	type_spec : Type_Spec
	size: (type(None))


class Null_Stmt(Statement):
	value : (type(None))

class Return_Stmt(Statement):
	value: (Expression,type(None))

class Break_Stmt(Statement):
	value: (type(None))

class Compound_Stmt(Statement):
	local_decl: [Statement]
	stmt_list: [Statement]

class VarDeclaration(Statement):
	'''
	var name type_spec [ = value ];
	'''
	name     : str
	type_spec : Type_Spec
	value    : (Expression, type(None))    # Optional


class ArrayDeclaration(Statement):
	'''
	var name type_spec [ = value ];
	'''
	name     : str
	type_spec : Type_Spec

class SimpleLocation(Location):
	name : str

class ReadLocation(Expression):
	location : Location

class WriteLocation(Statement):
	location : Location
	value    : Expression

class ArraySimpleLocation(Location):
	name : str
	size : Expression

class NewArrayExpr(Expression):
	type_spec: Type_Spec
	expr : Expression
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#                NO MODIFIQUE NADA DE AQUI EN ADELANTE
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
				
# NO MODIFICAR
def flatten(top):
	'''
	Aplana todo el árbol de análisis sintáctico en una lista para 
	depurar y probar.  Esto devuelve una lista de tuplas de la 
	forma (depth, node) donde depth es un entero que representa 
	la profundidad y node es el nodo AST asociado.
	'''
	class Flattener(NodeVisitor):
		def __init__(self):
			self.depth = 0
			self.nodes = []
		def generic_visit(self, node):
			self.nodes.append((self.depth, node))
			self.depth += 1
			NodeVisitor.generic_visit(self, node)
			self.depth -= 1
			
	d = Flattener()
	d.visit(top)
	return d.nodes


class DotVisitor(NodeVisitor):
	'''
	Crea archivo tipo 'dot' para Graphiz
	'''	
	_dot_graph_defaults = {
		'graph_name': 'AST',
		'graph_type': 'digraph'
	}
	
	_dot_node_defaults = {
		'shape': 'box',
		'color': 'lightblue2',
		'style': 'filled'
	}
	
	_dot_edge_defaults = { }
	
	def __init__(self):
		'''
		creamos un obj del tipo dot que se va a llamar AST
		'''
		self.dot = pydot.Dot(graph_name='AST', graph_type='digraph')
		self.dot.set_node_defaults(**self._dot_node_defaults)
		self.dot.set_edge_defaults(**self._dot_edge_defaults)
		self.st = []
		self.id =0

	def __repr__(self):
		return self.dot.to_string()

	def _dot_graph_defaults(self):
		return { }

	def _id(self):
		self.id += 1
		return 'n%02d' % self.id

	def generic_visit(self, node): 
		#siempre va a pasar poraca cada vez queeste en un nodo
		id = self._id()    
		label = node.__class__.__name__
		NodeVisitor.generic_visit(self, node)
		for field in getattr(node, '_fields'):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					self.dot.add_edge(pydot.Edge(id, self.st.pop()))
			elif isinstance(value, AST):
				self.dot.add_edge(pydot.Edge(id, self.st.pop()))
			elif value:
				label += '\\n' + '({}={})'.format(field, value)

		self.dot.add_node(pydot.Node(id, label=label))
		self.st.append(id)
