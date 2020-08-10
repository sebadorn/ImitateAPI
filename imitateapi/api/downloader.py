# Built-in modules
import json, os, shutil, tarfile, urllib.request

# Project modules
from .. import info
from ..logger import Logger



class APIDownloader:


	def __init__( self ):
		pass


	def _download_archive( self, api_id, url_archive, callback = None ):
		"""
		Parameters
		----------
		api_id      : str
		url_archive : str
		callback    : function, optional
		"""

		extract_to_dir = info.get_user_appdata_dir()
		out_file_path = os.path.join( extract_to_dir, api_id + '.tar.gz' )

		with open( out_file_path, 'wb' ) as out_file:
			try:
				with urllib.request.urlopen( url_archive ) as response:
					shutil.copyfileobj( response, out_file )
			except urllib.error.URLError as err:
				Logger.error( 'Connecting to %s failed.' % url_archive )

		with tarfile.open( out_file_path ) as tar:
			tar.extractall( extract_to_dir )

		os.unlink( out_file_path )

		if callable( callback ):
			callback()

		# TODO: handle various possible errors, like timeout or 404
		# TODO: check if file already exists
		# TODO: be careful uncompressing (members argument?), handle invalid file


	def download( self, api_id, callback = None ):
		"""
		Download the API file from the URL and save it in the local directory.

		Parameters
		----------
		api_id   : str
			ID of the API to download.
		callback : function, optional
		"""

		def find_api_info( result ):
			found = False

			for item in result:
				if item.get( 'id' ) == api_id:
					found = True
					self._download_archive( api_id, item.get( 'download' ), callback )
					break

			if not found:
				Logger.error( 'Could not find API with ID "%s" in repository list.' % api_id )

		self.list_online( find_api_info )


	def list_online( self, callback ):
		"""
		Parameters
		----------
		callback : function
		"""

		url = info.get_repository_index_url()

		try:
			with urllib.request.urlopen( url ) as f:
				content = f.read()
		except urllib.error.URLError as err:
			Logger.error( err )
			Logger.error( 'Connecting to "%s" failed.' % url )
			return

		# TODO: handle various possible errors, like timeout or 404

		index_dict = json.loads( content )

		callback( index_dict.get( 'list' ) )


	def print_online( self ):
		def print_result( result ):
			print( 'APIs in the repository:' )
			print( '-----------------------' )

			for api in result:
				api_id = api.get( 'id' )
				name = api.get( 'name' )
				version = api.get( 'v' )
				print( '  [%s] v%s - %s' % ( api_id, version, name ) )

		self.list_online( print_result )
