import re
import glob
import collections
import math
import pickle



class InvdIdx:
    def __init__(self, functions= None):

        # this member supposed to be useful for trying other formal
        #self.funcs = functions
        # it nested dicts {token: [{fl_id: tk_freq },{fl_id:tk_freq},{}]}
        self.invd_indx = collections.defaultdict(lambda: collections.defaultdict(int))

        # it is not used but I mean to have it document with high frequency for fuutre
        # functions to do some calcution or filtering if possible
        self.dc_high_frq = collections.defaultdict(int)



    """
    normal str_member for print and and writing the inverted index
    """
    def __str__(self):
        res= ""

        for(k, v) in self.invd_indx.items():
            res += k +"\t ->  " +str( {x: y for (x,y) in v.items()}) +"\n"
        return res


    """
    inscribe_token:
    input: token, document_id
    postcondition :registes the token in the inverted index
    """
    def inscribe_token(self, token, dc_id):
        self.invd_indx[token][dc_id] +=1



    """
    calc_tf_idf:
        using tf(t, d, D) * idf(t,d)
        A high weight in tf–idf is reached by a high term frequency and a
        low document frequency of the term
    """
    def calc_tf_idf(self):
        for tm, tm_qnty in self.invd_idx.items():
            idf = np.log10(len(self.invd_idx) / len(tm_qnty))
            for dc_id, pre_tf  in tm_qnty.items():
                tf = pre_tf
                tfidf = tf* idf
                self.dc_nrm_tf_idf[dc_id]+=(tfidf**2)
