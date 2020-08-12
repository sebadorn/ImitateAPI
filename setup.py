import setuptools

from imitateapi import info


with open( 'README.md', 'r' ) as file:
	long_description = file.read()


setuptools.setup(
	name = 'imitateapi',
	version = info.get_version(),
	author = 'Sebastian Dorn',
	author_email = 'sebadorn+pypi@posteo.de',
	description = 'Simulate how an API works.',
	license = 'MIT',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/sebadorn/ImitateAPI',
	packages = setuptools.find_packages(),
	package_data = {
		'': ['*.txt']
	},
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8'
	],
	keywords = 'api development http https imitate imitation local network server simulate simulation testing',
	python_requires = '>=3.6',
)
