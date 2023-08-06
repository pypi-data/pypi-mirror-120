from setuptools import setup
setup(
    name = 'pycodemon',
    url="https://github.com/techdoge/codemon",
    author="Elad Tal",
    author_email="techdoge12@gmail.com",
    version = '1.0.5',
    packages = ['pycodemon'],
    entry_points = {
        'console_scripts': ['cm = pycodemon.main:main', 'pycodemon = pycodemon.main:main']
    }
)
