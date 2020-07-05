import json, os



class APIManager:


	def __init__( self, api_dir ):
		self._directory = api_dir
		self._available = {}

		in_dir = self.read_from_dir( self._directory )

		for entry in in_dir:
			self._available[entry.get( 'name' )] = {
				'loaded': False,
				'path': entry.get( 'path' )
			}


	def load_api( self, name ):
		info = self._available.get( name )
		json_file_path = os.path.join( info.get( 'path' ), 'rules.json' )

		if not os.path.isfile( json_file_path ):
			raise Exception( '[APIManager.load_api] ERROR: File does not exist: %s' % json_file_path )

		with open( json_file_path ) as f:
			content = f.read()

		api_dict = json.loads( content )
		rules = APIRuleSet( api_dict )

		return rules


	def read_from_dir( self, api_dir ):
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


	def __init__( self, data ):
		self._data = data


	def getRequestResponse( self, requestHandler ):
		"""
		Parameters:
		requestHandler (APIRequestHandler) -- The request handler instance.
		"""

		res_status = 500
		res_message = ''
		res_headers = None

		req_method = requestHandler.command
		req_path = requestHandler.path
		req_headers = requestHandler.headers

		rule = self.getFirstMatchingRule( req_method, req_path, req_headers )

		if rule:
			rule_response = rule.get( 'response' )

			if rule_response:
				res_status = rule_response.get( 'status' )
				res_message = rule_response.get( 'message' )
				res_headers = rule_response.get( 'headers' )

		return res_status, res_message, res_headers


	def getFirstMatchingRule( self, req_method, req_path, req_headers ):
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