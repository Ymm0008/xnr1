# -*-coding:utf-8-*-
import sys
import json
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_xnr as es
from global_utils import group_message_index_name_pre, group_message_index_type

from global_config import QQ_S_DATE
from time_utils import ts2datetime, datetime2ts
from parameter import DAY

def group_message_mappings(qq_number, date):
    index_name = group_message_index_name_pre + str(date)
    index_info = {
        'settings':{
            'number_of_replicas':0,
            'number_of_shards':5
        },
        'mappings':{
            group_message_index_type:{
                'properties':{
                    'qq_uin_number':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'qq_group_number':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'qq_group_nickname':{
                         'type':'string',
                         'index':'not_analyzed'
                    },
                    'text':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'speaker_qq_number':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'speaker_nickname':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'timestamp':{
                        'type':'long'
                        
                    },
                    'xnr_qq_number':{
                        'type':'string',
                        'index': 'not_analyzed'
                    },
                    'xnr_nickname':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_value':{
                        'type':'long'
                        
                    },
                    'sensitive_words_string':{
                        'type':'string',
                        'index':'not_analyzed'
                    },
                    'sensitive_flag':{
                        'type':'long'
                        
                    }
                }

            }
        },
    }
    print 'index_name', index_name
    if not es.indices.exists(index=index_name):
        print es.indices.create(index=index_name,body=index_info,ignore=400)
        
    #else:
    #    es.indices.delete(index=index_name, timeout=100)
    #    es.indices.create(index=index_name,body=index_info,ignore=400) 

if __name__ == '__main__':
    qq_number = 123456
    #date = '2018-03-07'
    # date = QQ_S_DATE
    current_time=int(time.time()+DAY)
    date = ts2datetime(current_time)
    group_message_mappings(qq_number, date)
    
    '''
    current_time=int(time.time())
    start_time = datetime2ts('2018-05-01')
    
    num_day = (current_time-start_time)/(24*3600)
    for i in range(num_day):
        timestamp = start_time + i*24*3600
        date = ts2datetime(timestamp)
        group_message_mappings(qq_number, date)
    '''
