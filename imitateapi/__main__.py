# Built-in modules
import sys

# Project modules
from .api.manager import APIManager
from . import info
from .localhttp.localserver import LocalServerHTTP
from .localhttps.localserver import LocalServerHTTPS



if __name__ == '__main__':
	parser = info.get_parser()
	args = parser.parse_args( sys.argv[1:] )

	if args.version:
		print( 'Version: %s' % info.get_version() )
		sys.exit()

	apiManager = APIManager( args.api_files_dir )

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
		server = LocalServerHTTPS(
			port = args.port,
			certfile = args.ssl_certfile,
			keyfile = args.ssl_keyfile
		)
	else:
		server = LocalServerHTTP( args.port )

	server.set_api( api_rules )
	server.start()
