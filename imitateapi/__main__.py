# Built-in modules
from pathlib import Path
import sys

# Project modules
from .api.manager import APIManager
from .api.downloader import APIDownloader
from . import info
from .logger import Logger
from .localhttp.localserver import LocalServerHTTP
from .localhttps.localserver import LocalServerHTTPS



def _init():
	""" Initialize required directories and run some checks. """

	appdata_dir = info.get_user_appdata_dir()
	p = Path( appdata_dir )

	if not p.is_dir():
		Logger.info( 'Creating local user directory: %s' % appdata_dir )
		p.mkdir( parents = True, exist_ok = True )

	# TODO: check directory permissions


if __name__ == '__main__':
	Logger.init()

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
	# Download an API
	elif args.install_api:
		_init()
		apiDownloader = APIDownloader()
		apiDownloader.download( args.install_api )
	# Simulate an API.
	else:
		_init()
		apiManager = APIManager( args.api_files_dir )
		api_rules = None

		if args.api:
			print( 'Simulating API: %s' % args.api )
			api_rules = apiManager.load_api( args.api )
		else:
			Logger.warn( 'No API has been selected.' )

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
