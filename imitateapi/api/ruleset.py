# Built-in modules
from io import IOBase
from urllib.parse import quote
import mimetypes, os



def add_header_if_new( headers, key, value ):
	"""
	Parameters:
	headers (dict|None)       --
	key     (str)             --
	value   (None|number|str) --
	"""

	if value is None:
		return headers

	if headers is None:
		headers = {}

	if key not in headers:
		headers[key] = str( value )

	return headers


def get_content_type( filepath ):
	"""
	Get the content type of a file for the Content-Type HTTP header.
	Based on the MIME type (guessed) and with charset (UTF-8) for text files.

	Parameters:
	filepath (str) --
	"""

	content_type = mimetypes.guess_type( filepath )[0]

	if isinstance( content_type, str ):
		if (
			content_type.startswith( 'text/' ) or
			content_type.endswith( '/html' ) or
			content_type.endswith( '/json' ) or
			content_type.endswith( '/xml' )
		):
			content_type += '; charset=utf-8'
	else:
		content_type = 'application/octet-stream'

	return content_type


def get_download_filename( rule_response ):
	"""
	Parameters:
	rule_response (dict) --
	"""

	filename = 'download'

	if 'name' in rule_response:
		filename = rule_response.get( 'name' )
	else:
		download_path = rule_response.get( 'download' )
		filename = os.path.basename( download_path )

	return filename



class APIRuleSet:


	def __init__( self, api_dir, data ):
		"""
		Parameters:
		api_dir (str)  --
		data    (dict) --
		"""

		self._dir = api_dir
		self._data = data


	def _get_response_download( self, rule_response, res_headers ):
		"""
		Parameters:
		rule_response (dict)      --
		res_headers   (dict|None) --
		"""

		download_file = rule_response.get( 'download' )
		download_file = os.path.join( self._dir, download_file )

		content_type = get_content_type( download_file )
		content_length = os.path.getsize( download_file )

		res_status = 200
		res_message = open( download_file, mode = 'rb' )

		filename = get_download_filename( rule_response )

		res_headers = add_header_if_new( res_headers, 'Content-Type', content_type )
		res_headers = add_header_if_new( res_headers, 'Content-Length', content_length )
		res_headers = add_header_if_new(
			res_headers, 'Content-Disposition',
			"attachment; filename*=UTF-8''%s" % quote( filename, safe = '' )
		)

		return res_status, res_message, res_headers


	def _get_response_include( self, rule_response, res_headers ):
		"""
		Parameters:
		rule_response (dict)      --
		res_headers   (dict|None) --
		"""

		include_file = rule_response.get( 'include' )
		include_file = os.path.join( self._dir, include_file )

		res_status = 200
		res_message = None

		with open( include_file, mode = 'rb' ) as file:
			res_message = file.read()

		if 'status' in rule_response:
			res_status = rule_response.get( 'status' )

		content_type = get_content_type( include_file )
		res_headers = add_header_if_new( res_headers, 'Content-Type', content_type )

		return res_status, res_message, res_headers


	def _get_response_message( self, rule_response, res_headers ):
		"""
		Parameters:
		rule_response (dict) --
		res_headers   (dict) --
		"""

		res_status = 200
		res_message = rule_response.get( 'message' )

		if isinstance( res_message, str ):
			res_headers = add_header_if_new( res_headers, 'Content-Type', 'text/plain; charset=utf-8' )

		return res_status, res_message, res_headers


	def get_first_matching_rule( self, request_handler ):
		"""
		Parameters:
		request_handler (APIRequestHandler) --
		"""

		req_method = request_handler.command
		req_path = request_handler.path
		req_headers = request_handler.headers

		data_rules = self._data.get( 'rules' )
		matching_rule = None

		for rule in data_rules:
			rule_methods = rule.get( 'methods' )
			rule_path = rule.get( 'path' )

			if req_method not in rule_methods:
				continue

			if rule_path:
				if not req_path.startswith( rule_path ):
					continue

			matching_rule = rule
			break

		return matching_rule


	def get_request_response( self, request_handler ):
		"""
		Parameters:
		request_handler (APIRequestHandler) -- The request handler instance.
		"""

		res_status = 500
		res_message = None
		res_headers = None

		rule = self.get_first_matching_rule( request_handler )

		if rule and 'response' in rule:
			rule_response = rule.get( 'response' )

			# Set headers first so they have precedence.
			if 'headers' in rule_response:
				res_headers = rule_response.get( 'headers' )

			# Set body/message.
			if 'message' in rule_response:
				res_status, res_message, res_headers = self._get_response_message( rule_response, res_headers )
			# Set body/message from a file.
			elif 'include' in rule_response:
				res_status, res_message, res_headers = self._get_response_include( rule_response, res_headers )
			# Stream message from a file for download.
			elif 'download' in rule_response:
				res_status, res_message, res_headers = self._get_response_download( rule_response, res_headers )

			# Set status if part of rule, overwriting previous value.
			if 'status' in rule_response:
				res_status = rule_response.get( 'status' )

		# Convert str to bytes-like object.
		if isinstance( res_message, str ):
			res_message = str.encode( res_message )

		if res_message is not None and not isinstance( res_message, IOBase ):
			res_headers = add_header_if_new( res_headers, 'Content-Length', len( res_message ) )

		return res_status, res_message, res_headers
