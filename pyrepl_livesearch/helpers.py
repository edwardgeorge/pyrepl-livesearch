def iterate_words(text):
    i = 0
    while True:
        offset = text.find(' ', i)
        if offset > -1:
            word = text[i: offset]
        else:
            word = text[i:]
        if word:
            yield i, word
        if offset == -1:
            break
        i = offset + 1


def current_word(buffer, pos):
    for i, j in iterate_words(buffer):
        if i + len(j) == pos:
            return i, j
