import re
import default.const as c

from Lexicon import Lexicon


class LexiconLVL(Lexicon):
    def __init__(self, processor_name='lexicon', target_nodes="//token", \
                 target_attribute='text', part_of_speech_attribute='pos', child_node_type='segment',
                 output_attribute='pronunciation', \
                 class_attribute='token_class', word_classes=['word'],
                 probable_pause_classes=['punctuation', c.TERMINAL], \
                 possible_pause_classes=['space'], \
                 dictionary='some_dictionary_name', backoff_pronunciation='axr', lts_variants=1, \
                 lts_ntrain=0, lts_gram_length=3, max_graphone_letters=2, max_graphone_phones=2):

        super(LexiconLVL, self).__init__(processor_name, target_nodes, target_attribute, part_of_speech_attribute,
                                         child_node_type, output_attribute, class_attribute, word_classes, probable_pause_classes,
                                         possible_pause_classes, dictionary, backoff_pronunciation, lts_variants,
                                         lts_ntrain, lts_gram_length, max_graphone_letters, max_graphone_phones)

    def syllabify(self, phonestring):
        '''
        Syllabify with maximum legal (=observed) onset.
        Take "e g z a1 m"
        return "e g | z a1 m"
        '''
        assert '|' not in phonestring
        plain = re.sub('\d', '', phonestring)  ## remove stress marks so we can look up vowels
        plainphones = plain.split(' ')
        phones = phonestring.split(' ')
        vowel_indexes = [i for (i, phone) in enumerate(plainphones) \
                         if self.phoneset.lookup(phone, field='vowel_cons') == 'vowel']

        if len(vowel_indexes) > 0:  ## else add nothing to phones and return that.

            start = vowel_indexes[0] + 1

            for end in vowel_indexes[1:]:

                if start == end:  ## juncture between 2 vowels as in 'buyer'
                    best_split = start
                else:
                    split_scores = []
                    for split in range(start, end):
                        first_part = tuple(plainphones[start:split])
                        second_part = tuple(plainphones[split:end])

                        ## Take maximum legal onset:
                        if second_part in self.onsets:
                            score = len(second_part)
                        else:
                            score = -1

                        ## Older version: score is sum of onset and coda freqs:
                        # score = self.codas.get(first_part, 0) + self.onsets.get(second_part, 0)

                        split_scores.append((score, split))
                    split_scores.sort()

                    best_split = split_scores[-1][1]
                phones[best_split] = '| ' + phones[best_split]

                start = end + 1

        return ' '.join(phones)
