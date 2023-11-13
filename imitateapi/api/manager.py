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
			index_path = os.path.join( entry.get( 'path' ), 'index.json' )

			if os.path.isfile( index_path ):
				subentries = self._extend_from_index( entry )

				for subentry in subentries:
					self._available[subentry.get( 'name' )] = {
						'loaded': False,
						'path': subentry.get( 'path' ),
						'file': subentry.get( 'file' ),
						'parent': index_path,
					}
			else:
				self._available[entry.get( 'name' )] = {
					'loaded': False,
					'path': entry.get( 'path' ),
					'parent': None,
				}


	def _extend_from_index( self, entry ):
		subentries = []
		file_path = os.path.join( entry.get( 'path' ), 'index.json' )

		with open( file_path ) as f:
			content = f.read()

		# Allow lines with comments if they start with "//".
		# Remove those here, so the JSON can be parsed.
		p = re.compile( '^[\t ]*//.*', re.MULTILINE )
		content = p.sub( '', content )

		index = json.loads( content )
		list = index.get( 'variants' )

		for variant in list:
			subentry = {
				'name': entry.get( 'name' ) + ':' + variant.get( 'id' ),
				'path': entry.get( 'path' ),
				'file': os.path.join( entry.get( 'path' ), variant.get( 'file' ) ),
			}
			subentries.append( subentry )

		return subentries


	def _handle_index_file( self, info ):
		api_dict = APIManager.get_json( info.get( 'file' ) )

		if info.get( 'parent' ) is not None:
			base_dict = APIManager.get_json( info.get( 'parent' ) )
			base_rules = base_dict.get( 'rules' )
			info_rules = api_dict.get( 'rules' )

			if base_rules is not None:
				if info_rules is not None:
					base_rules.extend( info_rules )

				api_dict['rules'] = base_rules

		rules = APIRuleSet( info.get( 'path' ), api_dict )

		return rules


	def _handle_rules_file( self, path_base, file_path ):
		api_dict = APIManager.get_json( file_path )
		rules = APIRuleSet( path_base, api_dict )

		return rules


	def get_json( file_path ):
		with open( file_path ) as f:
			content = f.read()

		# Allow lines with comments if they start with "//".
		# Remove those here, so the JSON can be parsed.
		p = re.compile( '^[\t ]*//.*', re.MULTILINE )
		content = p.sub( '', content )

		return json.loads( content )


	def load_api( self, name ):
		"""
		Parameters
		----------
		name: str
			Directory name of the API to load.

		Returns
		-------
		APIRuleSet
		"""

		info = self._available.get( name )
		path_base = info.get( 'path' )
		json_file_path_rules = os.path.join( path_base, 'rules.json' )

		if info.get( 'file' ) is not None:
			return self._handle_index_file( info )
		elif os.path.isfile( json_file_path_rules ):
			return self._handle_rules_file( path_base, json_file_path_rules )
		else:
			raise Exception( '[APIManager.load_api] ERROR: Neither "index.json" nor "rules.json" file exists in %s' % path_base )


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
		keys = sorted( self._available )

		for key in keys:
			entry = self._available.get( key )
			path = entry.get( 'file' ) or entry.get( 'path' )
			print( format_str % ( key, path ) )
