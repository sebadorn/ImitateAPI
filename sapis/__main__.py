# Native modules
import argparse, sys
from http import server

# Project modules



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
		'-l', '--list',
		action = 'store_true',
		required = False,
		help = 'List the available APIs to use with the -a argument and exit.',
		dest = 'list'
	)
	args = parser.parse_args( sys.argv[1:] )

	if args.api:
		print( 'Simulating API: %s' % args.api )
	else:
		print( 'No API has been selected.' )

	print( 'A local HTTP server will be available under: http://127.0.0.1:%d' % args.port )
	print( '----------' )

	httpd = server.HTTPServer( ( '', args.port ), server.BaseHTTPRequestHandler )
	httpd.serve_forever()
