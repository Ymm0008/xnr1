#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from xnr.parameter import MAX_VALUE
from utils import show_qq_xnr, create_qq_xnr, delete_qq_xnr, change_qq_xnr,\
                  search_qq_xnr, delete_qq_group, login_status, get_login_name
from xnr.qq.qrCode import getQRCode_v2


mod = Blueprint('qq_xnr_manage', __name__, url_prefix='/qq_xnr_manage')

@mod.route('/history_speak_count/')
def ajax_history_speak_count():
    xnr_user_no = request.args.get('xnr_user_no','')

    results = get_history_speak_count(xnr_user_no)

    return json.dumps(results)

@mod.route('/get_qr_code/')
def ajax_get_qr_code():
    qq_number = request.args.get('qq_number', '')
    if qq_number:
        print 'qq_number::',qq_number
        path = getQRCode_v2(qq_number)
        print 'path..',path
        if path != None:
            if path == 'login':
                return json.dumps(path)
            new_path = '/'.join(path.split('/')[-2:])
            print 'new_path::',new_path
            return json.dumps(new_path)
        
        else:
            return json.dumps('try later')
    else:
        return False


# 点击登录
@mod.route('/click_login/')
def ajax_click_login():

    xnr_user_no = request.args.get('xnr_user_no','')
    result = get_login_name(xnr_user_no)

    return json.dumps(result)


# qq_number=1965056593&qq_groups=513304542&qq_nickname=维权律师&access_id=kwnrymiokjemiicb
#http://219.224.134.213:8098/qq_xnr_manage/add_qq_xnr/?qq_number=1039598173&group_names=嘿哼哈，房屋买卖违约维权律师&mark_names=我的群，房屋群&group_numbers=586502775，513304542&qq_nickname=石沫沫&access_id=lcnvnssnybdybffc&submitter=admin@qq.com

@mod.route('/add_qq_xnr/')
def ajax_add_qq_xnr():
    xnr_info = {}
    qq_number = request.args.get('qq_number','')
    #qq_groups = request.args.get('qq_groups','')        #所有群号中文逗号分隔
    group_names = request.args.get('group_names','')      #所有群名中文逗号分隔
    mark_names = request.args.get('mark_names','')      #所有群备注中文逗号分隔
    group_numbers = request.args.get('group_numbers','')   #所有群号中文逗号分隔
    
    nickname = request.args.get('qq_nickname','')
    submitter = request.args.get('submitter','admin@qq.com')
    remark = request.args.get('remark','')   # 备注
    access_id = request.args.get('access_id','')
    create_time = int(time.time())
    xnr_info['qq_number'] = qq_number
    #xnr_info['qq_groups'] = qq_groups
    xnr_info['group_names'] = group_names
    xnr_info['mark_names'] = mark_names
    xnr_info['group_numbers'] = group_numbers
    xnr_info['nickname'] = nickname
    xnr_info['create_ts'] = create_time
    xnr_info['access_id'] = access_id
    xnr_info['submitter'] = submitter
    xnr_info['remark'] = remark
    print 'before utils!!!!!'
    result = create_qq_xnr(xnr_info)
    return json.dumps(result)   # 结果：[True, '']、[False, '群名称数量、群备注数量和群号码数量不一致']、[False, '输入不能为空']、[False,'失败！以下备注名重复：' + ','.join(mark_name_exist_list)]

@mod.route('/delete_qq_xnr/')
def ajax_delete_qq_xnr():
    qq_number = request.args.get('qq_number','')
    results = delete_qq_xnr(qq_number)
    return json.dumps(results)


@mod.route('/show_qq_xnr/')
def ajax_show_qq_xnr():
    results = {}
    submitter = request.args.get('submitter','admin@qq.com')
    results = show_qq_xnr(MAX_VALUE,submitter)
    return json.dumps(results) 

@mod.route('/login_status/')
def ajax_login_status():
    
    xnr_user_no = request.args.get('xnr_user_no','')

    results = login_status(xnr_user_no)

    return json.dumps(results)  # True - 在线, False-离线


# # http://219.224.134.213:8098/qq_xnr_manage/add_group/?xnr_user_no=QXNR0007&group_numbers=513304542
# @mod.route('/add_group/')
# def ajax_add_group():

#     xnr_user_no = request.args.get('xnr_user_no','')
#     group_names = request.args.get('group_names','')      #所有群名中文逗号分隔
#     mark_names = request.args.get('mark_names','')      #所有群备注中文逗号分隔
#     group_numbers = request.args.get('group_numbers','')  #所有群号中文逗号分隔


#     results = add_qq_group(xnr_user_no,group_names,mark_names,group_numbers)

#     return json.dumps(results)

# http://219.224.134.213:8098/qq_xnr_manage/delete_group/?xnr_user_no=QXNR0007&group_numbers=513304542
@mod.route('/delete_group/')
def ajax_delete_group():

    xnr_user_no = request.args.get('xnr_user_no','')

    group_numbers = request.args.get('group_numbers','')   #所有群号中文逗号分隔

    results = delete_qq_group(xnr_user_no,group_numbers)

    return json.dumps(results)

# # http://219.224.134.213:8098/qq_xnr_manage/change_qq_xnr/?xnr_user_no=QXNR0007&group_names=嘿哼哈，房屋买卖违约维权律师&mark_names=我的群，房屋群&group_numbers=586502775，513304542
# @mod.route('/change_qq_xnr/')
# def ajax_change_qq_xnr():
#     xnr_user_no = request.args.get('xnr_user_no','')  # 编号
    
#     group_names = request.args.get('group_names','')      #所有群名中文逗号分隔
#     mark_names = request.args.get('mark_names','')      #所有群备注中文逗号分隔
#     group_numbers = request.args.get('group_numbers','') #所有群号中文逗号分隔
#     #xnr_info = [qq_number,qq_groups]
#     results = change_qq_xnr(xnr_user_no,group_names,mark_names,group_numbers)

#     return json.dumps(results)    # 三种结果：not_equal- 群名和群号数量不等, True - 成功, False - 失败

@mod.route('/search_qq_xnr/')
def ajax_search_qq_xnr():
    qq_number = request.args.get('qq_number','')
    results = search_qq_xnr(qq_number)
    return json.dumps(results)

# @mod.route('//')
