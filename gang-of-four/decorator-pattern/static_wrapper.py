# Traditional decorator: terribly verbose

class LinefeedCarriageReturnFile(object):
    def __init__(self, file):
        self.file = file

    def __enter__(self):
        return self.file.__enter__()

    def __exit__(self, *excinfo):
        return self.file.__exit__(*excinfo)

    def __iter__(self):
        return self.file.__iter__()

    def __repr__(self):
        return self.file.__repr__()

    def close(self):
        return self.file.close()

    @property
    def closed(self):
        return self.file.closed()

    @closed.setter
    def closed(self, value):
        self.file.closed = value

    @property
    def encoding(self):
        return self.file.encoding()

    @encoding.setter
    def encoding(self, value):
        self.file.encoding = value

    @property
    def errors(self):
        return self.file.errors()

    @errors.setter
    def errors(self, value):
        self.file.errors = value

    def fileno(self):
        return self.file.fileno()

    def flush(self):
        return self.file.flush()

    def isatty(self):
        return self.file.isatty()

    @property
    def mode(self):
        return self.file.mode()

    @mode.setter
    def mode(self, value):
        self.file.mode = value

    @property
    def name(self):
        return self.file.name()

    @name.setter
    def name(self, value):
        self.file.name = value

    @property
    def newlines(self):
        return self.file.newlines()

    @newlines.setter
    def newlines(self, value):
        self.file.newlines = value

    def next(self):
        return self.file.next()

    def read(self, *args):
        return self.file.read(*args)

    def readline(self, *args):
        return self.file.readline(*args)

    def readlines(self, *args):
        return self.file.readlines(*args)

    def seek(self, offset, whence=0):
        return self.file.seek(offset, whence=whence)

    @property
    def softspace(self):
        return self.file.softspace()

    @softspace.setter
    def softspace(self, value):
        self.file.softspace = value

    def tell(self):
        return self.file.tell()

    def truncate(self, *args):
        return self.file.truncate(*args)

    def write(self):
        return self.file.write()

    def writelines(self, strings):
        for string in strings:
            self.write(string)

    def xreadlines(self):
        return self