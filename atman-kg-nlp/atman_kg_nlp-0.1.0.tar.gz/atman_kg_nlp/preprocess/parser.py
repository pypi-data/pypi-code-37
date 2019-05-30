from ._stanford_nlp import LanguageCoreNLPClient
from ._benepar import *
from benepar import Parser as BeneparParser
import jieba
from enum import Enum
import json
from collections import OrderedDict


class Token(object):

    def __init__(self, doc, index, char_start, char_end):
        self.index = index
        self.doc = doc
        self.char_start = char_start
        self.char_end = char_end

    @property
    def text(self):
        return self.doc.text[self.char_start:self.char_end]

    def __repr__(self):
        return '({0},{1},{2})'.format(
            self.char_start,
            self.char_end,
            self.text)


class Span(object):

    def __init__(self, doc, start, end):
        self.doc = doc
        self.start = start
        self.end = end

    @property
    def char_start(self):
        return self.doc.tokens[self.start].char_start

    @property
    def char_end(self):
        return self.doc.tokens[self.end - 1].char_end

    @property
    def text(self):
        return self.doc.text[self.char_start:self.char_end]

    def __repr__(self):
        return '({0},{1},{2})'.format(
            self.char_start,
            self.char_end,
            self.doc.text[self.char_start:self.char_end])

    def __len__(self):
        return self.end - self.start


class Phrase(Span):

    def __init__(self, doc, start, end, tag):
        super().__init__(doc, start, end)
        self.tag = tag

    def __repr__(self):
        return '({0},{1},{2},{3})'.format(self.char_start, self.char_end,
                                          self.text,
                                          self.tag)


class Sentence(Span):

    def __init__(self, doc, start, end, index, constituency):
        self.index = index
        super().__init__(doc, start, end)
        self.constituency = constituency
        assert constituency is not None
        self._extract_phrases_from_constituency(constituency)

    def _extract_phrases_from_constituency(self, constituency):
        constituency = re.sub('\(PU  \)', '(PU -SPACE-)', constituency)
        tags = []
        phrase_starts = []
        tok_idx = self.start
        i = 0
        length = len(constituency)
        self.phrases = []
        while i < length:
            if constituency[i] == '(':
                i += 1
                prev = i
                while not str.isspace(constituency[i]):
                    i += 1
                tags.append(constituency[prev:i])
                phrase_starts.append(tok_idx)
            elif str.isspace(constituency[i]):
                i += 1
            elif constituency[i] == ')':
                pstart = phrase_starts.pop()
                tag = tags.pop()
                phrase = Phrase(self.doc, pstart, tok_idx, tag)
                self.phrases.append(phrase)
                i += 1
            else:
                prev = i
                while constituency[i] not in '()' \
                        and not str.isspace(constituency[i]):
                    i += 1
                tok_idx += 1
                tok_text = constituency[prev:i]

    def _extract_phrases_from_spacy(self, spacy_phrases):
        self.phrases = []
        for x, tag in spacy_phrases:
            if x.start >= self.start and x.end <= self.end:
                continue
            phrase = Phrase(self.doc, x.start, x.end, tag)
            self.phrases.append(phrase)

    @property
    def noun_adjective_phrases(self):
        for p in self.phrases:
            if p.tag in ['NN', 'ADJ', 'JJ', 'VA', 'NR', 'NP', 'NNP', 'NNS',
                         'VV', 'NOUN', 'ADJP']:
                yield p


