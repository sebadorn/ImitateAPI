# Built-in modules
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import sys



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
		'--list-online',
		action = 'store_true',
		required = False,
		help = 'List the APIs available for installation in the online repository.',
		dest = 'list_online'
	)
	parser.add_argument(
		'--install',
		required = False,
		help = 'Install an API file from the repository.',
		dest = 'install_api'
	)
	parser.add_argument(
		'-v', '--version',
		action = 'store_true',
		required = False,
		help = 'Print the module version and exit.',
		dest = 'version'
	)

	return parser


def get_repository_index_url():
	"""
	Returns
	-------
	str
	"""

	# TODO: create an official repository
	return 'http://localhost:8001/index.json'


def get_user_appdata_dir():
	"""
	Returns
	-------
	str
	"""

	platform = sys.platform
	appdata_dir = None

	if platform.startswith( 'linux' ):
		p = Path( '~/.local/share/imitateapi' )
		appdata_dir = str( p.expanduser() )
	elif platform.startswith( 'freebsd' ):
		# TODO: Not sure this is the right directory to use.
		p = Path( '/usr/local/share' )
		appdata_dir = str( p )
	elif platform.startswith( 'darwin' ):
		p = Path( '~/Library/Application Support/imitateapi' )
		appdata_dir = str( p.expanduser() )
	elif platform.startswith( 'win32' ) or platform.startswith( 'cygwin' ):
		pass # TODO

	if appdata_dir == None:
		raise Exception( 'Platform not supported: %s' % platform )

	return appdata_dir


def get_version():
	"""
	Returns
	-------
	str
	"""

	return '0.2.2'
