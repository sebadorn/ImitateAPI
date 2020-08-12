# Built-in modules
from http import server
from io import IOBase

# Project modules
from .. import info
from ..logger import Logger
from .apirequesthandler import APIRequestHandler



class LocalServerHTTP:


	def __init__( self, port ):
		"""
		Parameters
		----------
		port : int
			Port to run the local server on.
		"""

		if hasattr( server, 'ThreadingHTTPServer' ):
			self.httpd = server.ThreadingHTTPServer( ( '', port ), APIRequestHandler )
		else:
			Logger.warn(
				'http.server.ThreadingHTTPServer not available. '
				'Using fallback to http.server.HTTPServer instead.'
			)
			self.httpd = server.HTTPServer( ( '', port ), APIRequestHandler )


	def set_api( self, api ):
		"""
		Parameters
		----------
		api : api.APIRuleSet
		"""

		if not self.httpd:
			Logger.error( '[LocalServerHTTP.set_api] Server has not been created yet.' )
			return

		self.httpd.sapis_rules = api


	def start( self ):
		""" Start the local server. """

		if not self.httpd:
			Logger.error( '[LocalServerHTTP.start] No HTTP server running. Exiting.' )
			return

		print( 'A local HTTP server will be available under: http://127.0.0.1:%d' % self.httpd.server_port )
		print( '----------' )

		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			print( '\n----------' )
			Logger.info( 'Application has been terminated by user.' )
