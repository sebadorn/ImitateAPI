# Builtin modules
from http import server
import os, ssl, subprocess, tempfile

# Project modules
from .. import info
from .. import localhttp



def create_localhost_cert():
	""" Create the SSL certificate for localhost. """

	print( 'Creating localhost.crt and localhost.key files...' )

	try:
		configfile = tempfile.NamedTemporaryFile( delete = False )
		configfile.write( b'[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth' )
		configfile.close()

		tempdir = tempfile.gettempdir()
		certfile = os.path.join( tempdir, 'imitateapi_localhost.crt' )
		keyfile = os.path.join( tempdir, 'imitateapi_localhost.key' )

		completed = subprocess.run(
			[
				'openssl', 'req', '-x509',
				'-days', '365',
				'-out', certfile,
				'-keyout', keyfile,
				'-newkey', 'rsa:2048',
				'-nodes',
				'-sha256',
				'-subj', '/CN=localhost',
				'-extensions', 'EXT',
				'-config', configfile.name
			],
			check = True,
			stderr = subprocess.PIPE,
			universal_newlines = True
		)
		print( 'Done.' )
	except subprocess.CalledProcessError as err:
		print( 'openssl error:\n%s' % err.stderr )

	if configfile and os.path.exists( configfile.name ):
		os.unlink( configfile.name )

	return certfile, keyfile



class localserver( localhttp.localserver ):


	def __init__( self, port, certfile, keyfile ):
		"""
		Parameters:
		port     (int) -- Port to run the local server on.
		certfile (str) --
		keyfile  (str) --
		"""

		if not certfile or not keyfile:
			certfile, keyfile = create_localhost_cert()

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
