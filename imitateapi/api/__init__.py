import json, mimetypes, os, re



class APIManager:


	def __init__( self, api_dir ):
		"""
		Parameters:
		api_dir (str) -- Path to the directory where API files are located.
		"""

		mimetypes.init()

		self._directory = api_dir
		self._available = {}

		in_dir = self.read_from_dir( self._directory )

		for entry in in_dir:
			self._available[entry.get( 'name' )] = {
				'loaded': False,
				'path': entry.get( 'path' )
			}


	def load_api( self, name ):
		"""
		Parameters:
		name (str) -- Directory name of the API to load.
		"""

		info = self._available.get( name )
		json_file_path = os.path.join( info.get( 'path' ), 'rules.json' )

		if not os.path.isfile( json_file_path ):
			raise Exception( '[APIManager.load_api] ERROR: File does not exist: %s' % json_file_path )

		with open( json_file_path ) as f:
			content = f.read()

		# Allow lines with comments if they start with "//".
		# Remove those here, so the JSON can be parsed.
		p = re.compile( '^[\t ]*//.*', re.MULTILINE )
		content = p.sub( '', content )

		api_dict = json.loads( content )
		rules = APIRuleSet( info.get( 'path' ), api_dict )

		return rules


	def read_from_dir( self, api_dir ):
		"""
		Parameters:
		api_dir (str) --
		"""

		api_list = []
		found_names = []

		with os.scandir( api_dir ) as contents:
			for entry in contents:
				if not entry.is_dir():
					continue

				if entry.name in found_names:
					print( 'WARNING: API "%s" has already been found and will not be added again.' % entry.name )
					continue

				# Scan __private sub directory.
				# "__private" can never be the name of an API.
				if entry.name == '__private':
					private_list = self.read_from_dir( entry.path )
					api_list.extend( private_list )

					[found_names.append( sub.get( 'name' ) ) for sub in private_list]
				# Add the found API directory.
				else:
					api_list.append( {
						'name': entry.name,
						'path': entry.path
					} )

					found_names.append( entry.name )

		return api_list


	def print_available( self ):
		""" Print the found API directories. """

		max_length = 0

		for key in self._available:
			max_length = max( max_length, len( key ) )

		format_str = 'API found: %%-%ds (%%s)' % max_length

		for key in self._available:
			entry = self._available.get( key )
			print( format_str % ( key, entry.get( 'path' ) ) )



class APIRuleSet:


	def __init__( self, api_dir, data ):
		"""
		Parameters:
		api_dir (str)  --
		data    (dict) --
		"""

		self._dir = api_dir
		self._data = data


	def _get_response_include( self, rule_response ):
		"""
		Parameters:
		rule_response (dict) --
		"""

		include_file = rule_response.get( 'include' )
		include_file = os.path.join( self._dir, include_file )

		content = None
		content_type = mimetypes.guess_type( include_file )[0]

		with open( include_file, mode = 'rb' ) as file:
			content = file.read()

		if 'headers' in rule_response:
			headers = rule_response.get( 'headers' )

			if 'Content-Type' in headers:
				content_type = None

		return content, content_type


	def get_first_matching_rule( self, req_method, req_path, req_headers ):
		"""
		Parameters:
		req_method  (str)  --
		req_path    (str)  --
		req_headers (dict) --
		"""

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
		res_message = ''
		res_headers = None

		req_method = request_handler.command
		req_path = request_handler.path
		req_headers = request_handler.headers

		rule = self.get_first_matching_rule( req_method, req_path, req_headers )

		if rule and 'response' in rule:
			rule_response = rule.get( 'response' )

			# 1. Set status code.
			if 'status' in rule_response:
				res_status = rule_response.get( 'status' )

			# 2. Set headers.
			if 'headers' in rule_response:
				res_headers = rule_response.get( 'headers' )

			# 3a. Set body/message.
			if 'message' in rule_response:
				res_message = rule_response.get( 'message' )
			# 3b. Set body/message from a file.
			elif 'include' in rule_response:
				content, content_type = self._get_response_include( rule_response )

				if content is not None:
					res_message = content

					# If response.status is not set and
					# the file is found, return code 200.
					if 'status' not in rule_response:
						res_status = 200

				# If reponse.headers.Content-Type is not given and the
				# file is found guess the mimetype and set it as header.
				if content_type is not None:
					if res_headers is None:
						res_headers = {}

					res_headers['Content-Type'] = content_type

		if res_headers is None:
			res_headers = {}

		if 'Content-Length' not in res_headers:
			res_headers['Content-Length'] = len( res_message )

		return res_status, res_message, res_headers
