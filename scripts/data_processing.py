# script for data processing pipeline

from BZ2Reader import bz2reader
from glob import glob
import os
from pprint import pprint

# get list of b22 file in data folder
DATA_FOLDER = 'data'
bz2files = glob(os.path.join(DATA_FOLDER,'*.bz2'))

# for all bz2 files get a subset of attributes

def data_processing(bz2files, max_lines=-1):
    for bz2file in  bz2files:
        bzr = bz2reader(fname=bz2file,
                        keys=['body'], 
                        max_lines=max_lines)
        # bzr = bz2reader(fname=bz2file,
        #                 keys=['subreddit','id', 'author','body','created_utc'], 
        #                 max_lines=max_lines)

        # pprint(bzr.build_structure())
        for data in bzr.select_keys():
            print(data)
        # insert rest of pipeline here
        return 

def test():
    data_processing(bz2files, 100)

if __name__=="__main__":
    test()