class Section(object):

    def __init__(self, text=None, title=None,
                 corenlp_resp=None, spacy_doc=None,
                 benepar_tree=None, jstr=None):

        self.text = text
        self.title = title
        self.tokens = []
        self.sentences = []
        if jstr is None:
            if corenlp_resp is not None:
                assert spacy_doc is None and benepar_tree is None
                self._init_from_corenlp(corenlp_resp)
            elif spacy_doc is not None:
                assert benepar_tree is None
                self._init_from_spacy(spacy_doc)
            elif benepar_tree is not None:
                self._init_from_benepar_trees(trees=benepar_tree)
        else:
            self._init_from_json(jstr)

    def _init_from_corenlp(self, resp):
        assert isinstance(resp, dict)
        for jsent in resp['sentences']:
            for jtoken in jsent['tokens']:
                tok = Token(self, len(self.tokens),
                            jtoken['characterOffsetBegin'],
                            jtoken['characterOffsetEnd'])
                self.tokens.append(tok)
            sentence = Sentence(self,
                                len(self.tokens) - len(jsent['tokens']),
                                len(self.tokens),
                                len(self.sentences),
                                constituency=jsent['parse'])
            self.sentences.append(sentence)

    def _init_from_spacy(self, spacy_doc):
        assert isinstance(spacy_doc, Doc)
        for spacy_sent in spacy_doc.sents:
            for spacy_tok in spacy_sent:
                tok = Token(self, spacy_tok.i,
                            spacy_tok.idx,
                            spacy_tok.idx + len(spacy_tok))
                self.tokens.append(tok)
            sentence = Sentence(self,
                                len(self.tokens) - len(spacy_sent),
                                len(self.tokens),
                                len(self.sentences),
                                constituency=spacy_sent._.parse_string)
            self.sentences.append(sentence)

    def _init_from_benepar_trees(self, trees):
        char_offset = 0
        for tree in trees:
            for leaf in tree.leaves():
                if leaf == '-LRB-':
                    leaf = '（'
                elif leaf == '-RRB-':
                    leaf = '）'
                tok = Token(self, len(self.tokens), char_offset,
                            char_offset + len(leaf))
                char_offset += len(leaf)
                self.tokens.append(tok)
            sentence = Sentence(self,
                                len(self.tokens) - len(tree.leaves()),
                                len(self.tokens),
                                len(self.sentences),
                                constituency=str(tree))
            self.sentences.append(sentence)

    def _init_from_json(self, jstr):
        j = json.loads(jstr)
        self.text = j['text']
        if 'title' in j:
            self.title = j['title']
        for i, (cstart, cend) in enumerate(
                zip(j['tokens']['char_start'], j['tokens']['char_end'])):
            tok = Token(self, i, cstart, cend)
            self.tokens.append(tok)
        for i, (start, end, constituency) in enumerate(
                zip(j['sentences']['start'], j['sentences']['end'],
                    j['sentences']['constituency'], )):
            sentence = Sentence(self, start, end, i, constituency)
            self.sentences.append(sentence)

    def dumps(self):
        j = dict()
        j['text'] = self.text
        j['title'] = self.title
        tok_starts, tok_ends = [], []
        for tok in self.tokens:
            tok_starts.append(tok.char_start)
            tok_ends.append(tok.char_end)
        j['tokens'] = dict()
        j['tokens']['char_start'] = tok_starts
        j['tokens']['char_end'] = tok_ends

        sent_starts, sent_ends, sent_constituents = [], [], []
        for sent in self.sentences:
            sent_starts.append(sent.start)
            sent_ends.append(sent.end)
            sent_constituents.append(sent.constituency)
        j['sentences'] = dict()
        j['sentences']['start'] = sent_starts
        j['sentences']['end'] = sent_ends
        j['sentences']['constituency'] = sent_constituents
        return json.dumps(j)

    @property
    def phrases(self):
        for sent in self.sentences:
            for phrase in sent.phrases:
                yield phrase

    @property
    def noun_adjective_phrases(self):
        for sent in self.sentences:
            for phrase in sent.noun_adjective_phrases:
                yield phrase


class Document(object):

    def __init__(self, sections=None, jstr=None):
        self.sections = OrderedDict()
        if sections:
            for section in sections:
                self.sections[section.title] = section
        elif jstr:
            od = json.loads(jstr, object_pairs_hook=OrderedDict)
            for k, v in od.items():
                sec = Section(jstr=v)
                self.sections[k] = sec
        else:
            raise ValueError('Sections or json string need to be provided'
                             ' for initializing Document instance!')

    @property
    def text(self):
        t = '\n'.join([])
        return t

    @property
    def tokens(self):
        l = []
        for section in self.sections.values():
            l.extend(section.tokens)
        return l

    @property
    def sentences(self):
        l = []
        for section in self.sections.values():
            l.extend(section.sentences)
        return l

    @property
    def noun_adjective_phrases(self):
        l = []
        for section in self.sections.values():
            l.extend(section.noun_adjective_phrases)
        return l

    def dumps(self):
        od = OrderedDict()
        for sec in self.sections.values():
            od[sec.title] = sec.dumps()
        return json.dumps(od)


