from http import server



class APIRequestHandler( server.BaseHTTPRequestHandler ):


	def _handle_method( self, method ):
		if self.server.sapis_rules:
			status, message, headers = self.server.sapis_rules.getRequestResponse( self )

			if headers:
				for key in headers:
					self.send_header( key, headers.get( key ) )

			self.send_response( status, message )
			self.end_headers()
		else:
			self.end_headers()


	def do_CONNECT( self ):
		pass


	def do_DELETE( self ):
		self._handle_method( 'DELETE' )


	def do_GET( self ):
		self._handle_method( 'GET' )


	def do_HEAD( self ):
		pass


	def do_OPTIONS( self ):
		pass


	def do_PATCH( self ):
		pass


	def do_POST( self ):
		self._handle_method( 'POST' )


	def do_PUT( self ):
		self._handle_method( 'PUT' )


	def do_TRACE( self ):
		pass



class localserver:


	def __init__( self, port = 8000 ):
		self.httpd = server.HTTPServer( ( '', port ), APIRequestHandler )


	def set_api( self, api ):
		self.httpd.sapis_rules = api


	def start( self ):
		print( 'A local HTTP server will be available under: http://127.0.0.1:%d' % self.httpd.server_port )
		print( '----------' )
		self.httpd.serve_forever()
