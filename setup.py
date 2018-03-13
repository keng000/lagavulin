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
        'certifi==2018.1.18',
        'numpy==1.13.3',
        'pandas==0.22.0',
        'PyMySQL==0.8.0',
        'python-dateutil==2.6.1',
        'pytz==2018.3',
        'PyYAML==3.12',
        'scipy==0.19.1',
        'six==1.11.0',
        'SQLAlchemy==1.1.13',
        'tqdm==4.19.5'
    ],
    packages=find_packages()
)
