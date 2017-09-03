from StringIO import StringIO

def main():
    for module_name in 'decorator_verbose':
        original = StringIO()
        module = __import__(module_name)
        f = module.LinefeedCarriageReturnFile(original)
        f.write('Hello, world.')
        f.seek(2)
        assert f.read(5) == 'llo, '
        f.write('')

if __name__ == '__main__':
    main()
