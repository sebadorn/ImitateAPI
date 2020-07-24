# Built-in modules
from http import server
import ssl

# Project modules
from ..localhttp.localserver import LocalServerHTTP
from . import create_localhost_cert



class LocalServerHTTPS( LocalServerHTTP ):


	def __init__( self, port, certfile, keyfile ):
		"""
		Parameters:
		port     (int) -- Port to run the local server on.
		certfile (str) --
		keyfile  (str) --
		"""

		if not certfile or not keyfile:
			certfile, keyfile = create_localhost_cert()

		self.httpd = server.ThreadingHTTPServer( ( '', port ), localhttp.APIRequestHandler )

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
