#coding: utf-8
import numpy as np
import math	


def isnumber(x):
	return type(x) == float or type(x) == int


class Medida:
	
	def __init__(self, value, u, units='', var=None, function=None, derivadas=None):
		
		self.value = float(value)
		self.u = float(u)
		self.units = units
		
		if var == None:
			self.var = {self}
		else:
			self.var = var
				
		if function == None:
			def function(vardict):
				return vardict[self]
			self.function = function
		else:
			self.function = function
			
		if derivadas == None:
			self.derivadas = {self:1}
		else:
			self.derivadas = derivadas
	
	
	def __str__(self):
		#representación con print

		#falta que ajuste las cifras significativas
		return "%f ± %f %s" %(self.value, self.u, self.units)
		
	def __repr__(self):
		
		return 'Medida(%f, %f, %s,)' %(self.value, self.u, self.units) 
		
	def operate(self, other, h, h_A, h_B):
		
		 
		f = self.function
		g = other.function
		
		def function(vardict):
			return h(f(vardict), g(vardict))
		
		Df = self.derivadas
		Dg = other.derivadas
		
		var = self.var | other.var
		var_fg = self.var & other.var
		
				
		value = h(self.value, other.value)
		
		value_dict = {}
		derivadas = {}
		for variable in var:
			value_dict.update({variable: variable.value})
			derivadas.update({variable: h_A*Df.get(variable, 0.) \
								+ h_B*Dg.get(variable, 0.)})
			
		C = 0.
		for variable in var_fg:
			C+= Df[variable]*Dg[variable]*variable.u**2
		
		u = h_A**2*self.u**2 + h_B**2*other.u**2 + 2*h_A*h_B*C
		#para corregir los errores numéricos con los cuáles u puede resultar negativo
		u = np.sqrt(u)

		return Medida(value, u, '', var=var, function=function, derivadas=derivadas)
		
		
		
	def __mul__(self, other):
		if isinstance(other, Medida):
			def h(a,b):
				return a*b
			return self.operate(other, h, other.value, self.value)
			
		elif isnumber(other):
			#si la Medida se multiplica por un número estos son los cálculos
			value = other*self.value
			u = abs(other*self.u)
			
			def function(vardict):
				 return other*self.function(vardict)
			
			derivadas = {}
			for variable in self.var:
				derivadas.update({variable:other*self.derivadas[variable]})

			return Medida(value, u, var=self.var, function=function\
						  ,derivadas=derivadas)
		
		else:
			#para cualquier otro tipo se lanza un error
			raise ValueError('Tipo no válido para multiplicar una Medida: %s'\
			 %type(other))
			
	def __rmul__(self, other):
		return self.__mul__(other)
		
	def __imul__(self, other):
		return self.__mul__(other)
		
		

	def __add__(self, other):
		if isinstance(other, Medida):
			def h(a,b):
				return a + b
			return self.operate(other, h, 1., 1.)
			
			
		#esta opción deberá ser eliminida en cuanto se implemente el
		#cálculo con unidades, ya que no tiene sentido sumar un
		#valor con unidades y otro sin ellas.
		if isnumber(other):
			def function(vardict):
				return other + self.function(vardict)
			return Medida(self.value + other, self.u, var=self.var,\
					function=function, derivadas=self.derivadas)
		
		raise ValueError('Tipo no válido para sumar una Medida: %s'\
			 %type(other))

	def __radd__(self, other):
		return self.__add__(other)

	def __iadd__(self, other):
 		#operador +=
	 	return self.__add__(other)
	 	
	 	
	def __sub__(self, other):
		if isinstance(other, Medida):
			def h(a,b):
				return a - b
			return self.operate(other, h,1., -1.)
		
		if isnumber(other):
			def function(vardict):
				return self.function(vardict) - other
			return Medida(self.value - other, self.u, var=self.var,\
					function=function, derivadas=self.derivadas)
		
		raise ValueError('Tipo no válido para restar una Medida: %s'\
			 %type(other))

	def __rsub__(self, other):
		if isnumber(other):
			def function(vardict):
				return other - self.function(vardict)
			derivadas = {}
			for variable in self.var:
				derivadas.update({variable:-self.derivadas[variable]})
			return Medida(other - self.value, self.u, var=self.var,\
					function=function, derivadas=derivadas)

	def __isub__(self, other):
 		#operador +=
	 	return self.__sub__(other)

	
	def __div__(self, other):
		
		if isinstance(other, Medida):
			def h(a,b):
				return a/b
			return self.operate(other, h, 1./other.value, -self.value/other.value**2)
		
		elif isnumber(other):
			self.__mul__(1./other)
		
		else:
			raise ValueError('Tipo no válido para dividir una Medida: %s'\
				%type(other))
				
	def __rdiv__(self, other):
		
		if isnumber(other):
 			
 			try:
		 		value = other/self.value
		 		u = other*self.u/self.value**2
		 		
		 		def function(vardict):
		 			return 1./self.function(vardict)
				
				derivadas = {}
				for variable in self.var:
					derivadas.update({variable: \
									-self.derivadas[variable]/self.value**2})
				
		 		return Medida(value, u, var=self.var, function=function,
		 				derivadas=derivadas)
			except ZeroDivisionError:
				pass
				#implementar situación de error
		else:
			raise ValueError('Tipo no válido para la operación: %s' %type(other))
			
	def __idiv(self, other):
		return self.__div__(other)

	def __pow__(self, power):
		#cálculos para elevar una medida a una potencia, operador **
		if isnumber(power):

			value = self.value**power
			u = abs(power*self.value**(power-1)*self.u)
			
			def function(vardict):
				return self.value**power*self.function(vardict)
				
			derivadas = {}
			for variable in self.var:
				derivadas.update({variable:\
				power*self.value**(power-1.)*self.derivadas[variable]})

			return Medida(value, u, var=self.var, function=function,\
			derivadas=derivadas)

		
	def equal(self, other):
		
		if isinstance(other, Medida):
			return self.value == other.value and self.u == other.u
			#rewrite so that var and function are equal
			
		else:
			raise ValueError('Tipo no válido para comparar una medida %s'%type(other))



