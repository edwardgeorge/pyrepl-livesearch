from pyrepl.unix_console import UnixConsole

from pyrepl_livesearch import SearchingReader


class MyReader(SearchingReader):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', [])
        super(MyReader, self).__init__(*args, **kwargs)
        self.options = options
        self.enumerate = True

    def get_matches(self):
        line = self.get_unicode()
        match = lambda option: option.startswith(line)
        return filter(match, self.options) if line else []

if __name__ == '__main__':
    con = UnixConsole()
    options = ['apple', 'orange', 'pineapple', 'lemon', 'melon', 'angela']
    reader = MyReader(con, options=options)
    while True:
        try:
            print reader.readline()
        except KeyboardInterrupt, e:
            pass
        except EOFError, e:
            break
