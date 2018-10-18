#coding: utf-8
import numpy as np
import math


#El cálculo de incertidumbres de la clase Medida sólo funciona para casos simples,
#en los que la misma medida no aparece dos veces en la expresión

class Medida(object):

	'''
	La clase Medida permite crear y operar objetos con valor, unidades e incertidumbre,
	automatizando los cálculos. Se pueden usar sobre estos objetos los siguientes
	operadores: +, -, *, /, +=, -=, *=, /=, **, ==, !=, <, >, >=, <=
	La representación con print tiene la forma: valor ± incertidumbre unidades
	'''

	def __init__(self, value, s, units):

		self.value = float(value)
		self.s = float(s)
		self.units = units

	#implementar __repr__

	def __str__(self):
		#representación con print

		#falta que ajuste las cifras significativas
		return "%f ± %f %s" %(self.value, self.s, self.units)


	def __neg__(self):
		return Medida(-self.value, self.s, self.units)

	def __mul__(self,multiplier):
		#operador *
		
		'''
		Esta función se llama al usar el operador *, al escribir 
		A*B se ejectuta el código A.__mul__(B).
		En este caso se identifica primero el tipo de B, si es un objeto
		de la clase Medida se multiplican y se operan las incertidumbres,
		teniendo en cuenta si A y B no son independientes sólo para el
		caso más sencillo, A = a*B. Si B es un número se multiplica por
		el valor y la incertidumbre, y por último si B es un objeto de la
		clase mArray definida más abajo se llama la operación definida en
		mArray. Si B no es ninguno de los tipos mencionados se lanza un error.
		'''
		
		if isinstance(multiplier, Medida):
		
		#añadir el caso en que multiplier = self^b (puede venir bien definir
		#antes la función log() sobre medidas

			#fórmulas para los valores e incertidumbres al multiplicar dos Medidas
			try:
				ratio_value = multiplier.value/self.value
				ratio_s = multiplier.s/self.s
			except ZeroDivisionError:
				return 
			if multiplier.value/self.value == multiplier.s/self.s:
				value = self.value*multiplier.value
				s = abs(2*multiplier.value*self.s)
				units = self.units + '^2'

			else:
				value = self.value*multiplier.value
				s = math.sqrt((self.s*multiplier.value)**2 +\
				 (self.value*multiplier.s)**2)
			 	if multiplier.units == '':
			 		units = self.units
		 		else:
					units = self.units + '·' + multiplier.units

			#u = multiplier.value**2*self.u + self.value**2*multiplier.u
			return Medida(value, s, units)

		elif type(multiplier) == int or type(multiplier) == float:
			#si la Medida se multiplica por un número estos son los cálculos
			value = multiplier*self.value
			s = abs(multiplier*self.s)
			units = self.units

			return Medida(value, s, units)
		
		elif isinstance(multiplier, mArray):
			return multiplier*self
		
		else:
			#para cualquier otro tipo se lanza un error
			raise ValueError('Tipo no válido para multiplicar una Medida: %s'\
			 %type(multiplier))
		
 	def __rmul__(self, multiplier):
 		'''
	 	multiplicación por la derecha, sólo se ejecutará si se intenta
	 	multiplicar por un tipo no válido; es decir x * y donde x no es Medida,
	 	ya que la función se invoca sobre el primer objeto, x.__mul__(y)
		'''
		
	 	if type(multiplier) == int or type(multiplier) == float:

	 		value = multiplier*self.value
			s = abs(multiplier*self.s)
			units = self.units

			return Medida(value, s, units)

		else:
			#si no se multiplica por un número se lanza un error
			raise ValueError('Tipo no válido para multiplicar una Medida: %s'\
			 %type(multiplier))

	def __imul__(self, multiplier):
	 	#operador *=
	 	return self*multiplier


	def __add__(self, adder):
		#fórmulas para valores e incertidumbres al sumar dos Medidas
		if isinstance(adder, Medida):

			#comprueba que ambas medidas tengan las mismas unidades para poder sumarlas
			if adder.units != self.units:
				raise ValueError('Las unidades deben coincidir para sumar medidas')

			if adder.value/self.value == adder.s/self.s:
				s = self.s*(1+ adder.value/self.value)
			else:
				s = math.sqrt(self.s**2 + adder.s**2)
			value = self.value + adder.value
			units = self.units
			#u = self.u + adder.u

			return Medida(value, s, units)
		
		elif isinstance(adder, mArray):
			return adder+self
		
		else:
			raise ValueError('Tipo no válido para sumar una Medida: %s'\
			 %type(adder))
			 
	def __radd__(self, adder):
		raise ValueError('Tipo no válido para sumar una Medida: %s'\
			 %type(adder))

	def __iadd__(self, adder):
 		#operador +=
	 	return self + adder

 	def __sub__(self, substractor):
 		#resta, operador -
 		return self + -substractor

	def __isub__(self, substractor):
		#operador -=
		return self -subtractor

	def __div__(self, divider):
		'''
	 	cálculos del valor y la incertidumbre al dividir una medida por otra
	 	o por un número, operador / , no usar '//' en ningún caso, no está
	 	implementado. Si se quiere dividir un número por una Medida ver
	 	__rdiv__
	 	'''
	 	if isinstance(divider, Medida):

	 		if divider.value == 0:
	 			raise ValueError('No se puede dividir por una medida de valor 0')


 			if self.value/divider.value == self.s/divider.s:
 				return self.value/divider.value
 			else:
 				value = self.value/divider.value
 				s = math.sqrt((self.s/divider.value)**2 + \
 				(self.value*divider.s/divider.value**2)**2)
 				units = self.units + '/' + divider.units

 			#u = self.u/divider.value**2 + self.value**2*divider.u/divider.value**2

 			return Medida(value, s, units)

		elif isinstance(divider, mArray):
			return divider.__rdiv__(self)
			
			
		elif type(divider) == int or type(divider) == float:

			value = self.value/divider
			s = self.s/divider
			units = self.units

			return Medida(value, s, units)

		else:
			raise ValueError('Tipo no válido para dividir una Medida: %s'\
			 %type(divider))

	def __rdiv__(self,divider):
		
	 	'''
	 	Al intentar dividir un tipo numérico a entre una medida A se intenta
	 	usar a.__div__(A), lo cuál resulta en un error porque los tipos 
	 	numéricos de Python no están definidos para ser divisibles por
	 	objetos de la clase Medida que hemos definido aquí. Entonces python
	 	en vez de lanzar un error busca en el objeto A una función __rdiv__
	 	y si la encuentra ejecuta A.__rdiv__(a)
	 	'''
	 	if type(divider) == int or type(divider) == float:
	 		try:
		 		value = divider/self.value
		 		s = divider*self.s/self.value**2
		 		units = '1/' + self.units

		 		return Medida(value, s, units)
			except ZeroDivisionError:
				pass
				#implementar situación de error

		else:
			raise ValueError('Tipo no válido para la operación: %s' %type(divider))

	def __idiv__(self, divider):
		#operador /=
		return self/divider

	def __pow__(self, power):
		#cálculos para elevar una medida a una potencia, operador **
		if type(power) == int or type(power) == float:

			value = self.value**power
			s = abs(power*self.value**(power-1)*self.s)
			units = self.units + '^' + str(power)

			return Medida(value, s, units)

	#los operadores de orden e igualdad sólo tienen en cuenta el valor de la Medida,
	#no su incertidumbre ni sus unidades

	def __eq__(self, other):
		#operador ==
		
		if isinstance(other, Medida):
			return self.value == other.value
			
		elif type(other) == float or type(other) == int:
			return self.value == other
		
		else:
			raise ValueError('Tipo no válido para comparar una medida %s'\
			%type(other))
			

	def __ne__(self, other):
		#operador !=
		return not self == other
			
	def __lt__(self, other):
		#operador <
		if isinstance(other, Medida):
			return self.value < other.value
			
		elif type(other) == float or type(other) == int:
			return self.value < other
		
		else:
			raise ValueError('Tipo no válido para comparar una medida %s'\
			%type(other))
			
	def __gt__(self, other):
		#operador >
		if isinstance(other, Medida):
			return self.value > other.value
	
		elif type(other) == float or type(other) == int:
			return self.value > other
			
		else:
			raise ValueError('Tipo no válido para comparar una medida %s'\
			%type(other))		

	def __le__(self, other):
		#operador <=
		return self == other or self < other

	def __ge__(self, other):
		#operador >=
		return self == other or self > other
		
	def equal(self, other):
		
		if isinstance(other, Medida):
			return self.value == other.value and self.s == other.s\
			and self.units == other.units
			
		else:
			raise ValueError('Tipo no válido para comparar una medida %s'%type(other))


class Constant(Medida):
	'''
	Inicialización rápida de Medidas de incertidumbre 0
	'''
	def __init__(self, value, units):
		self.value = value
		self.s = 0
		self.untis = units






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
#>Añadir cálculo con covarianzas a la incertidumbre
#>Adecentar la clase mArray, que tiene código redundante y está algo mal estructurada
#>Escribir tests
