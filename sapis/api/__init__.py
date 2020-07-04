import os



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



class APIParser:


	def __init__( self ):
		pass



class APIRuleSet:


	def __init__( self ):
		pass