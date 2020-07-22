from argparse import ArgumentParser, RawDescriptionHelpFormatter



def get_version():
	"""
	Returns
	-------
	str
	"""

	return '0.1.0'


def get_parser():
	"""
	Returns
	-------
	argparse.ArgumentParser
	"""

	parser = ArgumentParser(
		formatter_class = RawDescriptionHelpFormatter,
		description = (
			'ImitateAPI -- A simple API simulator.\n'
			'-------------------------------------\n'
			'NOT INTENDED FOR USE IN PRODUCTION. This application was created with development and testing in mind.\n'
			'-------------------------------------'
		)
	)
	parser.add_argument(
		'-s', '--server',
		default = 'http',
		choices = ['http', 'https'],
		required = False,
		dest = 'server'
	)
	parser.add_argument(
		'--ssl-certfile',
		required = False,
		help = 'Path to the SSL certificate file. Only used if a local HTTPS server is used.',
		dest = 'ssl_certfile'
	)
	parser.add_argument(
		'--ssl-keyfile',
		required = False,
		help = 'Path to the SSL key file. Only used if a local HTTPS server is used.',
		dest = 'ssl_keyfile'
	)
	parser.add_argument(
		'-p', '--port',
		default = 8000,
		type = int,
		required = False,
		dest = 'port'
	)
	parser.add_argument(
		'-a', '--api',
		required = False,
		help = 'Select an API to simulate.',
		dest = 'api'
	)
	parser.add_argument(
		'--api-files-dir',
		default = './api-files',
		required = False,
		help = 'The directory to search for API files.',
		dest = 'api_files_dir'
	)
	parser.add_argument(
		'-l', '--list',
		action = 'store_true',
		required = False,
		help = 'List the available APIs to use with the -a argument and exit.',
		dest = 'list'
	)
	parser.add_argument(
		'-v', '--version',
		action = 'store_true',
		required = False,
		help = 'Print the module version and exit.',
		dest = 'version'
	)

	return parser
