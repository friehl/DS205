from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name =  'Yelp',
    description = 'A scraper that grabs yelp reviews for restaurants',
    url = 'https://github.com/friehl/DS205',
    author_email ='fletcher.riehl@gmail.com',
    version =  '0.1',
    install_requires = requirements,
    packages = ['Yelp'],
    scripts = []
)
