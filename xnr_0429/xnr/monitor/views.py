#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
				  abort, flash, session, redirect



mod = Blueprint('monitor', __name__, url_prefix='/monitor')

@mod.route('/characterBehavior/')
def characterBehavior():
	return render_template('monitor/character_behavior.html')

@mod.route('/speechContent/')
def speechContent():
	return render_template('monitor/speech_content.html')

@mod.route('/eventEmerges/')
def eventEmerges():
	return render_template('monitor/event_emerges.html')

@mod.route('/timeWarning/')
def timeWarning():
	return render_template('monitor/time_warning.html')

# 社区预警
@mod.route('/communityWarning/')
def communityWarning():
	return render_template('monitor/community_warning.html')

# 社区详情
@mod.route('/communityDetails/')
def communityDetails():
	communityID = request.args.get('communityID','')
	communityName = request.args.get('communityName','')
	communityTime = request.args.get('communityTime','')
	communityPeople = request.args.get('communityPeople','')
	flag = request.args.get('flag','')
	return render_template('monitor/community_details.html',communityID=communityID,communityName=communityName,
		communityTime=communityTime,communityPeople=communityPeople,flag=flag)

# 预警详情
@mod.route('/communityWaringdetails/')
def communityWaringdetails():
	comId = request.args.get('comId','')
	oldNew = request.args.get('oldNew','')
	flag = request.args.get('flag','')
	return render_template('monitor/communityWaring_details.html',comId=comId,oldNew=oldNew,flag=flag)

@mod.route('/characterBehaviorTwitter/')
def characterBehaviorTwitter():
	return render_template('monitor/character_behaviorTwitter.html')

@mod.route('/speechContentTwitter/')
def speechContentTwitter():
	return render_template('monitor/speech_contentTwitter.html')

@mod.route('/eventEmergesTwitter/')
def eventEmergesTwitter():
	return render_template('monitor/event_emergesTwitter.html')

@mod.route('/timeWarningTwitter/')
def timeWarningTwitter():
	return render_template('monitor/time_warningTwitter.html')

@mod.route('/characterBehaviorFaceBook/')
def characterBehaviorFaceBook():
	return render_template('monitor/character_behaviorFaceBook.html')

@mod.route('/speechContentFaceBook/')
def speechContentFaceBook():
	return render_template('monitor/speech_contentFaceBook.html')

@mod.route('/eventEmergesFaceBook/')
def eventEmergesFaceBook():
	return render_template('monitor/event_emergesFaceBook.html')

@mod.route('/timeWarningFaceBook/')
def timeWarningFaceBook():
	return render_template('monitor/time_warningFaceBook.html')