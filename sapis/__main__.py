# Native modules
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

	if args.api:
		print( 'Simulating API: %s' % args.api )
	else:
		print( 'No API has been selected.' )

	if args.server is 'https':
		server = localhttps.localserver( args.port )
	else:
		server = localhttp.localserver( args.port )

	server.start()
