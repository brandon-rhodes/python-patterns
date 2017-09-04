# Traditional decorator: terribly verbose

class WriteLoggingFile(object):
    def __init__(self, file):
        self.file = file

    def write(self, s):
        if not isinstance(s, (bytes, str)):
            raise TypeError('you can only write str or bytes to a file')
        return self.file.write(s.upper())

    def writelines(self, strings):
        if self.closed:
            raise ValueError('this file is closed')
        for s in strings:
            self.write(s)

    def __getattr__(self, name):
        return getattr(self.__dict__['file'], name)
