#coding: utf-8
try:
    from setuptools import setup
    
except ImportError:
    from distutils.core import setup
    
config = {
    'description' : 'Programas útiles para simplificar los cálculos de incertidumbres',
    'author' : 'Jorge Expósito',
    'url' : '',
    'author email' : 'jorge@monteuve.com',
    'version' : '0.1',
    'install_requires' : ['nose'],
    'packages' : ['PhysLab'],
    'scripts' : [],
    'name' : 'PhysLab'
}

setup(**config)   
