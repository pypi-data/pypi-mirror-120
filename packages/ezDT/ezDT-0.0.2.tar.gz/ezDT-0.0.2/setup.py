from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
	name = 'ezDT',
	version = '0.0.2',
	description = 'Simple datetime functions',
	py_modules = ['ezDT'],
	package_dir = {'': 'src'},
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/jblarson/ezDT',
    author = 'JB Larson',

    classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
		 'License :: OSI Approved :: BSD License',
         'Operating System :: OS Independent',
       ],
)
