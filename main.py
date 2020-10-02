#!/usr/bin/python3

import parser
from expralgs import ExpressionAlgorithms
from exprchange import *





try:
	while True:
		parser.variables = dict();
		expr = parser.yacc.parse(input('> '));

		if expr is None:
			continue;

		algs = ExpressionAlgorithms(expr, parser.variables);

		print( 'Выражение: ' + str(expr) );
		print( 'Таблица истинности: ' );
		print( algs.pretty_table() );

		print( 'Вектор истинности: ' + ''.join( map(str, algs.truth_vector()) ) );
		print( 'СКНФ: ' + algs.sdnf() );
		print( 'СДНФ: ' + algs.sknf() );
		print();

		clear = expr.clone();
		recursion(add_to_or_and, clear);
		recursion(eq_to_or_and, clear);
		print( 'Очистка от сложения и эквиваленции: ' + str(clear) );

		recursion(imp_to_or, clear);
		print( 'Очистка от импликации: ' + str(clear) );

		#  shef = expr.clone();
		#  all_to_shef(shef);
		#  print( 'Через штрих Шеффера: ' + str(shef) );
		#  pirs = expr.clone();
		#  all_to_pirs(pirs);
		#  print( 'Через стрелки Пирса: ' + str(pirs) );

except EOFError:
	pass;

except KeyboardInterrupt:
	pass;

print("\nПрощайте!");





# END
