# -*- coding:utf-8 -*-
import sys
import json
sys.path.append('../../')
from global_utils import es_xnr as es, tw_xnr_flow_text_index_name_pre, \
                tw_xnr_flow_text_index_type


def tw_xnr_flow_text_mappings(index_name):
    index_info = {
            'settings':{
                'analysis':{
                    'analyzer':{
                        'my_analyzer':{
                            'type': 'pattern',
                            'pattern': '&'
                        }
                    }
                }
            },
            'mappings':{
                'text':{
                    'properties':{
                        'task_source':{  # 日常发帖，热点跟随，业务发帖
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'xnr_user_no':{
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'uid':{
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'text':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'picture_url':{
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'vedio_url':{
                            'type':'string',
                            'index':'not_analyzed'
                        },
                        'user_fansnum':{
                            'type':'long'
                        },
                        'user_followersum':{
                            'type':'long'
                        },
                        'weibos_sum':{
                            'type':'long'
                        },
                        'tid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'ip':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'directed_uid':{
                            'type':'long',
                            },
                        'directed_uname':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'timestamp':{
                            'type': 'long'
                            },
                        'sentiment': {
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'geo':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'keywords_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'keywords_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'sensitive_words_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'sensitive_words_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'message_type':{
                            'type': 'long'
                            },
                        'root_uid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'root_tid':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                         # uncut weibo text
                        'origin_text':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'origin_keywords_dict':{
                            'type': 'string',
                            'index': 'not_analyzed'
                            },
                        'origin_keywords_string':{
                            'type': 'string',
                            'analyzer': 'my_analyzer'
                            },
                        'comment':{
                            'type':'long'
                            },
                        'sensitive':{
                            'type':'long'
                            },
                        'retweeted':{
                            'type':'long'
                            }
                        }
                    }
                }
            }
    exist_indice = es.indices.exists(index=index_name)
    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)

def tw_daily_inerests_flow_text_mappings(index_name):

    index_info = {
        'settings':{
            'number_of_replicas':0,
            'bumber_of_shards':5
        },
        'mappings':{
            'text':{
                'properties':{
                    'timestamp':{
                        'type':'long'
                    },
                    'content':{
                        'type':'string',
                        'index':'no'
                    }
                }
            }
        }
    }

    exist_indice = es.indices.exists(index=index_name)

    if not exist_indice:
        es.indices.create(index=index_name, body=index_info, ignore=400)

if __name__ == '__main__':

    tw_xnr_flow_text_mappings(index_name)