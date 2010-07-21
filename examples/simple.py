from pyrepl.unix_console import UnixConsole

from pyrepl_livesearch import SearchingReader


class MyReader(SearchingReader):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', [])
        super(MyReader, self).__init__(*args, **kwargs)
        self.options = options
        self.enumerate = True

    def get_matches(self):
        pos, word = self.current_word()
        match = lambda option: option.startswith(word)
        return filter(match, self.options) if word else []

    def insert_match(self, match):
        pos, word = self.current_word()
        if match.startswith(word):
            self.insert(match[len(word):])
        else:
            buffer = self.buffer
            buffer[pos:pos + len(word)] = map(None, match)
            self.pos = pos + len(match)
            self.refresh()

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
