# Tactical version of Decorator Pattern: implement only what you need

class WriteLoggingFile(object):
    def __init__(self, file):
        self.file = file

    def write(self, s):
        return self.file.write(s.upper())
