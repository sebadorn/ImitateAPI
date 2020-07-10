# Builtin modules
from http import server
import ssl, subprocess

# Project modules
from .. import localhttp



def create_localhost_cert():
	""" Create the SSL certificate for localhost. """

	print( 'Creating localhost.crt and localhost.key files...' )

	try:
		completed = subprocess.run(
			[
				'openssl', 'req', '-x509',
				'-days', '365',
				'-out', './sapis/localhttps/localhost.crt',
				'-keyout', './sapis/localhttps/localhost.key',
				'-newkey', 'rsa:2048',
				'-nodes',
				'-sha256',
				'-subj', '/CN=localhost',
				'-extensions', 'EXT',
				'-config', './sapis/localhttps/openssl_config_template.txt'
			],
			check = True,
			stderr = subprocess.PIPE,
			universal_newlines = True
		)
		print( 'Done.' )
	except CalledProcessError as err:
		print( 'openssl error:\n%s' % err.stderr )



class localserver( localhttp.localserver ):


	def __init__( self, port, certfile, keyfile ):
		"""
		Parameters:
		port     (int) -- Port to run the local server on.
		certfile (str) --
		keyfile  (str) --
		"""

		if not certfile or not keyfile:
			create_localhost_cert()
			certfile = './sapis/localhttps/localhost.crt'
			keyfile = './sapis/localhttps/localhost.key'

		self.httpd = server.HTTPServer( ( '', port ), localhttp.APIRequestHandler )

		self.httpd.socket = ssl.wrap_socket(
			self.httpd.socket,
			certfile = certfile,
			keyfile = keyfile,
			server_side = True
		)


	def start( self ):
		""" Start the local server. """

		print( 'A local HTTPS server will be available under: https://127.0.0.1:%d' % self.httpd.server_port )
		print( '----------' )
		self.httpd.serve_forever()
