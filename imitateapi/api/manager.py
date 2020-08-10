# Built-in modules
import json, mimetypes, os, re

# Project modules
from ..logger import Logger
from .ruleset import APIRuleSet



class APIManager:


	def __init__( self, api_dir ):
		"""
		Parameters
		----------
		api_dir : str
			Path to the directory where API files are located.
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
		Parameters
		----------
		name : str
			Directory name of the API to load.

		Returns
		-------
		APIRuleSet
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
		Parameters
		----------
		api_dir : str

		Returns
		-------
		list of dicts
		"""

		api_list = []
		found_names = []

		with os.scandir( api_dir ) as contents:
			for entry in contents:
				if not entry.is_dir():
					continue

				if entry.name in found_names:
					Logger.warn( 'API "%s" has already been found and will not be added again.' % entry.name )
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
