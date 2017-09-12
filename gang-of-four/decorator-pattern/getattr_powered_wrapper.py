# Dynamic version of Decorator Pattern: intercept live attributes

class WriteLoggingFile3(object):
    def __init__(self, file, logger):
        self._file = file
        self._logger = logger

    # The two methods we actually want to specialize,
    # to log each occasion on which data is written.

    def write(self, s):
        self._file.write(s)
        self._logger.debug('wrote %s bytes to %s', len(s), self._file)

    def writelines(self, strings):
        if self.closed:
            raise ValueError('this file is closed')
        for s in strings:
            self.write(s)

    # Two methods we don't actually want to intercept,
    # but iter() and next() will be upset without them.

    def __iter__(self):
        return self.__dict__['_file'].__iter__()

    def __next__(self):
        return self.__dict__['_file'].__next__()

    # Offer every other method and property dynamically.

    def __getattr__(self, name):
        return getattr(self.__dict__['_file'], name)

    def __setattr__(self, name, value):
        if name in ('_file', '_logger'):
            self.__dict__[name] = value
        else:
            setattr(self.__dict__['_file'], name, value)

    def __delattr__(self, name):
        delattr(self.__dict__['_file'], name)
