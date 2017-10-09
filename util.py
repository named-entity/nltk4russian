# coding: utf-8

import codecs
from itertools import izip
from BeautifulSoup import BeautifulSoup
from pymorphy2 import MorphAnalyzer

DELTAGS = ['impf', 'perf', 'excl', 'GNdr', 'tran', 'intr', 'anim', 'inan', 'real', 'intg', 'Infr', 'Slng', 'Arch',
          'Litr', 'Erro', 'Dist', 'Ques', 'Dmns', 'V-be', 'V-en', 'V-ie', 'V-bi', 'Fimp', 'Prdx', 'Coun', 'Coll',
          'V-sh', 'Af-p', 'Inmx', 'Vpre', 'Anph', 'Init', 'Impe', 'Uimp', 'Mult', 'Refl', 'Abbr', 'Name', 'Surn',
          'Patr', 'Geox', 'Orgn', 'Trad', 'Subx', 'Supr', 'Qual', 'Apro', 'Anum', 'Poss', 'V-ey', 'V-oy', 'Cmp2',
          'V-ej', 'Ms-f', 'Sgtm', 'Pltm', 'Fixd']


def read_corpus_to_nltk(inc):
    sent = []
    for t in inc:
        t = t.rstrip().decode('utf-8')
        if not t:
            continue
        if t == u'sent':
            sent = []
            continue
        if t == u'/sent' or t == u'SENT':
            yield sent
            continue
        t = t.split('\t')
        try:
            # token = (t[1], t[2].split()[1], ','.join(t[2].split(' ')[2:]))
            token = (t[1], ','.join(t[2].split(' ')[2:]))
            sent.append(token)
        except:
            continue


# читаем тестовый корпус -  plain text
def read_test_corpus(fn):
    m = MorphAnalyzer()
    for line in fn:
        line = line.rstrip('\n')
# считаем, что текст у нас уже токенизованный
#        line = word_tokenize(line)
        line = line.decode('utf-8').split()
# разбираем слова по словарю, возьмем только первый разбор от pymorphy
        parses = [m.parse(token) for token in line]
        if line:
            yield [(p[0].word, p[0].tag) for p in parses]


# читаем тестовый корпус - tsv
def read_tab_corpus(inc):
    m = MorphAnalyzer()
    sent = []
    for t in inc:
        t = t.rstrip().decode('utf-8')
        if not t:
            continue
        if t == u'sent':
            sent = []
            continue
        if t == u'/sent' or t == u'SENT':
            sent = [x[0] for x in sent]
            parses = [m.parse(token) for token in sent]
            if sent:
                yield [(p[0].word, p[0].tag) for p in parses]
            continue
        t = t.split('\t')
        try:
            token = (t[1], ' '.join(t[2].split(' ')[2:]))
            sent.append(token)
        except IndexError:
            continue


def prettytag(tagslist, withcommas=False, first=False):
    # TODO: проверить и оптимизировать
    if first and len(tagslist):
        return tagslist[0].split(',')[0].replace('NUMR', 'NUMB')
    info1 = []
    if withcommas:
        tagslist1 = []
        for x in tagslist:
            tagslist1 += x.split(',')
    else:
        tagslist1 = tagslist
    for tag in tagslist1:
        if not (tag in DELTAGS):
            info1.append(tag)
        info2 = info1[1:]
        info2.sort()
        if len(info1):
            info1 = [info1[0].replace('NUMR', 'NUMB')] + info2

    restag = u','.join(info1)
    return restag


def get_tags_tokens(sent, first = False):
    tags = []
    tokens = []
    words = sent.findAll('token')
    for w in words:
        tokens.append(w.get('text'))

    for w in words:
        grams = w.findAll('g')
        tag = ''
        s = []
        for g in grams:
            s.append(g.get('v'))
        tag = prettytag(s, first)
        tags.append(tag)

    l = len(tags)
    tagstoks = [(tokens[i], tags[i]) for i in range(l)]
    return tags,tokens, tagstoks


def get_sentences(fn):
    f = codecs.open(fn, 'r', 'utf-8')
    s = f.read()
    f.close()
    soup = BeautifulSoup(s)
    ss = soup.findAll('sentence')

    return ss


def get_tags_tokens_from_tab(sent, withcommas=False, first = False):
    tags = []
    tokens = []

    for w in sent:
        ws = w.split(u'\t')
        if len(ws) < 2:
            continue
        tokens.append(ws[1])
        # TODO: проверить исключение
        try:
            info = ws[2].split()[2:]
        except:
            print ws
        tag = prettytag(info, withcommas, first)
        tags.append(tag)

    l = len(tags)
    tagstoks = [(tokens[i], tags[i]) for i in range(l)]
    return tags, tokens, tagstoks

def get_sentences_from_tab(fn):
    f = codecs.open(fn, 'r', 'utf-8')
    ls = f.readlines()
    f.close()
    ss = []
    for l in ls:
        if l.strip(u'\r\n') in (u'/sent', u'sent'):
            ss.append([])
        else:
            ss[-1].append(l.strip(u'\r\n'))
    return ss


def accuracy(reference, test, verbose=False):
    if len(reference) != len(test):
        raise ValueError("Lists must have the same length.")
    num_correct = 0
    if verbose:
        wrongs = []
    for x, y in izip(reference, test):
        if x == y:
            num_correct += 1
        elif verbose:
            wrongs.append((x, y))
    if verbose:
        return float(num_correct) / len(reference), wrongs
    return float(num_correct) / len(reference)
