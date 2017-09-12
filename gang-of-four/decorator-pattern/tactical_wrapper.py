# Tactical version of Decorator Pattern:
# what if you read the code, and the only thing
# the library really needs is the write() method?

class WriteLoggingFile2(object):
    def __init__(self, file, logger):
        self._file = file
        self._logger = logger

    def write(self, s):
        self._file.write(s)
        self._logger.debug('wrote %s bytes to %s', len(s), self._file)
