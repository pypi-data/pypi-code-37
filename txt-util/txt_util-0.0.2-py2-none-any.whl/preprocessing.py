# -*- coding: utf-8 -*-

SPECIAL_CHARS = u'＠§※☆★○●◎◇◆□■△▲▽▼→←←↑↓↔〓◁◀▷▶♤♠♡♥♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☜☞¶†‡↕↗↙↖↘♭♩♪♬〔〕｛｝‘’“”〔〕〈〉《》「」『』【】[]'
XML_SYMS = [u'&nbsp;', u'&lt;', u'&gt;', u'&amp;', u'&quot;', u'&apos;', u'&nbsp', u'&lt', u'&gt', u'&amp', u'&quot', u'&apos']


def fix_sent(txt):
    import re
    txt = re.sub(ur' ?\.[^ 0-9\n]?', ur' . ', txt)
    txt = re.sub(ur' ?\" ?', ur' " ', txt)
    # txt = re.sub(ur" ?\' ?", ur" ' ", txt)
    txt = re.sub(ur" ?, ?", ur" , ", txt)
    return txt

def kr_preprocessing(prj_path, cont):
    from util.cnch.replace_cn_kr import change

    cont = change(prj_path, cont)  # 한자 치환
    for symbol in XML_SYMS:
        cont = cont.replace(symbol,'')
    for ch in list(SPECIAL_CHARS):
        cont = cont.replace(ch,' ')

    return cont
def rm_xml_tags(cont):

    for symbol in XML_SYMS:
        cont = cont.replace(symbol,'')

    return cont

# NOT FOR W2V, FOR CORPUS PADDING

def unk_prcessing(sentences, vocab_dic_by_freq, min_count=2, unk_tag=u'<unk>', already_cut=False):
    # vocab_dic_by_freq : { index1:(word1, count1), index2:(word2,count2), ...  }
    if already_cut is False:
        low_freq_words = []
        # print 'get low freq words'
        for w, c in vocab_dic_by_freq.values():

            if c < min_count:
                low_freq_words += [w]

        for sent in sentences:
            for i, w in enumerate(sent):
                if w in low_freq_words:
                    sent[i] = unk_tag
    else:
        if type(vocab_dic_by_freq) is list:
            vocab_dic_by_freq = dict(vocab_dic_by_freq)

        for sent in sentences:
            for i, w in enumerate(sent):
                if vocab_dic_by_freq.has_key(w) is False:
                    sent[i] = unk_tag

    return sentences


def padding(sentences, pad_length=20, pad_tag=u'PAD'):

    for i, s in enumerate(sentences):
        if len(s)<pad_length:
            sentences[i] = [pad_tag]*(pad_length-len(s))+s
    return sentences


if __name__ == "__main__":
    from itertools import chain
    sentences = [u'나는 오늘 학교 갔다',u'나는 학교 밥을 먹었다', u'오늘 학교 재밌었다']
    sentences = [s.split() for s in sentences]

    vocab_dic_by_freq = {}
    words = list(chain.from_iterable(sentences))
    vocabs = list(set(words))

    for i, w in enumerate(vocabs):
        vocab_dic_by_freq[i] = (w, words.count(w))

    new_sentences = unk_prcessing(sentences, vocab_dic_by_freq)
    new_sentences = padding(new_sentences, pad_length=5)
    for s in new_sentences:
        print ' '.join(s)
