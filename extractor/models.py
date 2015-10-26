MARKUP = u'**{}**'


class Word:
    """
    Each Word consists of a word, its lemma, and a designation if this is a verb.
    """
    def __init__(self, word, lemma, is_verb):
        self.word = word
        self.lemma = lemma
        self.is_verb = is_verb


class PresentPerfect:
    """
    A present perfect consists of a list of Words.
    """

    def __init__(self, aux_verb, aux_lemma):
        """
        A present perfect is initiated by an auxiliary verb.
        """
        self.words = []
        self.add_word(aux_verb, aux_lemma, True)

    def add_word(self, word, lemma, is_verb):
        """
        Adds a word to the present perfect.
        """
        self.words.append(Word(word, lemma, is_verb))

    def extend(self, present_perfect):
        """
        Extends a present perfect with another one (used to create a present perfect continuous).
        """
        for i, w in enumerate(present_perfect.words):
            if i == 0:
                continue
            self.add_word(w.word, w.lemma, w.is_verb)

    def perfect_lemma(self):
        """
        Returns the lemma of the perfect: the lemma of the last word of the construction.
        """
        return self.words[-1].lemma

    def verbs(self):
        """
        Extracts the verbs from the present perfect.
        """
        return [w.word for w in self.words if w.is_verb]

    def verbs_to_string(self):
        """
        Returns the verbs from the present perfect as a string.
        """
        return ' '.join(self.verbs())

    def words_between(self):
        """
        Returns the number of non-verbs in a present perfect construction.
        """
        return len([w.word for w in self.words if not w.is_verb])

    def mark_sentence(self, sentence):
        """
        Marks the present perfect in a full sentence.
        """
        # TODO: this is a bit iffy, another idea could be to compose the sentence from the remaining siblings
        # To find the pp in the full text, simply join all the parts of the pp
        pp_text = ' '.join([w.word for w in self.words])

        # For the replacement, mark the verbs with the MARKUP
        if len(self.words) == len(self.verbs()):
            marked_pp = MARKUP.format(pp_text)
        else:
            marked_pp = ' '.join([MARKUP.format(w.word) if w.is_verb else w.word for w in self.words])

        return sentence.replace(pp_text, marked_pp)