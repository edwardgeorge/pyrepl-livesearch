from pyrepl import commands
from pyrepl.reader import Reader

from pyrepl_livesearch import helpers


class search(commands.Command):
    def do(self):
        r = self.reader
        if not r._curmatches:
            r.error('no matches')
        elif len(r._curmatches) == 1:
            r.insert_match(r._curmatches[0])
        else:
            event = r.console.get_event()
            if event.evt == 'key' and event.data.isnumeric():
                choice = int(event.data)
                if 1 <= choice <= r.maxmatches and choice <= len(r._curmatches):
                    r.insert_match(r._curmatches[choice - 1])
                    return
            r.error('invalid choice')


class SearchingReader(Reader):
    def __init__(self, *args, **kwargs):
        super(SearchingReader, self).__init__(*args, **kwargs)
        self.maxmatches = 5
        self.enumerate = False

    def collect_keymap(self):
        return super(SearchingReader, self).collect_keymap() + (
            (r'\t', search),)

    def current_word(self):
        return helpers.current_word(self.get_unicode(), self.pos)

    def _insert_screen(self, screen, insert):
        ly = self.lxy[1]
        screen[ly:ly] = insert
        self.screeninfo[ly:ly] = [(0, [])] * len(insert)
        self.cxy = self.cxy[0], self.cxy[1] + len(insert)
        return screen

    def calc_screen(self):
        screen = super(SearchingReader, self).calc_screen()
        matches = self.get_matches()[:self.maxmatches]
        self._curmatches = matches
        if self.enumerate:
            matches = ['%d. %s' % (i[0] + 1, i[1]) for i in enumerate(matches)]
        return self._insert_screen(screen, matches)

    def get_matches(self):
        return []

    def insert_match(self, match):
        pass
