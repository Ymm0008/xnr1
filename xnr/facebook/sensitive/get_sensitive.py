# -*-coding:utf-8-*-

import json
import time
import os

import sys
reload(sys)
sys.path.append('../../')
from global_utils import facebook_flow_text_index_name_pre,facebook_flow_text_index_type,es_xnr
from time_utils import ts2datetime
from parameter import sensitive_score_dict
from global_utils import R_ADMIN as r_sensitive


def get_sensitive_info(timestamp,mid):
    index_name = facebook_flow_text_index_name_pre + ts2datetime(timestamp)
    try:
        item_result = es_xnr.get(index=index_name,doc_type=facebook_flow_text_index_type,id=mid)['_source']
        sensitive_info = item_result['sensitive']
    except:
        sensitive_info = 0

    return sensitive_info

def get_sensitive_user(uid):
    sensitive_score = 0
    try:
        tmp_stage = r_sensitive.hget('sensitive_words', uid)
        if tmp_stage:
            sensitive_score += v * sensitive_score_dict[str(tmp_stage)]
    except Exception,e:
        print e
        

    return sensitive_score
    
if __name__ == '__main__':
    print get_sensitive_user(uid='100023545574584')

        # for k,v in  r_sensitive.hgetall('sensitive_words').items():
        #     print k ,v
        # print r_sensitive.keys()
        # print tmp_stage