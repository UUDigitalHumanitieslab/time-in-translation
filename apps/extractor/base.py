from abc import ABCMeta, abstractmethod
import codecs
import os

from .utils import UnicodeWriter

LEMMATA_CONFIG = os.path.join(os.path.dirname(__file__), 'config/{language}_lemmata.txt')


class BaseExtractor(object):
    __metaclass__ = ABCMeta

    def __init__(self, language_from, languages_to):
        """
        Initializes the extractor for the given source and target language(s).
        :param language_from: the source language
        :param languages_to: the target language(s)
        """
        self.l_from = language_from
        self.l_to = languages_to

    def process_folder(self, dir_name):
        """
        Creates a result file and processes each file in a folder.
        """
        result_file = '-'.join([dir_name, self.l_from]) + '.csv'
        with open(result_file, 'wb') as f:
            f.write(u'\uFEFF'.encode('utf-8'))  # the UTF-8 BOM to hint Excel we are using that...
            csv_writer = UnicodeWriter(f, delimiter=';')

            header = ['document', self.l_from, 'xml']
            for language in self.l_to:
                header.extend([language, 'xml'])
            csv_writer.writerow(header)

            for filename in self.list_filenames(dir_name):
                results = self.process_file(filename)
                csv_writer.writerows(results)

    def read_lemmata(self, lemmata):
        self.lemmata_list = []
        if lemmata is not None:
            if type(lemmata) == list:
                self.lemmata_list = lemmata
            elif type(lemmata) == bool:
                if lemmata:
                    with codecs.open(LEMMATA_CONFIG.format(language=self.l_from), 'rb', 'utf-8') as lexicon:
                        self.lemmata_list = lexicon.read().split()
            else:
                raise ValueError('Unknown value for lemmata')

    @abstractmethod
    def get_config(self):
        """
        Returns the location of the configuration file.
        """
        raise NotImplementedError

    @abstractmethod
    def process_file(self, filename):
        """
        Process a single file
        """
        raise NotImplementedError

    @abstractmethod
    def list_filenames(self, dir_name):
        """
        List all to be processed files in the given directory.
        """
        raise NotImplementedError

    @abstractmethod
    def get_translated_lines(self, alignment_trees, language_from, language_to, segment_number):
        """
        Returns the translated segment numbers (could be multiple) for a segment number in the original text.
        """
        raise NotImplementedError

    @abstractmethod
    def get_sentence(self, element):
        """
        Returns the full sentence XML for the given element.
        """
        raise NotImplementedError

    @abstractmethod
    def get_siblings(self, element, sentence_id, check_preceding):
        """
        Returns the siblings of the given element in the given sentence_id.
        The check_preceding parameter allows to look either forwards or backwards.
        """
        raise NotImplementedError