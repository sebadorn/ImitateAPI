from http import server


class localserver:


	def __init__( self, port = 8000 ):
		self.httpd = server.HTTPServer( ( '', port ), server.BaseHTTPRequestHandler )


	def start( self ):
		print( 'A local HTTP server will be available under: http://127.0.0.1:%d' % self.httpd.server_port )
		print( '----------' )
		self.httpd.serve_forever()
