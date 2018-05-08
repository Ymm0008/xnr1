# -*-coding:utf-8-*-

import os
import sys
import time
import json

sys.path.append('../../')
from global_utils import es_xnr, es_intel, writing_task_index_name, writing_task_index_type, \
                        intel_opinion_results_index_name, intel_models_text_index_name, \
                        intel_models_text_index_type, opinion_corpus_index_name, \
                        opinion_corpus_index_type, opinion_corpus_results_index_name,\
                        opinion_corpus_results_index_type

def save2topic_es(task_source,task_id,search_results):


    bulk_action = []
    count = 0
    for tweet in search_results:

        action = {'index':{'_id':tweet['_id']}}
        source = tweet['_source']

        bulk_action.extend([action,source])

        count += 1

        if count % 1000 == 0:
            es_intel.bulk(bulk_action,index=task_id,doc_type=task_source,timeout=600)
    
    if bulk_action:
        es_intel.bulk(bulk_action,index=task_id,doc_type=task_source,timeout=600)
    

def save_intelligent_opinion_results(task_id,sub_opinion_results,summary, intel_type):

    try:
        item_exist = dict()
        item_exist['task_id'] = task_id
        item_exist['subopinion_tweets'] = json.dumps(sub_opinion_results)
        item_exist['summary'] = summary
        # 保存子观点结果
        es_intel.index(index=intel_opinion_results_index_name,doc_type=intel_type,\
                id=task_id,body=item_exist)

        item_task = dict() 
        item_task['compute_status'] = 2  ## 保存子观点结果，更新计算状态
        es_xnr.update(index=writing_task_index_name,doc_type=writing_task_index_type,\
             id=task_id, body={'doc':{'compute_status':2}})

        mark = True

    except:
        mark = False

    return mark

def save2models_text(task_id,model_text_dict):

    item_exist = dict()
    item_exist['task_id'] = task_id
    item_exist['model_text_pos'] = model_text_dict['model_text_pos']
    item_exist['model_text_neg'] = model_text_dict['model_text_neg']
    item_exist['model_text_news'] = model_text_dict['model_text_news']

    # 保存智能发帖模板文本结果
    print 'item_exist...',item_exist
    
    es_intel.index(index=intel_models_text_index_name,doc_type=intel_models_text_index_type,\
                id=task_id,body=item_exist)

    item_task = dict() 
    item_task['compute_status'] = 4  ## 保存智能发帖模板文本结果，更新计算状态，计算完成
    es_xnr.update(index=writing_task_index_name,doc_type=writing_task_index_type,\
            id=task_id, body={'doc':{'compute_status':4}})


def save2opinion_corpus(task_id,opinion_results):

    item_exist = dict()
    item_exist['task_id'] = task_id
    item_exist['corpus_results'] = json.dumps(opinion_results)

    es_intel.index(index=opinion_corpus_results_index_name,doc_type=opinion_corpus_results_index_type,\
                id=task_id,body=item_exist)


    item_task = dict() 
    item_task['compute_status'] = 3  ## 保存观点语料结果，更新计算状态
    es_xnr.update(index=writing_task_index_name,doc_type=writing_task_index_type,\
            id=task_id, body={'doc':item_task})

