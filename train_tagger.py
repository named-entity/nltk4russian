# coding: utf-8
"""
Документация по nltk.tag: http://www.nltk.org/api/nltk.tag.html
Документация по pymorphy2: https://pymorphy2.readthedocs.org/en/latest/user/guide.html#id3
Документация по opencorpora-tools: https://github.com/kmike/opencorpora-tools
Тестовый корпус можно давать в двух форматах: tsv (слово, лемма, разбор), между предложениями - SENT
и plain text (токенизованный)
"""


from opencorpora import CorpusReader
from argparse import ArgumentParser
from nltk.tag.sequential import TrigramTagger, BigramTagger, UnigramTagger
import sys

from tagger import PMContextTagger, PyMorphyTagger
from util import read_corpus_to_nltk, read_tab_corpus, read_test_corpus

taggers = {
    '3gram': TrigramTagger,
    '2gram': BigramTagger,
    '1gram': UnigramTagger,
    'pmcontext': PMContextTagger,
    'pymorphy': PyMorphyTagger,
}

p = ArgumentParser()
p.add_argument('-n', '--name', help='Tagger name', choices=taggers.keys())
p.add_argument('-f', '--file', help='Corpus to tag')
p.add_argument('-o', help='Output file')
p.add_argument('-full', default=False, action='store_true', help='use full tag to train and test tagger')
p.add_argument('-t', help='Training corpus in tsv format')
p.add_argument('-tab', default=False, action='store_true', help='test corpus is in tsv format.')
args = p.parse_args()

#if args.t:
with open(args.t, 'r') as tc:
    sents = list(read_corpus_to_nltk(tc))
#else:
#    corpus = CorpusReader('../data/annot.opcorpora.no_ambig.xml')
#    sents = list(corpus.iter_tagged_sents())

sents = filter(lambda x: len(x), sents)

if not args.full:
    print >> sys.stderr, 'Training %s on POS data...' % taggers[args.name].__name__
    pos_sents = []
    for s in sents:
        pos = []
        for w in s:
            if w[1].split(',')[0]:
                pos.append((w[0], w[1].split(',')[0]))
        pos_sents.append(pos)
    tagger = taggers[args.name](train=pos_sents)

else:
    print >> sys.stderr, 'Training %s on full tags...' % taggers[args.name].__name__
    tagger = taggers[args.name](sents)

if args.tab:
    read_test_corpus = read_tab_corpus

with open(args.file, 'r') as f:
    with open(args.o, 'w') as output:
        for sentence in read_test_corpus(f):
            tokens, tags = zip(*sentence)
            print >> output, 'sent'
            for i, t in enumerate(tagger.tag(tokens)):
                if not t[1]:
                    print >> output, u'\t'.join((str(i), t[0],
                                      u'%d d %s' % (i, str(tags[i])))).encode('utf-8')
                else:
                    print >> output, u'\t'.join((str(i), t[0],
                                      u'%d d %s' % (i, t[1]))).encode('utf-8')
            print >> output, '/sent'
