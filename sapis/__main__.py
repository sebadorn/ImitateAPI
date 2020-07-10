# Builtin modules
import argparse, sys

# Project modules
from . import api
from . import localhttp
from . import localhttps


if __name__ == '__main__':
	parser = argparse.ArgumentParser( description = 'Simple API Simulator' )
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
	args = parser.parse_args( sys.argv[1:] )

	apiManager = api.APIManager( args.api_files_dir )

	if args.list:
		apiManager.print_available()
		sys.exit()

	api_rules = None

	if args.api:
		print( 'Simulating API: %s' % args.api )
		api_rules = apiManager.load_api( args.api )
	else:
		print( 'No API has been selected.' )

	if args.server == 'https':
		server = localhttps.localserver(
			port = args.port,
			certfile = args.ssl_certfile,
			keyfile = args.ssl_keyfile
		)
	else:
		server = localhttp.localserver( args.port )

	server.set_api( api_rules )
	server.start()