class UnderlyingModel(Enum):
    CORE_NLP = 'corenlp'
    BENEPAR = 'benepar'


class Language(Enum):
    EN = 'en'
    ZH = 'zh'


class AtmanParser(object):
    corenlp_client = None
    corenlp_counter = 0

    def __init__(self, model, language):
        self.model = model
        self.language = language
        if model == UnderlyingModel.CORE_NLP:
            AtmanParser.corenlp_counter += 1
            if AtmanParser.corenlp_client is None:
                AtmanParser.corenlp_client = LanguageCoreNLPClient()
        elif model == UnderlyingModel.BENEPAR:
            if self.language == Language.EN:
                self.benepar_model = spacy_nlp
            elif self.language == Language.ZH:
                self.benepar_model = BeneparParser("benepar_zh")
        else:
            raise NotImplementedError('The model type is not'
                                      ' supported yet: ' + model)

    def __del__(self):
        if self.model == UnderlyingModel.CORE_NLP:
            AtmanParser.corenlp_counter -= 1
            if AtmanParser.corenlp_counter == 0:
                AtmanParser.corenlp_client.stop()

    @staticmethod
    def _segment_zh_sentences(text):
        start = 0
        for i, c in enumerate(text):
            if c in '。！？!?':
                yield text[start:i + 1]
                start = i + 1
            if c == '.':
                if i == 0:
                    if not str.isdigit(text[i + 1]):
                        yield text[start:i + 1]
                        start = i + 1
                elif i == len(text) - 1:
                    if not str.isdigit(text[i - 1]):
                        yield text[start:]
                        start = i + 1
                else:
                    if not str.isdigit(text[i - 1]) \
                            and not str.isdigit(text[i + 1]):
                        yield text[start:i + 1]
                        start = i + 1
        if len(text[start:]) > 0:
            yield text[start:]

    @staticmethod
    def normalize_text(text):
        paragrahs = text.split('\n')
        new_paragrahs = []
        for paragrah in paragrahs:
            if paragrah.strip() == "":
                continue
            new_paragraph = ' '.join(re.split('\s+', paragrah.strip()))
            new_paragrahs.append(new_paragraph)
        return '\n'.join(new_paragrahs)

    def parse_section(self, title, content):
        normalized_content = self.normalize_text(content)
        if self.model == UnderlyingModel.CORE_NLP:
            response = self.corenlp_client \
                .annotate(normalized_content, annotators=['parse'],
                          language=self.language.value)
            return Section(normalized_content, title, corenlp_resp=response)
        elif self.model == UnderlyingModel.BENEPAR \
                and self.language == Language.EN:
            spacy_doc = self.benepar_model(normalized_content)
            return Section(normalized_content, title, spacy_doc=spacy_doc)
        elif self.model == UnderlyingModel.BENEPAR \
                and self.language == Language.ZH:
            bparser = BeneparParser("benepar_zh")
            trees = []
            for sent in self._segment_zh_sentences(normalized_content):
                toks = [x for x in jieba.cut(sent, cut_all=False)]
                tree = bparser.parse(toks)
                trees.append(tree)
            return Section(normalized_content, title, benepar_tree=trees)
        else:
            raise NotImplementedError(
                'The model is not supported yet:' + self.model)

    def parse(self, j):
        if isinstance(j, str):
            j = OrderedDict({'default': j})
        assert isinstance(j, OrderedDict)
        sections = []
        for title, content in j.items():
            sec = self.parse_section(title, content)
            sections.append(sec)
        return Document(sections)
