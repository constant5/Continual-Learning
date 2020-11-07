# Module for opening reddit bz2 files

import json
import bz2 

class bz2reader():

    def __init__(self, fname, keys=[], max_lines=-1):
        self.fname = fname
        self.file_object = bz2.open(self.fname, 'rb')
        self.max_lines = max_lines
        self.keys = keys

    def read_lines(self):
        ''' reads bz2 file line by line and yields dicts'''
        i = 0
        while True:
            data = self.file_object.readline()
            if not data or i == self.max_lines:
                self.file_object.close()
                break
            i += 1
            yield json.loads(data.decode())
    
    def select_keys(self, keys=None):
        # yields dictionaries with selected key
        if keys:
            self.keys = keys
        ''' yield lines with only specified keys'''
        for data in self.read_lines():
            processed = {}
            for k in self.keys:
                if k.find('utc')>-1:
                    processed[k] = int(data[k])
                else:
                    processed[k] = data[k]
            yield processed

    def build_structure(self):
        # build a dictionary with subreddits as keys and body text as values
        data = {}
        for p in self.select_keys():
            if p['body'] != 'deleted' and len(p['body'].split(' ')) >= 4:
                try:
                    # data[p['subreddit']] = data[p['subreddit']].append([{k:p[k] for k in self.keys() if k!='subreddit'}])
                    if len(self.keys) == 2:
                        data[p['subreddit']].append(p['body'])
                    else:
                        data[p['subreddit']].append({k:p[k] for k in self.keys  if k!='subreddit'})
                    # print('appending')
                except:
                    # print('creating new')
                    if len(self.keys) ==2:
                        data[p['subreddit']] = [p['body']]
                    else:
                        data[p['subreddit']] = [{k:p[k] for k in self.keys  if k!='subreddit'}]
        return data


    
    def __del__(self):
        if self.file_object:
            self.file_object.close()


if __name__=='__main__':
    print('loaded module')
    




