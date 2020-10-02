from node import Node, Var, Operation





# Рекурсивно вызывает переданную функцию в первом аргументе
# с переданным узлом и со всеми его потомками
def recursion(fun, node):
	if node is None:
		return;
	fun(node);
	recursion(fun, node.left);
	recursion(fun, node.right);
	return;



# Производит неравносильное преобразование узла выражения — 
# отрицание; если данное выражение уже содержит отрицание,
# то оно будет удалено
def negation(node):
	''' отрицание '''
	if node.isleaf():
		node.op = Operation.NOT;
		node.left = Node(value=node.value);
		node.value = None;
		return;

	if node.op == Operation.NOT:
		if node.left.isleaf():
			node.op = None;
			node.value = node.left.value;
			node.left = None;
			return;

		node.op = node.left.op;
		node.right = node.left.right;
		node.left = node.left.left;
		return;

	left = Node(node.op, node.left, node.right);
	node.op = Operation.NOT;
	node.left = left;
	node.right = None;
	return;





# Выполняет ряд равносильных преобразований, в результате которых
# в выражении остаются только операции штриха Шеффера
def all_to_shef(node):
	recursion(add_to_or_and, node);
	recursion(eq_to_or_and,  node);
	recursion(imp_to_or,     node);
	recursion(and_to_or,     node);
	recursion(or_to_shef,    node);
	recursion(not_to_shef,   node);
	return;


# Выполняет ряд равносильных преобразований, в результате которых
# в выражении остаются только операции стрелки Пирса
def all_to_pirs(node):
	recursion(add_to_or_and, node);
	recursion(eq_to_or_and,  node);
	recursion(imp_to_and,    node);
	recursion(or_to_and,     node);
	recursion(and_to_pirs,   node);
	recursion(not_to_pirs,   node);
	return;





# Следюущие процедуры принимают узел выражения и производят
# равносильное преобразование из одной операции в другую;
# если функция не предназначена для преобразования опера-
# ции, которую содержит узел, то узел останется неизменным
def or_to_and(node):
	''' дизъюнкция -> конъюнкция '''
	if node.op != Operation.OR:
		return;
	negation(node.left);
	negation(node.right);
	node.op = Operation.AND;
	negation(node);
	return;

def and_to_or(node):
	''' конъюнкция -> дизъюнкция '''
	if node.op != Operation.AND:
		return;
	negation(node.left);
	negation(node.right);
	node.op = Operation.OR;
	negation(node);
	return;

def imp_to_or(node):
	''' импликация -> дизъюнкция и отрицание '''
	if node.op != Operation.IMP:
		return;
	negation(node.left);
	node.op = Operation.OR;
	return;

def imp_to_and(node):
	''' импликация -> конъюнкция и отрицание '''
	if node.op != Operation.IMP:
		return;
	negation(node.right);
	node.op = Operation.AND;
	negation(node);
	return;





# Функции преобразования операций эквивалентности и сложения по
# Жегалкину в операции конъюнкции и дизъюнкции
def eq_to_or_and(node):
	''' эквивалентность -> конъюнкция и дизъюнкция '''
	if node.op != Operation.EQ:
		return;

	lnode = Node(Operation.AND, node.left, node.right);

	rleft = node.left.clone();
	negation(rleft);
	rright = node.right.clone();
	negation(rright);
	rnode = Node(Operation.AND, rleft, rright);

	node.op = Operation.OR;
	node.left = lnode;
	node.right = rnode;
	return;

def add_to_or_and(node):
	''' сложение по Жегалкину -> конъюнкция и дизъюнкция '''
	if node.op != Operation.ADD:
		return;

	lnode = Node(Operation.AND, node.left, node.right.clone());
	negation(lnode.right);

	rnode = Node(Operation.AND, node.left.clone(), node.right);
	negation(lnode.left);

	node.op = Operation.OR;
	node.left = lnode;
	node.right = rnode;
	return;





# Функции преобразования к штриху Шеффера
def or_to_shef(node):
	''' дизъюнкция -> штрих Шеффера '''
	if node.op != Operation.OR:
		return;

	lnode = Node(Operation.SHEF, node.left, node.left.clone());
	rnode = Node(Operation.SHEF, node.right, node.right.clone());

	node.op = Operation.SHEF;
	node.left = lnode;
	node.right = rnode;
	return;

def not_to_shef(node):
	''' отрицание -> штрих Шеффера '''
	if node.op != Operation.NOT:
		return;

	node.op = Operation.SHEF;
	node.right = node.left.clone();
	return;





# Функции преобразования к стрелке Пирса
def and_to_pirs(node):
	''' конъюнкция -> стрелка Пирса '''
	if node.op != Operation.AND:
		return;

	lnode = Node(Operation.PIRS, node.left, node.left.clone());
	rnode = Node(Operation.PIRS, node.right, node.right.clone());

	node.op = Operation.PIRS;
	node.left = lnode;
	node.right = rnode;
	return;

def not_to_pirs(node):
	''' отрицание -> стрелка Пирса '''
	if node.op != Operation.NOT:
		return;

	node.op = Operation.SHEF;
	node.right = node.left.clone();
	return;





# end
