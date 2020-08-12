# Built-in modules
from http import server
import ssl

# Project modules
from . import create_localhost_cert
from ..localhttp.apirequesthandler import APIRequestHandler
from ..localhttp.localserver import LocalServerHTTP
from ..logger import Logger



class LocalServerHTTPS( LocalServerHTTP ):


	def __init__( self, port, certfile, keyfile ):
		"""
		Parameters
		----------
		port     : int
			Port to run the local server on.
		certfile : str
		keyfile  : str
		"""

		self.httpd = None

		if not certfile or not keyfile:
			certfile, keyfile = create_localhost_cert()

		if not certfile or not keyfile:
			Logger.error( '[LocalServerHTTPS.__init__] No certfile and/or no keyfile. Cannot start HTTPS server.' )
			return

		if hasattr( server, 'ThreadingHTTPServer' ):
			self.httpd = server.ThreadingHTTPServer( ( '', port ), APIRequestHandler )
		else:
			Logger.warn(
				'http.server.ThreadingHTTPServer not available. '
				'Using fallback to http.server.HTTPServer instead.'
			)
			self.httpd = server.HTTPServer( ( '', port ), APIRequestHandler )

		self.httpd.socket = ssl.wrap_socket(
			self.httpd.socket,
			certfile = certfile,
			keyfile = keyfile,
			server_side = True
		)


	def start( self ):
		""" Start the local server. """

		if not self.httpd:
			Logger.error( '[LocalServerHTTPS.start] No HTTPS server running. Exiting.' )
			return

		print( 'A local HTTPS server will be available under: https://127.0.0.1:%d' % self.httpd.server_port )
		print( '----------' )

		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			print( '\n----------' )
			Logger.info( 'Application has been terminated by user.' )
