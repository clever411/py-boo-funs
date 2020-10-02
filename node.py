# node class





# Перечисление операций
class Operation:
	OR   = 0;
	AND  = 1;
	NOT  = 2;
	IMP  = 3;
	EQ   = 4;
	ADD  = 5;
	PIRS = 6;
	SHEF = 7;





# Отображение имени операции на код, выполняющий её
_operation_code_dict = {
	Operation.OR   : '(%s or %s)',
	Operation.AND  : '(%s and %s)',
	Operation.NOT  : '(not %s)',
	Operation.IMP  : '(not %s or %s)',
	Operation.EQ   : '(%s == %s)',
	Operation.ADD  : '(%s != %s)',
	Operation.PIRS : '(not %s and not %s)',
	Operation.SHEF : '(not %s or not %s)'
};

# Отображение имён операций на их представление 
# в выражении в виде дерева
_operation_repres_dict = {
	Operation.OR   : 'or',
	Operation.AND  : 'and',
	Operation.NOT  : 'not',
	Operation.IMP  : '->',
	Operation.EQ   : '~',
	Operation.ADD  : '+',
	Operation.PIRS : 'pirs',
	Operation.SHEF : 'shef'
};

# Отображение имён операций на их символы в строчной записи
# выражения
_operation_math_syms = {
	Operation.OR   : '∨',
	Operation.AND  : '&',
	Operation.NOT  : '¬',
	Operation.IMP  : '—>',
	Operation.EQ   : '~',
	Operation.ADD  : '+',
	Operation.PIRS : '↧',
	Operation.SHEF : '|'
};

# Сопоставление имён операций с их приоритетом; необходимо
# для правильной расстановки скобок в строчной записи выражения
_operation_priority = {
	Operation.OR   : 1,
	Operation.AND  : 2,
	Operation.NOT  : 3,
	Operation.IMP  : 0,
	Operation.EQ   : 0,
	Operation.ADD  : 0,
	Operation.PIRS : 0,
	Operation.SHEF : 0
};





# Представляет из себя переменную, которая
# имеет имя и значение
class Var:
	'''
	Fields:
		name  - str contains 'x', 'y', 'z'...
		value - 0 or 1
	'''
	def __init__(self, name, value=0):
		self.name = name;
		self.value = value;
		return;

	def __str__(self):
		return self.name + ' : ' + str(self.value);





# Класс представляющий узел выражения, который может быть:
#
#   1. Листом. Тогда op, left, right = None, а значение
#      листа находится в value, имеющей тип Var
#
#   2. Унарной операцией. Тогда right, value = None, а в
#      op хранится имя операции Operation.<NAME>, в
#      left хранится узел Node, над которым операция
#      производится
#
#   3. Бинарная операция. Тогда value = None, а в
#      op хранится имя операции Operation.<NAME>, в
#      left и right хранятся узлы Node, над которыми и
#      производится операция

class Node:
	'''
	Fields:
		op    - Operation.XXX (if Node is't leaf)
		left  - Node (if Node is't leaf)
		right - Node (if Node is't leaf and op is't unary)
		value - Var with value 0 or 1 (if Node is leaf)
	'''

	def __init__(self, op=None, left=None, right=None, value=None):
		self.op = op;
		self.left = left;
		self.right = right;
		self.value = value;

	def __str__(self):
		return self.toline();

	def toline(self, prior=-1):
		'''
		преобразует выражение в его строчное предаствелине
		(по умолчанию)
		'''
		if self.isleaf():
			return self.value.name;

		s = None;
		selfpr = _operation_priority[self.op];
		if self.isunary():
			s = ( _operation_math_syms[self.op] +
				  self.left.toline(selfpr) );
		else:
			s = (
				self.left.toline(selfpr) +
				( ' ' if selfpr <= 1 else '' ) +
				_operation_math_syms[self.op] +
				( ' ' if selfpr <= 1 else '' ) +
				self.right.toline(selfpr)
			);

		if _operation_priority[self.op] <= prior:
			s = '(' + s + ')';

		return s;

	def str_tree(self, tab=''):
		''' преобразует вырание в представление в виде дерева '''
		if self.isleaf():
			return tab + str(self.value.name);

		if self.isunary():
			if self.left.isleaf():
				return ( tab + _operation_repres_dict[self.op] +
					     ' ' + self.left.tostr() );
			else:
				return ( tab + _operation_repres_dict[self.op] +
					     '\n' + self.left.tostr(tab+'  ') );

		return (
			tab + _operation_repres_dict[self.op] + '\n' +
			self.left.tostr(tab + '  ') + '\n' +
			self.right.tostr(tab + '  ')
		);



	def isleaf(self):
		''' Является ли узел листом? '''
		return self.op is None;

	def isunary(self):
		''' Является ли операция узла унарной? '''
		return self.op == Operation.NOT;

	def calc(self):
		''' Вычислить значение (возвращается True или False) '''
		if self.isleaf():
			return self.value.value != 0;

		if self.isunary():
			return eval( _operation_code_dict[self.op] % 'self.left.calc()');

		left = self.left.calc();
		right = self.right.calc();
		return eval(  _operation_code_dict[self.op] % ('left', 'right') );

	def clone(self):
		'''
		Губокое копирование узла с сохранение ссылки на
		переменную
		'''
		node = Node();
		node.op = self.op;

		if self.left is not None:
			node.left = self.left.clone();

		if self.right is not None:
			node.right = self.right.clone();

		if self.value is not None:
			node.value = self.value;

		return node;





# end
