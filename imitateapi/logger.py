# Built-in modules
import logging



class Logger( object ):


	_logger = None


	@staticmethod
	def _log( fn, msg ):
		"""
		Parameters
		----------
		fn  : str
		msg : str or object
		"""

		getattr( Logger._logger, fn )( msg )


	@staticmethod
	def critical( msg ):
		"""
		Parameters
		----------
		msg : str or object
		"""

		Logger._log( 'critical', 'CRITICAL: ' + str( msg ) )


	@staticmethod
	def debug( msg ):
		"""
		Parameters
		----------
		msg : str or object
		"""

		Logger._log( 'debug', msg )


	@staticmethod
	def error( msg ):
		"""
		Parameters
		----------
		msg : str or object
		"""

		Logger._log( 'error', 'ERROR: ' + str( msg ) )


	@staticmethod
	def info( msg ):
		"""
		Parameters
		----------
		msg : str or object
		"""

		Logger._log( 'info', msg )


	@staticmethod
	def init( indent = 0 ):
		"""
		Parameters
		----------
		indent : int, optional
		"""

		logger = logging.getLogger( 'ImitateAPI' )
		logger.setLevel( logging.DEBUG )

		handler = logging.StreamHandler()
		handler.setLevel( logging.DEBUG )
		Logger._handler = handler

		logger.addHandler( handler )
		Logger._logger = logger

		Logger.setIndent( indent )


	@staticmethod
	def setIndent( indent ):
		"""
		Parameters
		----------
		indent : int
		"""

		if not Logger._handler:
			logging.error( 'No handler instance found. Has Logger.init() not been called yet?' )
			return

		spaces = indent * ' '
		formatter = logging.Formatter( spaces + '%(message)s' )
		Logger._handler.setFormatter( formatter )


	@staticmethod
	def setLevel( level ):
		"""
		Parameters
		----------
		level : int or str
		"""

		if isinstance( level, str ):
			level = level.lower()

			if level == 'critical':
				level = logging.CRITICAL
			elif level == 'debug':
				level = logging.DEBUG
			elif level == 'error':
				level = logging.ERROR
			elif level == 'info':
				level = logging.INFO
			elif level == 'warning':
				level = logging.WARNING

		Logger._handler.setLevel( level )


	@staticmethod
	def warn( msg ):
		"""
		Parameters
		----------
		msg : str or object
		"""

		Logger._log( 'warning', 'WARNING: ' + str( msg ) )
