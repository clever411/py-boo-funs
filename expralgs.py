from prettytable import PrettyTable





# Класс для нахождения таблицы истинности, вектора истинности,
# СДНФ и СКНФ
class ExpressionAlgorithms:
	expr      = None;
	variables = None;
	varnames  = None;
	varc      = None;
	_table    = None;
	_ptable   = None;
	_vector   = None;
	_sdnf     = None;
	_sknf     = None;
	
	def __init__(self, expr, variables):
		self.expr = expr;
		self.variables = variables;
		self.varnames = sorted(variables);
		self.varc = len(self.varnames);

	# Возвращает таблицу истинности
	def truth_table(self):
		'''
		return array of arrays of values of sorted
		variables and function value:
		  x -> y (implication):
			[
				# x  y  F
				[ 0, 0, 1 ]
				[ 0, 1, 1 ]
				[ 1, 0, 0 ]
				[ 1, 1, 1 ]
			]
		'''
		if self._table is None:
			self._calc_truth_table();
		return self._table;

	# Возвращает вектор истинности
	def truth_vector(self):
		if self._vector is None:
			self._calc_truth_vector();
		return self._vector;

	# Возвращает объект PrettyTable
	def pretty_table(self, head='FUN'):
		ptcont = [ self.varnames + [ head ] ] + self.truth_table();
		pt = PrettyTable(ptcont[0]);
		for i in range(1, len(ptcont)):
			pt.add_row( ptcont[i] );
		return pt;

	# Возвращает СДНФ в виде строки
	def sdnf(self):
		if self._sdnf is None:
			self._calc_sdnf();
		return self._sdnf;

	# Возвращает СКНФ в виде строки
	def sknf(self):
		if self._sknf is None:
			self._calc_sknf();
		return self._sknf;



	# implementation
	def _add_rows(self, addto, proto, off, isvec=False):
		'''
		expr     - Node
		varnames - [ 'x', 'y', ... ] to set vars by variables[varnames[off]]
		table    - [ [] ] to append row
		proto    - [ x, y, ..., 0, 0]
							off
		'''
		if off == len(proto):
			if isvec:
				addto.append( int(self.expr.calc()) );
			else:
				addto.append( proto + [ int(self.expr.calc()) ] );
			return;

		oldprotoval = proto[off];
		oldvarval = self.variables[ self.varnames[off] ].value;

		proto[off] = 0;
		self.variables[ self.varnames[off] ].value = 0;
		self._add_rows(addto, proto, off+1, isvec);

		proto[off] = 1;
		self.variables[ self.varnames[off] ].value = 1;
		self._add_rows(addto, proto, off+1, isvec);

		proto[off] = oldprotoval;
		self.variables[ self.varnames[off] ].value = oldvarval;
		return;


	def _calc_truth_table(self):
		self._table = [];
		self._add_rows(self._table, [0]*self.varc, 0);
		return;

	def _calc_truth_vector(self):
		self._vector = [];
		self._add_rows(self._vector, [0]*self.varc, 0, True);
		return;

	def _calc_sdnf(self):
		mems = [];
		for row in self.truth_table():
			if row[-1] != 1:
				continue;
			avars = [];
			for colnum in range(len(row)-1):
				if row[colnum] == 1:
					avars.append(self.varnames[colnum]);
				else:
					avars.append('¬' + self.varnames[colnum]);
			mems.append(avars);
		self._sdnf = ' ∨ '.join(reversed( [ '&'.join(avars) for avars in mems ] ));
		return;

	def _calc_sknf(self):
		mems = [];
		for row in self.truth_table():
			if row[-1] != 0:
				continue;
			avars = [];
			for colnum in range(len(row)-1):
				if row[colnum] == 0:
					avars.append(self.varnames[colnum]);
				else:
					avars.append('¬' + self.varnames[colnum]);
			mems.append(avars);
		self._sknf = '&'.join( [ '(' + ' ∨ '.join(avars) + ')' for avars in mems ] );
		return;





# END
