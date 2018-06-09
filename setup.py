from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name='lagavulin',
    version='0.1.0',
    description='Scraping Crawler for netkeiba.com',
    long_description=readme,
    author='Kengo Miyakawa',
    author_email='4s.flashback@gmail.com',
    url='https://github.com/keng000/lagavulin',
    install_requires=[
	'certifi',
	'numpy',
	'pandas',
	'PyMySQL',
	'python-dateutil',
	'pytz',
	'PyYAML',
	'scipy',
	'six',
	'SQLAlchemy',
	'tqdm'
    ],
    packages=find_packages()
)
