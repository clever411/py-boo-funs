#!/usr/bin/python3

from ply import lex, yacc
from node import Operation, Var, Node





# TOKENS
tokens = [
	'OR',      # or
	'AND',     # and, *, ^, &
	'NOT',     # not <expr>
	'NOTPOST', # <expr>'
	'IMP',     # ->
	'ADD',     # +
	'EQ',      # ~
	'SHEF',    # |
	'PIRS',    # |.

	'VAR',     # любое слово кроме or, and, not
	'LPAREN',  # (
	'RPAREN'   # )
];



# token's rules
t_LPAREN  = r'\(';
t_RPAREN  = r'\)';
t_NOTPOST = r"'";
t_ignore  = ' \t';



def t_error(t):
	print("Непонятная лексема: %s" % t.value[0]);
	t.lexer.skip(1);
	return;

def t_word(t):
	r'\w+'

	if t.value == 'or':
		t.type = 'OR';
		t.value = Operation.OR;
		return t;

	if t.value == 'and':
		t.type = 'AND';
		t.value = Operation.AND;
		return t;

	if t.value == 'not':
		t.type = 'NOT';
		t.value = Operation.NOT;
		return t;

	t.type = 'VAR';
	return t;

def t_AND(t):
	r'\*|\^|&'
	t.type = 'AND';
	t.value = Operation.AND;
	return t;

def t_IMP(t):
	r'->'
	t.type = 'IMP';
	t.value = Operation.IMP;
	return t;

def t_EQ(t):
	r'~'
	t.type = 'EQ';
	t.value = Operation.EQ;
	return t;

def t_ADD(t):
	r'\+'
	t.type = 'ADD';
	t.value = Operation.ADD;
	return t;

def t_SHEF_PIRS(t):
	r'\|\.?'
	if t.value == '|':
		t.type = 'SHEF';
		t.value = Operation.SHEF;
	else:
		t.type = 'PIRS';
		t.value = Operation.PIRS;
	return t;





# PARSER RULES
def p_error(v):
	print("Неправильный синтаксис на токене %s!" % str(v));
	return;

def p_zeroexpr(v):
	'''
	zeroexpr : zeroexpr IMP  expr
	         | zeroexpr EQ   expr
		     | zeroexpr ADD  expr
			 | zeroexpr SHEF expr
			 | zeroexpr PIRS expr
	'''
	v[0] = Node(v[2], v[1], v[3]);
	return;

def p_zeroexpr_expr(v):
	'zeroexpr : expr'
	v[0] = v[1];
	return;

def p_expr_or(v):
	'expr : expr OR term'
	v[0] = Node(v[2], v[1], v[3]);
	return;

def p_expr_term(v):
	'expr : term'
	v[0] = v[1];
	return;

def p_term_and(v):
	'''
	term : term AND factor
	     | term factor
	'''
	if len(v) == 3:
		v[0] = Node(Operation.AND, v[1], v[2]);
	else:
		v[0] = Node(v[2], v[1], v[3]);
	return;

def p_term_factor(v):
	'term : factor'
	v[0] = v[1];
	return;

def p_factor_var(v):
	'factor : VAR'
	global variables;

	var = None;
	if variables.get(v[1]) is None:
		var = Var(v[1]);
		variables[v[1]] = var;
	else:
		var = variables[v[1]];

	v[0] = Node(value=var);
	return;

def p_factor_not(v):
	'''
	factor : NOT factor
	       | factor NOTPOST
	'''
	node = v[2] if isinstance(v[2], Node) else v[1];
	v[0] = Node(op=Operation.NOT, left=node);
	return;

def p_factor_paren(v):
	'factor : LPAREN zeroexpr RPAREN'
	v[0] = v[2];
	return;





# GLOBAL OBJECTS

# В этот словарь помещаются все используюемые переменные в выражении
# (при считывании нового выражения словарь нужно очищать) и ссылки
# на них, с помощью которые можно установить значение переменной
# ( variables['x'].value = 1 )
variables = dict();

lex = lex.lex();
yacc = yacc.yacc();






# end
