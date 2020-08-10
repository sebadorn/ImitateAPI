# Built-in modules
from http import server
from io import IOBase

# Project modules
from .. import info



class APIRequestHandler( server.SimpleHTTPRequestHandler ):


	def _handle_method( self ):
		self.server_version = 'ImitateAPI/' + info.get_version()

		if self.server.sapis_rules:
			status, message, headers = self.server.sapis_rules.get_request_response( self )

			self.send_response( status )

			if headers:
				for key in headers:
					self.send_header( key, headers.get( key ) )

			self.end_headers()

			if self.command != 'HEAD' and message is not None:
				if isinstance( message, IOBase ):
					self._send_file( message )
				else:
					self.wfile.write( message )
		else:
			self.end_headers()


	def _send_file( self, file ):
		"""
		Parameters
		----------
		file : io.IOBase
		"""

		chunk_size = 1 # MB
		chunk_size = chunk_size * 1024 * 1024 * 1024

		while True:
			chunk = file.read( chunk_size )

			if not chunk:
				break

			self.wfile.write( chunk )

		file.close()


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
