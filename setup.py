try:
    from setuptools import setup
except ImportError:
    from distuils.core import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name =  'Yelp',
    description = 'A project that does things',
    url = 'https://github.com/friehl/NAME',
    author_email ='fletcher.riehl@gmail.com',
    version =  '0.1',
    install_requires = requirements,
    packages = ['Yelp'],
    scripts = []
)
    
