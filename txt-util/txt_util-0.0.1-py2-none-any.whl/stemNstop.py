# -*- coding:utf-8 -*-
# writer: Mia at 16. 12. 7, 
# last revision: 오후 9:47
##############################
# Stemming, Stop words  제거
##############################
def rm_punc(lines):
    from string import maketrans
    transtab = maketrans('!"#$%&\()*+,/:;<=>?@[\\]^_`{|}~.', ' ' * 31)  # 없앨 문장부호들
    
    return [line.lower().translate(transtab)  for line in lines]

def rm_punc_utf8(lines):
    specials = ['&nbsp;','&npbp','npsp']
    for s in specials:
        lines = lines.replace(s,'')
    puncs = u'◇·▲\'…!"#$%&\()〈〉*+,/:;<=>?@[\\]^_`{|}~\t\r\n'
    for p in puncs:
        lines = lines.replace(p, ' ')

    return lines

def stem_sentences(lines): #스테밍 + stop words
    from nltk.stem.porter import PorterStemmer  #Porter Stemmer
    from nltk.corpus import stopwords
    from string import maketrans
    transtab = maketrans('!"#$%&\()*+,/:;<=>?@[\\]^_`{|}~.', ' ' * 31)  # 없앨 문장부호들


    stm = PorterStemmer()
    st_words = stopwords.words('english')   # 영어 Stop words

    stm_lines =[]
    for line in lines:
        aline = line.translate(transtab)    # 문장부호 없애기
        aline = aline.lower()               # 소문자
        sted_line = [stm.stem(word) for word in aline.split()]  # 단어 스테밍
        stm_lines.append([ word for word in sted_line if word.lower() not in st_words]) # stop words 에 없으면 추가

    return stm_lines


if __name__ == "__main__":

    lines = ["this is string example....wow!!!", "Hello, World!"]
    print(rm_punc(lines))
