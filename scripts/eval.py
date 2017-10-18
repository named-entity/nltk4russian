#coding: utf-8
from __future__ import print_function

import sys
from argparse import ArgumentParser
from itertools import chain

from nltk4russian.util import get_sentences_from_tab, get_tags_tokens_from_tab, accuracy
#from nltk.metrics.scores import accuracy

_misc = ('Infr', 'Slng', 'Arch', 'Litr', 'Erro', 'Dist', 'Ques', 'Dmns', 'V-be', 'V-en', 'V-ie', 'V-bi',
         'Fimp', 'Prdx', 'Coun', 'Coll', 'V-sh', 'Af-p', 'Inmx', 'Vpre', 'Anph', 'Init', 'Impe', 'Uimp',
         'Mult', 'Refl', 'Abbr', 'Name', 'Surn', 'Patr', 'Geox', 'Orgn', 'Trad', 'Subx', 'Supr', 'Qual',
         'Apro', 'Anum', 'Poss', 'V-ey', 'V-oy', 'Cmp2', 'V-ej', 'Ms-f', 'Sgtm', 'Pltm', 'Fixd',
         'tran', 'intr', 'anim', 'inan', 'real', 'intg')

p = ArgumentParser()
p.add_argument('test')
p.add_argument('gold')
p.add_argument('-pos', default=True, action='store_true', help='use for POS evaluation')
p.add_argument('-full', default=False, action='store_true', help='use for full tag evaluation')
args = p.parse_args()


def pos(tag):
    return tag.split(',')[0]


def full(tag):
    return pos(tag) + ',' + ','.join(sorted(filter(lambda x: x not in _misc, tag.split(',')[1:])))


def precision(atagged, mtagged):
    s = 0.0
    tagged = 0.0
    mistagged = 0
    tokens = zip(atagged, mtagged)
    for t1, t2 in tokens:
        t1 = t1.rstrip('\r\n').decode('utf-8')
        t2 = t2.rstrip('\r\n').decode('utf-8')
        if u'sent' in t1 or not t1:
            s += 0.5
            continue
        tagged += 1
        t1, t2 = t1.split('\t'), t2.split('\t')
        if len(t1) < 3 or len(t2) < 3:
            print >> sys.stderr, t1, t2
            continue
        try:
            tag1, tag2 = ','.join(t1[2].split()[2:]), ','.join(t2[2].split()[2:])
        except:
            continue
        if args.full:
            tag1, tag2 = full(tag1), full(tag2)
        else:
            tag1, tag2 = pos(tag1), pos(tag2)
        if tag2 == 'UNKN':
            continue
        if tag1 != tag2:
#            print >> sys.stderr, tag1, tag2
            mistagged += 1
    return mistagged, tagged, s


inc = list(chain(*[get_tags_tokens_from_tab(x, withcommas=True)[2] for x in get_sentences_from_tab(args.test)]))
ref = list(chain(*[get_tags_tokens_from_tab(x, withcommas=True)[2] for x in get_sentences_from_tab(args.gold)]))
a, w = accuracy(inc, ref, verbose=True)
print(a)
