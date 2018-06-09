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
        'certifi==2018.4.16',
        'numpy==1.14.4',
        'pandas==0.23.0',
        'PyMySQL==0.8.1',
        'python-dateutil==2.6.1',
        'pytz==2018.3',
        'PyYAML==3.12',
        'scipy==1.1.0',
        'six==1.11.0',
        'SQLAlchemy==1.2.8',
        'tqdm==4.19.5'
    ],
    packages=find_packages()
)
