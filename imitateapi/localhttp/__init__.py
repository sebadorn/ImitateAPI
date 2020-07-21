from http import server



class APIRequestHandler( server.BaseHTTPRequestHandler ):


	def _handle_method( self ):
		if self.server.sapis_rules:
			status, message, headers = self.server.sapis_rules.get_request_response( self )

			if headers:
				for key in headers:
					self.send_header( key, headers.get( key ) )

			self.send_response( status, message )
			self.end_headers()
		else:
			self.end_headers()


	def do_CONNECT( self ):
		self._handle_method()


	def do_DELETE( self ):
		self._handle_method()


	def do_GET( self ):
		self._handle_method()


	def do_HEAD( self ):
		self._handle_method()


	def do_OPTIONS( self ):
		self._handle_method()


	def do_PATCH( self ):
		self._handle_method()


	def do_POST( self ):
		self._handle_method()


	def do_PUT( self ):
		self._handle_method()


	def do_TRACE( self ):
		self._handle_method()



class localserver:


	def __init__( self, port ):
		"""
		Parameters:
		port (int) -- Port to run the local server on.
		"""

		self.httpd = server.HTTPServer( ( '', port ), APIRequestHandler )


	def set_api( self, api ):
		"""
		Parameters:
		api (api.APIRuleSet) --
		"""

		self.httpd.sapis_rules = api


	def start( self ):
		""" Start the local server. """

		print( 'A local HTTP server will be available under: http://127.0.0.1:%d' % self.httpd.server_port )
		print( '----------' )

		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			print( '\n----------' )
			print( 'Application has been terminated by user.' )
