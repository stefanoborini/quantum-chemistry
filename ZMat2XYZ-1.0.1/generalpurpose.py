class ParseError(Exception):
	def __init__(self, message, filename="Unknown", linenum="Unknown"):
		self.__message = message
		self.__filename = filename
		self.__linenum = linenum
	def __str__(self):
		string = 'Error parsing file \"%s\":%s : %s' % (self.__filename,self.__linenum,self.__message)
		return string

