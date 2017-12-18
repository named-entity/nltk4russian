#coding: utf-8
from __future__ import print_function

import sys
from argparse import ArgumentParser
from itertools import chain

from nltk4russian.util import get_sentences_from_tab, get_tags_tokens_from_tab, accuracy

p = ArgumentParser()
p.add_argument('test')
p.add_argument('gold')
p.add_argument('-pos', default=True, action='store_true', help='use for POS evaluation')
p.add_argument('-full', default=False, action='store_true', help='use for full tag evaluation')
args = p.parse_args()


inc = list(chain(*[get_tags_tokens_from_tab(x, withcommas=True)[2] for x in get_sentences_from_tab(args.test)]))
ref = list(chain(*[get_tags_tokens_from_tab(x, withcommas=True)[2] for x in get_sentences_from_tab(args.gold)]))
test_type = 'pos'
if args.full:
    test_type = 'full'
a, w = accuracy(inc, ref, verbose=True, test_type=test_type)
print(a)
