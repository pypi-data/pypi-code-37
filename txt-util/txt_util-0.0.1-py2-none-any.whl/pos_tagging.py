# -*-coding:utf-8-*-

def tagging(sent):
    from konlpy.tag import Kkma
    kkma = Kkma()
    return [pos+'/'+tag for pos, tag in kkma.pos(sent)]

def tagging_no_tag(sent):
    from konlpy.tag import Kkma
    kkma = Kkma()
    return [pos for pos, tag in kkma.pos(sent)]

def get_nouns(sent):
    from konlpy.tag import Kkma
    kkma = Kkma()
    return kkma.nouns(sent)


def get_main_pos(sent):

    from konlpy.tag import Kkma
    kkma = Kkma()

    EXCEPT_TAG = [ 'X', 'E', 'J']
    return [pos for pos, tag in kkma.pos(sent) if tag not in EXCEPT_TAG]