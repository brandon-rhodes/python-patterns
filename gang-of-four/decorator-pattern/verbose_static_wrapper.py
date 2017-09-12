# Traditional Decorator pattern: noticeably verbose

class WriteLoggingFile1(object):
    def __init__(self, file, logger):
        self._file = file
        self._logger = logger

    # We need to implement every file method,
    # and in the truly general case would need
    # a getter, setter, and deleter for every
    # single attribute!  Here goes:

    def __enter__(self):
        return self._file.__enter__()

    def __exit__(self, *excinfo):
        return self._file.__exit__(*excinfo)

    def __iter__(self):
        return self._file.__iter__()

    def __next__(self):
        return self._file.__next__()

    def __repr__(self):
        return self._file.__repr__()

    def close(self):
        return self._file.close()

    @property
    def closed(self):
        return self._file.closed

    @closed.setter
    def closed(self, value):
        self._file.closed = value

    @closed.deleter
    def closed(self):
        del self._file.closed

    @property
    def encoding(self):
        return self._file.encoding

    @encoding.setter
    def encoding(self, value):
        self._file.encoding = value

    @encoding.deleter
    def encoding(self):
        del self._file.encoding

    @property
    def errors(self):
        return self._file.errors

    @errors.setter
    def errors(self, value):
        self._file.errors = value

    @errors.deleter
    def errors(self):
        del self._file.errors

    def fileno(self):
        return self._file.fileno()

    def flush(self):
        return self._file.flush()

    def isatty(self):
        return self._file.isatty()

    @property
    def mode(self):
        return self._file.mode

    @mode.setter
    def mode(self, value):
        self._file.mode = value

    @mode.deleter
    def mode(self):
        del self._file.mode

    @property
    def name(self):
        return self._file.name

    @name.setter
    def name(self, value):
        self._file.name = value

    @name.deleter
    def name(self):
        del self._file.name

    @property
    def newlines(self):
        return self._file.newlines

    @newlines.setter
    def newlines(self, value):
        self._file.newlines = value

    @newlines.deleter
    def newlines(self):
        del self._file.newlines

    def read(self, *args):
        return self._file.read(*args)

    def readinto(self, buffer):
        return self._file.readinto(buffer)

    def readline(self, *args):
        return self._file.readline(*args)

    def readlines(self, *args):
        return self._file.readlines(*args)

    def seek(self, *args):
        return self._file.seek(*args)

    def tell(self):
        return self._file.tell()

    def truncate(self, *args):
        return self._file.truncate(*args)

    # Finally, we reach the two methods
    # that we actually want to specialize!
    # These log each time data is written:

    def write(self, s):
        self._file.write(s)
        self._logger.debug('wrote %s bytes to %s', len(s), self._file)

    def writelines(self, strings):
        if self.closed:
            raise ValueError('this file is closed')
        for s in strings:
            self.write(s)
