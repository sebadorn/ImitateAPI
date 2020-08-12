# Built-in modules
import os, subprocess, tempfile
from shutil import which

# Project modules
from ..logger import Logger



def create_localhost_cert():
	"""
	Create the SSL certificate for localhost.

	Returns
	-------
	certfile : str
	keyfile  : str
	"""

	Logger.info( 'Creating localhost.crt and localhost.key files...' )

	if which( 'openssl' ) is None:
		Logger.error( '[create_localhost_cert] Command "openssl" cannot be found. Cannot create certificate files.' )
		return None, None

	try:
		configfile = tempfile.NamedTemporaryFile( delete = False )
		configfile.write( b'[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth' )
		configfile.close()

		tempdir = tempfile.gettempdir()
		certfile = os.path.join( tempdir, 'imitateapi_localhost.crt' )
		keyfile = os.path.join( tempdir, 'imitateapi_localhost.key' )

		completed = subprocess.run(
			[
				'openssl', 'req', '-x509',
				'-days', '365',
				'-out', certfile,
				'-keyout', keyfile,
				'-newkey', 'rsa:2048',
				'-nodes',
				'-sha256',
				'-subj', '/CN=localhost',
				'-extensions', 'EXT',
				'-config', configfile.name
			],
			check = True,
			stderr = subprocess.PIPE,
			universal_newlines = True
		)
		Logger.info( '... Certificate has been created.' )
	except subprocess.CalledProcessError as err:
		Logger.error( '[create_localhost_cert] openssl error:\n%s' % err.stderr )
		return None, None

	if configfile and os.path.exists( configfile.name ):
		os.unlink( configfile.name )

	return certfile, keyfile
