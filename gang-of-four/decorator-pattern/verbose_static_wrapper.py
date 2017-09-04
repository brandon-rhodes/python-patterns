# Traditional decorator: terribly verbose

class AllCapsFileWrapper(object):
    def __init__(self, file):
        self.file = file

    def __enter__(self):
        return self.file.__enter__()

    def __exit__(self, *excinfo):
        return self.file.__exit__(*excinfo)

    def __iter__(self):
        return self.file.__iter__()

    def __next__(self):
        return self.file.__next__()

    def __repr__(self):
        return self.file.__repr__()

    def close(self):
        return self.file.close()

    @property
    def closed(self):
        return self.file.closed

    @closed.setter
    def closed(self, value):
        self.file.closed = value

    @closed.deleter
    def closed(self):
        del self.file.closed

    @property
    def encoding(self):
        return self.file.encoding()

    @encoding.setter
    def encoding(self, value):
        self.file.encoding = value

    @encoding.deleter
    def encoding(self):
        del self.file.encoding

    @property
    def errors(self):
        return self.file.errors()

    @errors.setter
    def errors(self, value):
        self.file.errors = value

    @errors.deleter
    def errors(self):
        del self.file.errors

    def fileno(self):
        return self.file.fileno()

    def flush(self):
        return self.file.flush()

    def isatty(self):
        return self.file.isatty()

    @property
    def mode(self):
        return self.file.mode

    @mode.setter
    def mode(self, value):
        self.file.mode = value

    @mode.deleter
    def mode(self):
        del self.file.mode

    @property
    def name(self):
        return self.file.name

    @name.setter
    def name(self, value):
        self.file.name = value

    @name.deleter
    def name(self):
        del self.file.name

    @property
    def newlines(self):
        return self.file.newlines

    @newlines.setter
    def newlines(self, value):
        self.file.newlines = value

    @newlines.deleter
    def newlines(self):
        del self.file.newlines

    def read(self, *args):
        return self.file.read(*args)

    def readinto(self, buffer):
        return self.file.readinto(buffer)

    def readline(self, *args):
        return self.file.readline(*args)

    def readlines(self, *args):
        return self.file.readlines(*args)

    def seek(self, *args):
        return self.file.seek(*args)

    def tell(self):
        return self.file.tell()

    def truncate(self, *args):
        return self.file.truncate(*args)

    def write(self, s):
        if not isinstance(s, (bytes, str)):
            raise TypeError('you can only write str or bytes to a file')
        return self.file.write(s.upper())

    def writelines(self, strings):
        if self.closed:
            raise ValueError('this file is closed')
        for s in strings:
            self.write(s)
