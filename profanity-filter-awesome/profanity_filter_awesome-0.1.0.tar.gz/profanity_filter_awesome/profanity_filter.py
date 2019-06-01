def censor(text, blacklist=()):
    output = ''

    for word in text.split():
        if word in blacklist:
            output += '***** '
            continue
        elif has_invalid_chars(word, ('*', '@',)):
            output += '***** '
            continue
        else:
            output += word + ' '

    return output


def has_invalid_chars(word, invalid_chars=()):
    for character in word:
        if character in invalid_chars:
            return True

    return False
