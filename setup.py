try:
    from setuptools import setup
except ImportError:
    from distuils.core import setup

with open('requirements.txt') as f:
    requirments = f.readlines()

setup(
    name =  'NAME',,
    description = 'A project that does things',
    url = 'https://github.com/friehl/NAME',
    email ='fletcher.riehl@gmail.com',
    version =  '0.1',
    install_requires = requirments,
    packages = ['NAME']
    scripts: []
}
    
