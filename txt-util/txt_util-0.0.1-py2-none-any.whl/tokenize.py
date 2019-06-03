# -*- coding: utf-8 -*-


def sent_tokenize(txt):
    from nltk import sent_tokenize as sento
    from preprocessing import fix_sent
    import re
    from pos_tagging import tagging

    txt = fix_sent(txt)
    # str_in_q = ur'\'([^\']*)\''
    str_in_dq = ur'"([^"]*)"'

    # single_qoute_strs = re.findall(str_in_q, txt)
    double_qoute_strs = re.findall(str_in_dq, txt)

    # quote_label_dic = dict([("'" + key + "'", '[QUOTE_' + str(i) + ']') for i, key in enumerate(single_qoute_strs)])
    # single_len = len(quote_label_dic)
    # quote_label_dic.update(
    #     dict([('"' + key + '"', '[QUOTE_' + str(i + single_len) + ']') for i, key in enumerate(double_qoute_strs)]))

    quote_label_dic = dict([("'" + key + "'", '[QUOTE_' + str(i) + ']') for i, key in enumerate(double_qoute_strs)])

    label_quote_dic = dict(zip(*zip(*quote_label_dic.items())[::-1]))

    for q, label in quote_label_dic.items():
        txt = txt.replace(q, label)

    del quote_label_dic
    # print(txt)
    sentences = []
    txt_sents = sento(txt)
    if txt_sents[0].count('=')>0:
        txt_sents[0] = txt_sents[0].split('=')[1]
    quote_pat = ur'\[QUOTE_[0-9]+\]'
    # print txt_sents[0]
    for sent in txt_sents:
        # print sent
        quotes_in_sent = re.findall(quote_pat, sent)
        if len(quotes_in_sent) > 0:
            for q in quotes_in_sent:
                sent = sent.replace(q, label_quote_dic[q])
        """
        res = dep_parse_result(sent, dump=False)
        morp = res[0]['morp']
        if (len(res) >1):
            morp += [m['morp'][0] for m in res[1:]]
        print morp
        morp = [m['lemma']+'/'+m['type'] for m in morp]
        """
        # sent = ['<start>'] + tagging(sent) + ['<end>']    # MORPH

        sentences.append(sent)

    del label_quote_dic
    return sentences