class mArray(object):
	
	def _set_medidas(self):
		
		for i in xrange(self.lenght):
			self.medidas[i] = Medida(self.values[i], self.s[i], self.units[i])
			
	def _calc_valores(self, medidas):
		#función auxiliar para las operaciones
		#medidas es una lista de Medidas, no un array
		values = [0]*len(medidas)
		s = [0]*len(medidas)
		units = [0]*len(medidas)
		for i in xrange(self.lenght):
			#el siguiente if está porque al dividir medidas se puede obtener
			#un escalar
			if type(medidas[i]) == float:
				values[i], s[i], units[i] = medidas[i], 0., ''
			else:
				values[i], s[i], units[i] = medidas[i].value, medidas[i].s,\
				 medidas[i].units
		return values, s, units
		
	def _check_lenght(self, array):
		return len(self) == len(array)
	
		
	def __init__(self, *args):
	
		self.tipos_lista = [list, np.ndarray]
		self.tipos_numeros = [int, float]
	
		if len(args) == 3:
			value = args[0]
			s = args[1]
			units = args[2]
		
			#esta parte está un poco desordenada, habría que arreglarla un poco
			if type(s) in self.tipos_lista:
				if type(units) == list:
					if len(values) != len(s) or len(values) != len(units):
						raise ValueError('Las longitudes de las listas no coinciden')
					
					else: 
						self.values = np.array(values).astype(float)
						self.s = np.array(s).astype(float)
						self.units = units
						self.lenght = len(self.values)
						self.medidas = [0]*self.lenght
						self._set_medidas()
				elif type(units) == str:
					if len(values) != len(s):
						raise ValueError('Las longitudes de las listas no coinciden')
					else:
						self.values = np.array(values).astype(float)
						self.s = np.array(s).astype(float)
						self.lenght = len(self.values)
						self.units = [units]*self.lenght
						self.medidas = [0]*self.lenght
						self._set_medidas()	
				else:
					raise ValueError('Tipo %s no válido para las unidades'\
					%type(units))
						
			elif type(s) in self.tipos_numeros:
				if type(units) == list:
					if len(values) != len(units):
						raise ValueError('Las longitudes de las listas no coinciden')
					
					else:
						self.values = np.array(values).astype(float)
						self.lenght = len(self.values)
						self.s = np.array([s]*self.lenght).astype(float)
						self.units = units
						self.medidas = [0]*self.lenght
						self._set_medidas()
				elif type(units) == str:
						self.values = np.array(values).astype(float)
						self.lenght = len(self.values)
						self.s = np.array([s]*self.lenght).astype(float)
						self.units = [units]*self.lenght
						self.medidas = [0]*self.lenght
						self._set_medidas()
					
				else:
					raise ValueError('Tipo %s no válido para las unidades'\
					%type(units))
			else:
				raise ValueError('Tipo %s no válido para las incertidumbres'%type(s))
		
		elif len(args) == 1:
			self.medidas = args[0]
			self.lenght = len(self.medidas)
			self.v, self.s, self.units = self._calc_valores(self.medidas)
			
		else:
			
			raise ValueError('Inicialización incorrecta, la forma correcta es\
			mArray(valores, incertidumbre, unidades) donde valores ha de ser una\
			lista y los otros dos pueden ser listas o escalares, o bien se puede\
			inicializar con mArray(medidas) donde medidas es una lista de objetos\
			medida')	
	
	def __str__(self):
		
		string = '['
		for i in xrange(self.lenght):
			string += str(self.medidas[i]) + ', '
			
		string = string[:-2]
		string += ']'
		return string
		
	def __setitem__(self, idx, medida):
		if isinstance(medida, Medida):
			self.medidas[idx] = medida
		else:
			raise ValueError('Los elementos de mArray han de ser Medidas')
		
	def __getitem__(self,idx):
		return self.medidas[idx]
		
	def __len__(self):
		return self.lenght
		
	def __iter__(self):
		return iter(self.medidas)
				
	def append(self, medida):
		if isinstance(medida, Medida):
			self.medidas.append(medida)
		
		else:
			raise ValueError('Los elementos de mArray han de ser Medidas')
			
	def __mul__(self, multiplier):
		
		if isinstance(multiplier, mArray):
			array = multiplier
			if self._check_lenght(array):
				medidas = [0]*self.lenght
				
				for i in xrange(self.lenght):
					medidas[i] = self[i]*array[i]
					
				values, s, units = self._calc_valores(medidas)	
				return mArray(values, s, units)
			
			else:
				raise ValueError('Las longitudes de las listas no coinciden')
			
		elif isinstance(multiplier, Medida):
			medida = multiplier
			medidas = [0]*self.lenght
			
			for i in xrange(self.lenght):
				medidas[i] = self[i]*medida
			
			values, s, units = self._calc_valores(medidas)
			return mArray(values, s, units)
		
		elif type(multiplier) == int or type(multiplier) == float:
			return mArray(multiplier*self.values, multiplier*self.s, self.units)
		
		else:
			raise ValueError('mArray no puede ser multiplicado por %s'\
			 %type(multiplier))
		
	def __rmul__(self, multiplier):
		
		if type(multiplier) == int or type(float):
			return mArray(multiplier*self.values, multiplier*self.s, self.units)
			
		else:
			raise ValueError('mArray no puede ser multiplicado por %s'\
			%type(multiplier))
			
	def __imul__(self, multiplier):
	 	return self*multiplier
	
	def __add__(self, adder):
		
		if isinstance(adder, mArray):
			array = adder
			if self._check_length(array):
				medidas = [0]*self.lenght
				
				for i in xrange(self.lenght):
					medidas[i] = self[i] + array[i]
				
				values, s, units = self._calc_valores(medidas)
				return mArray(values, s, units)
			
			else:
				raise ValueError('Las longitudes de las listas no coinciden')
			
		elif isinstance(adder, Medida):
			medida = adder
			medidas = [0]*self.lenght
			
			for i in xrange(self.lenght):
				medidas[i] = self[i] + medida
			
			values, s, units = self._calc_valores(medidas)
			return mArray(values, s, units)
			
		else:
			raise ValueError('mArray no puede ser sumado con %s'% type(adder)) 	
 	
 	def __radd__(self, medida):
 		if isinstance(medida, Medida):
 			medidas = [0]*self.lenght
			
			for i in xrange(self.lenght):
				medidas[i] = self[i] + medida
			
			values, s, units = self._calc_valores(medidas)
			return mArray(values, s, units)
			
		else:
			raise ValueError('mArray no puede ser sumado con %s'% type(adder)) 
 	
 	def __iadd__(self, adder):
 		return self + adder
		
	def __div__(self, divider):	
		if isinstance(divider, mArray):
			array = divider
			if self._check_lenght(array):
				medidas = [0]*self.lenght
				
				for i in xrange(self.lenght):
					medidas[i] = self[i]/array[i]
				
				print type(medidas)	
				values, s, units = self._calc_valores(medidas)	
				return mArray(values, s, units)
			else:
				raise ValueError('Las longitudes de las listas no coinciden')
			
			
		elif isinstance(divider, Medida):
			medida = divider
			medidas = [0]*self.lenght
			
			for i in xrange(self.lenght):
				medidas[i] = self[i]/medida
			
			values, s, units = self._calc_valores(medidas)
			return mArray(values, s, units)
		
		elif type(divider) in self.tipos_numeros:
			return mArray(self.values/divider, self.s/divider, self.units)
		
		else:
			raise ValueError('mArray no puede ser multiplicado por %s'\
			 %type(divider))
	 
	def __rdiv__(self, divider):
	 
	 	if isinstance(divider, Medida):
	 		medida = divider
			medidas = [0]*self.lenght
			
			for i in xrange(self.lenght):
				medidas[i] = medida/self[i]
			
			values, s, units = self._calc_valores(medidas)
			return mArray(values, s, units)
		
		if type(divider) in self.tipos_numeros:
			units = [0]*self.lenght
			for i in xrange(self.lenght):
				units[i] = '1/' + self.units[i]
			return mArray(divider/self.values, divider/self.s, units)

def log(x):
	
	if isinstance(x, Medida):
		v = math.log(x.value)
		s = abs(x.s/x.value)
		u = ''
		return Medida(v,s,u)
		
	elif isinstance(x, mArray):
		medidas = [0]*len(x)
		for i in xrange(len(x)):
			medidas[i] = log(x[i])
		return mArray(medidas)
		
			
	else:
		return np.log(medida)
		
def cos(medida):
	pass
#--------------------------------
#Por hacer:
#>Implementar representación en cifras significativas
#>Crear sistema de unidades que se puedan operar entre ellas
#>Crear funciones que actuen sobre las medidas, ej.: exponencial, coseno, seno...
#>Adecentar la clase mArray, que tiene código redundante y está algo mal estructurada
#>Escribir tests
