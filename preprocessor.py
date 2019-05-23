
#######################################################
# author : ahmed alhaj
# email : alhaj1@umbc.edu
# phase2: caculate the frequency of token with respect to fileself
# class : cmsc476Block
#######################################################






import re
import glob
import collections
import math
import pickle
import html2text
from structures import InvdIdx
import time




"""
WordParse : works as tokenize for for each document
takes list of common_word that need to disgarded
filter on single letter either captial or small
normalize the toke to lower_case
"""
class WordParser:
    def __init__(self, common_words_path):
        with open('./{}'.format("stop_list.txt"),'r') as f:
            self.common_words = set(f.read().split('\n'))
        #print(self.common_words)

    def filter_common_words(self, token):
        return token not in self.common_words

    def Parse(self, token_stream):
        reg = re.compile(r"[a-zA-Z]+")
        for token in reg.findall(token_stream):
            lower_token = token.lower()
            if self.filter_common_words(lower_token):
                yield lower_token

"""
FilePiper: read the document and converted to HTML_FILE structure the name might very confusing
HTML_FILE relates more a parsed html file than an actuak html fileself.
takes the path of corpus and read them
"""
class FilesPiper:
    def __init__(self, path):
        self.hndlr =html2text.HTML2Text()
        self.path = path

    def get_files(self):

        i = 0
        dc_set = set()

        print(self.path)
        for fl_name in glob.glob(self.path +'/*'):

            with open(fl_name, encoding ='utf-8', errors='ignore') as file:
                doc = file.read()
                doc = HtmlFile(doc, i)
                dc_set.add(doc)
                i +=1
        return dc_set


"""
HtmlFile:  I meant to say HTML_FILE_PROCESSOR but it was too long.
define the attribute of the file
has a Pasre to parse token
it is pretty useful strucure for large scale documment processsing it is easy to build on top of it
postcondition: parse the token generate
"""
class HtmlFile:
    def __init__(self, content, id):
        self.id =id
        self.content = content
        self.content_field= ["content"]
    def tokenize(self, parser, inverted_index=None):
        for tkf in self.content_field:
            setattr(self, tkf + '_words', [word for word in parser.Parse(getattr(self,tkf))])
            for tk in getattr(self, tkf + '_words'):
                inverted_index.inscribe_token(tk, self.id)
    def to_string(self):
        return self.content[:500]

"""
this is the main method where everything is running

"""

def preprocessor(path=None, path1=None, common_words_path=None):
    #stop_word = []
    #path = r'''C:\Users\alhaj1\Documents\cmsc476\files'''
    if (path == None):

        path = r'''C:\Users\alhaj1\Documents\cmsc476\files'''
        path1 =  r'''C:\Users\alhaj1\Documents\cmsc476\proj2\out_file'''
        common_words_path = r'''C:\Users\alhaj1\Documents\cmsc476\proj2\stop_list.txt'''



    inverted_index_arr = []
    retrieval_list = []

    parser = WordParser(common_words_path)
    files_piper = FilesPiper(path)


    inv_idx = InvdIdx()
    inverted_index_arr.append(inv_idx)
    doc_retrieve_dicts = {}


    i = 0

    for htfl in files_piper.get_files():

        htfl.tokenize(parser, inv_idx)
        #doc_retrieve_dicts[htfl.id] = htfl.to_string() // just for testing and future goal
        i += 1

    out_file = open(path1+"output.txt", "w", errors='ignore')
    out_file.write("token \t -> {dcoumnet_id, token_freq}")
    out_file.write(str(inv_idx))
    out_file.close()

    return




"""
main:
takes the path from the users
pass the path and proprocessor
"""
# quick make sure the time does not count the wrtiting the files
def main():

    path1 = None ; path2 = None ; path3 = None
    input_list = []
    for i in range(3):
        if i == 0:
            input_list.append(input("please enter the in_file path"))
        elif i == 1:
            input_list.append(input("please enter the out_file path"))
        elif i == 2:
            input_list.append(input("please enter the common_word path"))

    if(len(input_list[0]) > 1):
        path1 , path2 , path3 = input_list[0], input_list[1], input_list[2]
    start = time.time()
    preprocessor(path1, path2, path3)
    end = time.time()
    print(end- start)

main()
