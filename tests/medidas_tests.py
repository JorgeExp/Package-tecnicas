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
	
	assert_equal([v4.value, v4.u, v4.units],[v5.value, v5.u, v5.units])
	assert_equal([v4.value, v4.u],[3*v1.value, 3*v1.u])
	
	assert_raises(ValueError, v4.__mul__,'hola')
	assert_raises(ValueError, v4.__rmul__, [1,2,3])
	
	
	#caso concreto para comprobar que los resultados son correctos
	x = md.Medida(10, 0.2, 'V')
	y = md.Medida(7, 0.1, 'V')
	
	z = x*y
	
	eq_(z.value, 70.)
	eq_(np.round(z.u,1),1.7) 
	
	w1 = x*(0.5*x)
	w2 = 0.5*x*x
	
	eq_(w1.value, w2.value)
	eq_(w1.u, w2.u)
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
	z = y/y
	eq_(z.value, 1.)
	
	assert_raises(ValueError, y.__div__,'hola')
	assert_raises(ValueError, y.__rdiv__, [1,2,3])
	
	#ejemplo concreto
	x = md.Medida(122, 0.65, 'V')
	y = md.Medida(31, 6.2, 'V')
	
	z = x/y
	
	eq_(z.value, 122./31.)
	eq_(np.round(z.u,2),0.79)

def test_add_Medida():
	
	value1 = random.uniform(-1e2, 1e2)
	s1 = random.uniform(0., abs(value1))
	units1 = 'V'
	
	value2 = random.uniform(-1e2, 1e2)
	s2 = random.uniform(0., abs(value2))
	units2 = 'A'
	
	v1 = md.Medida(value1, s1, units1)	
	v2 = md.Medida(value2, s2, units2)
	
	
	v2.units = 'V'
	
	v3 = v1 + v2
	
	assert isinstance(v3, md.Medida)
	
	assert_raises(ValueError, v1.__add__, 'hola')
	
	#caso concreto
	x = md.Medida(42, 0.012, 'V')
	y = md.Medida(91, 0.17, 'V')
	
	z = x+y
	
	eq_(z.value, 133.)
	eq_(np.round(z.u,2),0.17)
	
	w1 = x+x
	w2 = 2*x
	
	eq_(w1.value, w2.value)
	eq_(w1.u, w2.u)
	
def test_sub_medida():

	#caso concreto
	x = md.Medida(22, 0.41, 'V')
	y = md.Medida(11, 0.53, 'V')
	
	z = x-y
	
	eq_(z.value, 11)
	eq_(np.round(z.u,2), 0.67)

def test_pow_medida():
	
	value1 = random.uniform(-1e2, 1e2)
	s1 = random.uniform(0., abs(value1))
	units1 = ''
	
	x = md.Medida(value1, s1, units1)
	
	n = random.randint(0, 10)
	
	z = x
	y = x**n
	
	for _ in xrange(n-1):
		z *= x	
	
	z = x*x
	y = x**2
	
	eq_(z.value, y.value)
	eq_(z.u, y.u)
	

	
def test_calculos():
	
	x1 = md.Medida(42, 0.13, '')
	x2 = md.Medida(31, 0.22, '')
	x3 = md.Medida(22, 0.41, '')
	x4 = md.Medida(11, 0.53, '')
	
	y1 = (x1+x2)/(x3-x4)
	
	eq_(y1.value,(x1.value + x2.value)/(x3.value - x4.value))
	eq_(np.round(y1.u, 2), 0.40)	
	
	y1 = (x1*x2)/(x2*x3-x4)
	A = x2.value*x3.value - x4.value
	u = ((x2.value*x1.u)/A)**2 +\
	x1.value**2*(x4.value**2*x2.u**2 + x2.value**4*x3.u**2 + x2.value**2*x4.u**2)/A**4
	u = np.sqrt(u)
	eq_(y1.value, (x1.value*x2.value)/(x2.value*x3.value-x4.value))
	eq_(np.round(y1.u,3), np.round(u,3))

