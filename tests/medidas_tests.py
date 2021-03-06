#coding: utf-8
from nose.tools import *
from PhysLab import medidas as md
import numpy as np
import random

def test_mul_Medida():
	
	value1 = random.uniform(-1e2, 1e2)
	s1 = random.uniform(0., abs(value1))
	units1 = 'V'
	
	value2 = random.uniform(-1e2, 1e2)
	s2 = random.uniform(0., abs(value2))
	units2 = 'A'
	
	v1 = md.Medida(value1, s1, units1)	
	v2 = md.Medida(value2, s2, units2)
	
	v3 = v1*v2
	
	assert isinstance(v3, md.Medida)
	assert_equal(v3.value, value1*value2)
	
	v4 = 3*v1
	v5 = v1*3
	
	assert_equal([v4.value, v4.s, v4.units],[v5.value, v5.s, v5.units])
	assert_equal([v4.value, v4.s],[3*v1.value, 3*v1.s])
	
	assert_raises(ValueError, v4.__mul__,'hola')
	assert_raises(ValueError, v4.__rmul__, [1,2,3])
	
	
	#caso concreto para comprobar que los resultados son correctos
	x = md.Medida(10, 0.2, 'V')
	y = md.Medida(7, 0.1, 'V')
	
	z = x*y
	
	eq_(z.value, 70.)
	eq_(np.round(z.s,1),1.7) 
	
	w1 = x*(0.5*x)
	w2 = 0.5*x*x
	
	eq_(w1.value, w2.value)
	eq_(w1.s, w2.s)
	eq_(w1.units, w2.units)	
	
	assert w1.equal(w2)
	
def test_div_Medida():
	
	value1 = random.uniform(-1e2, 1e2)
	s1 = random.uniform(0., abs(value1))
	units1 = 'V'
	
	value2 = random.uniform(-1e2, 1e2)
	s2 = random.uniform(0., abs(value2))
	units2 = 'A'
	
	v1 = md.Medida(value1, s1, units1)	
	v2 = md.Medida(value2, s2, units2)
	
	v3 = v1/v2
	
	eq_(isinstance(v3,md.Medida), True)
	
	y = 1/v3
	eq_(y/y, 1.)
	
	assert_raises(ValueError, y.__div__,'hola')
	assert_raises(ValueError, y.__rdiv__, [1,2,3])
	
	#ejemplo concreto
	x = md.Medida(122, 0.65, 'V')
	y = md.Medida(31, 6.2, 'V')
	
	z = x/y
	
	eq_(z.value, 122./31.)
	eq_(np.round(z.s,2),0.79)

def test_add_Medida():
	
	value1 = random.uniform(-1e2, 1e2)
	s1 = random.uniform(0., abs(value1))
	units1 = 'V'
	
	value2 = random.uniform(-1e2, 1e2)
	s2 = random.uniform(0., abs(value2))
	units2 = 'A'
	
	v1 = md.Medida(value1, s1, units1)	
	v2 = md.Medida(value2, s2, units2)
	
	assert_raises(ValueError, v1.__add__, v2)
	
	v2.units = 'V'
	
	v3 = v1 + v2
	
	assert isinstance(v3, md.Medida)
	
	assert_raises(ValueError, v1.__add__, 3)
	assert_raises(ValueError, v1.__add__, 'hola')
	assert_raises(ValueError, v2.__radd__, 5)
	
	#caso concreto
	x = md.Medida(42, 0.012, 'V')
	y = md.Medida(91, 0.17, 'V')
	
	z = x+y
	
	eq_(z.value, 133.)
	eq_(np.round(z.s,2),0.17)
	
	w1 = x+x
	w2 = 2*x
	
	assert w1.equal(w2)
	
def test_sub_medida():

	#caso concreto
	x = md.Medida(22, 0.41, 'V')
	y = md.Medida(11, 0.53, 'V')
	
	z = x-y
	
	eq_(z.value, 11)
	eq_(np.round(z.s,2), 0.67)

def test_pow_medida():
	
	value1 = random.uniform(-1e2, 1e2)
	s1 = random.uniform(0., abs(value1))
	units1 = ''
	
	x = md.Medida(value1, s1, units1)
	'''
	n = random.randint(0, 10)
	
	z = x
	y = x**n
	
	for _ in xrange(n-1):
		z *= x	
	'''
	z = x*x
	y = x**2
	
	eq_(z.value, y.value)
	eq_(z.s, y.s)
	
	
def test_orders():
	
	x = md.Medida(42, 0.13, 'm')
	
	y = md.Medida(31, 0.22, 'm')
	
	eq_(x == y, False)
	eq_(x>y, True)
	eq_(x<y, False)
	eq_(x>=y, True)
	eq_(x<=y, False)
	eq_(x != y, True)
	
	assert_raises(ValueError, x.__eq__, 'hola')
	
	
def test_calculos():
	
	x1 = md.Medida(42, 0.13, '')
	x2 = md.Medida(31, 0.22, '')
	x3 = md.Medida(22, 0.41, '')
	x4 = md.Medida(11, 0.53, '')
	
	y1 = (x1+x2)/(x3-x4)
	
	eq_(y1.value,(x1.value + x2.value)/(x3.value - x4.value))
	eq_(np.round(y1.s, 2), 0.40)	
	
	#El siguiente fragmento requiere de cálculos con covarianzas, ya que la forma
	#en la que Medida realiza las operaciones es que en cada caso opera dos Medidas
	#y devuelve una nueva con su correspondiente valor e incertidumbre, pero este
	#proceso crea correlaciones que no puede resolver (ver apartado por hacer en
	#medidas.py)
	
	
	#y1 = (x1*x2)/(x2*x3-x4)
	#eq_(y1.value, (x1.value*x2.value)/(x2.value*x3.value-x4.value))
	#eq_(np.round(y1.s, 3), 0.036)
	
	
def test_constant():
	
	g = md.Constant(9.8, 'm/s^2')
	
	t = md.Medida(10, 0.012, 's')
	
	v = g*t
	
	
	#problema al multiplicar por constante, ya que comprueba las relaciones
	#entre valores e incertidumbres y si la incertidumbre es 0 da ZeroDivisionError
	#esto se puede solucionar con un try/except o añadiendo las covarianzas para
	#evitar tener que comprobar que uno de los factores es múltiplo del otro
	
	'''	
	assert isinstance(v, md.Medida)
	eq_(v.s, t.s*g.value)
	'''
