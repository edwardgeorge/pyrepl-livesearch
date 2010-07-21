from pyrepl import commands
from pyrepl.reader import Reader


class search(commands.Command):
    def do(self):
        r = self.reader
        event = r.console.get_event()
        if event.evt == 'key' and event.data.isnumeric():
            choice = int(event.data)
            if 1 <= choice <= r.maxmatches:
                pass


class SearchingReader(Reader):
    def __init__(self, *args, **kwargs):
        super(SearchingReader, self).__init__(*args, **kwargs)
        self.maxmatches = 5
        self.enumerate = False

    def collect_keymap(self):
        return super(SearchingReader, self).collect_keymap() + (
            (r'\t', search),)

    def _insert_screen(self, screen, insert):
        ly = self.lxy[1]
        screen[ly:ly] = insert
        self.screeninfo[ly:ly] = [(0, [])] * len(insert)
        self.cxy = self.cxy[0], self.cxy[1] + len(insert)
        return screen

    def calc_screen(self):
        screen = super(SearchingReader, self).calc_screen()
        matches = self.get_matches()[:self.maxmatches]
        if self.enumerate:
            matches = ['%d. %s' % (i[0] + 1, i[1]) for i in enumerate(matches)]
        return self._insert_screen(screen, matches)

    def get_matches(self):
        return []
