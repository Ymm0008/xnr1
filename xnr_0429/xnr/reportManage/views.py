#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('reportManage', __name__, url_prefix='/reportManage')

@mod.route('/management/')
def management():
    flag = request.args.get('flag','')
    return render_template('reportManage/report_manage.html',flag=flag)
