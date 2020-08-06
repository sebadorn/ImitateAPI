# Built-in modules
import sys

# Project modules
from .api.manager import APIManager
from .api.downloader import APIDownloader
from . import info
from .localhttp.localserver import LocalServerHTTP
from .localhttps.localserver import LocalServerHTTPS



if __name__ == '__main__':
	parser = info.get_parser()
	args = parser.parse_args( sys.argv[1:] )

	# Print the version.
	if args.version:
		print( 'Version: %s' % info.get_version() )
	# List locally available APIs.
	elif args.list:
		apiManager = APIManager( args.api_files_dir )
		apiManager.print_available()
	# List online available APIs for download.
	elif args.list_online:
		apiDownloader = APIDownloader()
		apiDownloader.print_online()
	elif args.install_api:
		apiDownloader = APIDownloader()
		apiDownloader.download( args.install_api )
	# Simulate an API.
	else:
		apiManager = APIManager( args.api_files_dir )
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
