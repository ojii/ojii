from setuptools import setup, find_packages

version = __import__('ojii').__version__

setup(
    name = 'ojii-utils',
    version = version,
    description = 'Some utilities I wrote',
    author = 'Jonas Obrist',
    author_email = 'jonas.obrist@divio.ch',
    url = 'http://github.com/ojii/ojii-utils',
    packages = find_packages(),
    zip_safe=False,
)