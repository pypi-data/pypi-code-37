# -*-coding:utf-8-*-


def slice(sents, wlen=114):
    from nltk import word_tokenize
    # print wlen, sents
    summary = []
    i=0
    _wlen = 0

    while _wlen < wlen:
        this_len = len(word_tokenize(sents[i]))
        if _wlen + this_len < wlen:
            _wlen += this_len
            summary.append(sents[i])
            i += 1
        else:
            break
    return '\n'.join(summary)
