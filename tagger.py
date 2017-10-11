# coding: utf-8

from __future__ import print_function

from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.tag.sequential import ContextTagger, SequentialBackoffTagger, NgramTagger
import pymorphy2


class PMContextTagger(NgramTagger):
    """
    """
    def __init__(self, train=None, model=None,
                 backoff=None, cutoff=0, verbose=False):
        self._morph = pymorphy2.MorphAnalyzer()
        self._contexts_to_tags = (model if model else {})
        NgramTagger.__init__(self, 1, train, model,
                             backoff, cutoff, verbose)

    def context(self, tokens, index, history):
        tag_context = tuple(history[max(0,index-1):index])
        return tag_context

    def choose_tag(self, tokens, index, history):
        context = self.context(tokens, index, history)

        s = self._morph.parse(tokens[index])
        tags = [x.tag.__str__().replace(u' ', u',') for x in s]
        if len(tags) == 0:
            return None
        if (len(tags) == 1) or not (context in self._contexts_to_tags.keys()):
            return tags[0]

        tagsconts = FreqDist()
        for tag in tags:
            #print 'TAG: ', tag
            #print tokens[index]
            tagsconts[tag] = self._contexts_to_tags[context].get(tag, 0)

            #print 'PROB: | ', context, tagsconts[tag]
        best_tag = tagsconts.max()
        if tagsconts[best_tag] == 0:
            return tags[0]
        return best_tag

    def _train(self, tagged_corpus, cutoff=0, verbose=False):
        """
        """
        token_count = hit_count = 0

        # A context is considered 'useful' if it's not already tagged
        # perfectly by the backoff tagger.
        useful_contexts = set()

        # Count how many times each tag occurs in each context.
        fd = ConditionalFreqDist()
        for sentence in tagged_corpus:
            tokens, tags = zip(*sentence)
            for index, (token, tag) in enumerate(sentence):
                # Record the event.
                token_count += 1
                context = self.context(tokens, index, tags[:index])
                if context is None: continue
                fd[context][tag] += 1
                # If the backoff got it wrong, this context is useful:
                if (self.backoff is None or
                    tag != self.backoff.tag_one(tokens, index, tags[:index])):
                    useful_contexts.add(context)

        # Build the context_to_tag table -- for each context, figure
        # out what the most likely tag is.  Only include contexts that
        # we've seen at least `cutoff` times.
        for context in useful_contexts:
            #best_tag = fd[context].max()
            for (tag, hits) in fd[context].items():
                if hits > cutoff:
                    self._contexts_to_tags[context] = self._contexts_to_tags.get(context, {})
                    self._contexts_to_tags[context][tag] = hits
                    hit_count += hits

        # Display some stats, if requested.
        if verbose:
            size = len(self._context_to_tag)
            backoff = 100 - (hit_count * 100.0)/ token_count
            pruning = 100 - (size * 100.0) / len(fd.conditions())
            print("[Trained Unigram tagger:")
            print("size=%d, backoff=%.2f%%, pruning=%.2f%%]" % (
                  size, backoff, pruning))

class PyMorphyTagger(SequentialBackoffTagger):
    """
    A tagger that assigns the most frequent tag according to PyMorphy2 statistics.
    """

    def __init__(self, train=None):
        self._morph = pymorphy2.MorphAnalyzer()
        SequentialBackoffTagger.__init__(self, None)

    def choose_tag(self, tokens, index, history):
        s = self._morph.parse(tokens[index])
        tags = [x.tag.__str__().replace(u' ', u',') for x in s]
        if len(tags) > 0:
            self._tag = tags[0]
        else:
            self._tag = None
        return self._tag
