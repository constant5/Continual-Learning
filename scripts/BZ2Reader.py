# Module for opening reddit bz2 files

import json
import bz2
import os

class BZ2Reader():
    """The BZ2Reader aids in efficient processing of bz2 files containing a key:attribute structure """

    def __init__(self, fname, keys=[], max_lines=-1):
        """reader object

        Args:
            fname (str): path of file to process
            max_lines (int, optional): maximum number of lines to process
            keys (:obj:'list` of :obj:`str`): specific attributes to return
        """

        self.fname = fname
        self.file_object = bz2.open(self.fname, 'rb')
        self.max_lines = max_lines
        self.keys = keys

    def read_lines(self):
        ''' reads bz2 file line by line and yields dicts
        
        Yields:
            dict: individual posts
        '''
        i = 0
        while True:
            data = self.file_object.readline()
            if not data or i == self.max_lines:
                self.file_object.close()
                break
            i += 1
            yield json.loads(data.decode())
    
    def select_keys(self, keys=None):
        ''' yields dictionaries with selected key

        Args:
            keys (:obj:`list` of :obj:`str`): specific attributes to return

        Yields:
            dict: post with selected keys
        '''

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
        ''' build a dictionary with subreddits as keys and body text as values


        Returns:
            dict: all posts as lists with subreddits as keys
        '''

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

    def file_writer(self, dest = "data", p_min=1000, batch_save=1000):
        ''' Takes the file and splits it into individual text files for each subreddit. 

        Args:
            dest (str): dest folder to hold text files 
                (note a "subreddit" folder will be created here).
            p_min (int): the minimum number of posts required to start saving posts
            batch_save (int): how often to write files (after p_min satisfied)
        '''

        # make dir to hold txt files
        if not os.path.exists(os.path.join(dest, 'subreddits','')):
            os.mkdir(os.path.join(dest, 'subreddits'))
        
        # create temporary data structure to batch save data
        data = {}
        for post in self.select_keys():
            if post['body'] != 'deleted' and len(post['body'].split(' ')) >= 4:
                try:
                    # data[p['subreddit']] = data[p['subreddit']].append([{k:p[k] for k in self.keys() if k!='subreddit'}])
                    if len(self.keys) == 2:
                        data[post['subreddit']].append(post['body'])
                    else:
                        data[post['subreddit']].append({k:post[k] for k in self.keys  if k!='subreddit'})
                    # print('appending')
                except:
                    # print('creating new')
                    if len(self.keys) ==2:
                        data[post['subreddit']] = [post['body']]
                    else:
                        data[post['subreddit']] = [{k:post[k] for k in self.keys  if k!='subreddit'}]
            
                
                data_path = os.path.join(dest,'subreddits',  post['subreddit']+'.txt')
                
                # for data that is being saved save batch
                if os.path.exists(data_path) and len(data[post['subreddit']]) >= batch_save:
                    with open(data_path, 'a', encoding='utf-8') as f:
                            f.writelines([l.replace('\n',' ') + '\n' for l in data[post['subreddit']]])
                    data[post['subreddit']] = []

                 # if data structure has more the p_min post for a given subreddit then create file
                if len(data[post['subreddit']]) >= p_min:
                    print(f'Initializing file for {post["subreddit"]}')
                    with open(data_path, 'w', encoding='utf-8') as f:
                        f.writelines([l.replace('\n',' ') + '\n' for l in data[post['subreddit']]])
                    # reset the data structure list for processed batch
                    data[post['subreddit']] = []

    
    def __del__(self):
        ''' Special object destruction method to make sure file is closed'''
        if self.file_object:
            self.file_object.close()


if __name__=='__main__':
    print('loaded module')
    




