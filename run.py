import os
import time

from extractor.perfectextractor import PerfectExtractor


def process_data_folders(extractors, path):
    for extractor in extractors:
        for directory in os.listdir(path):
            d = os.path.join(path, directory)
            if os.path.isdir(d):
                t0 = time.time()
                print 'Now processing {} for {}'.format(d, extractor.l_from)
                extractor.process_folder(d)
                print 'Processing finished, took {:.3} seconds'.format(time.time() - t0)


def create_extractors():
    en_extractor = PerfectExtractor('en', ['fr', 'nl'])
    nl_extractor = PerfectExtractor('nl', ['en', 'fr'])
    fr_extractor = PerfectExtractor('fr', ['en', 'nl'])
    return [en_extractor, nl_extractor, fr_extractor]

if __name__ == "__main__":
    process_data_folders(create_extractors(), 'data')