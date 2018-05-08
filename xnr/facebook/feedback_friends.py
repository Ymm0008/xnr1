#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from Elasticsearch_fb import Es_fb
import re
import json

class Friend():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		time.sleep(2)
		# 退出通知弹窗进入页面
		try:
			self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
		except:
			pass
		# # 进入个人主页
		# self.driver.find_element_by_xpath('//a[@title="个人主页"]').click()
		# time.sleep(3)
		# # 退出通知弹窗进入页面
		# try:
		# 	self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
		# except:
		# 	pass
		# # 点击好友列表
		# self.driver.find_element_by_xpath('//ul[@data-referrer="timeline_light_nav_top"]/li[3]/a').click()
		# time.sleep(3)

		# 进入好友请求页面
		self.driver.get('https://www.facebook.com/friends/requests')
		time.sleep(3)
		# 退出通知弹窗进入页面
		try:
			self.driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
		except:
			pass

		#加载更多
		length=100
		for i in range(0,20):
			js="var q=document.documentElement.scrollTop="+str(length) 
			self.driver.execute_script(js) 
			time.sleep(1)
			length+=400

		self.es = Es_fb()
		self.list = []
		self.current_ts = int(time.time())
		self.update_time = self.current_ts

	def get_friend(self):
		try:
			# for each in self.driver.find_elements_by_xpath('//div[@class="_5h60 _30f"]//ul//li'):
			# 	try:
			# 		pic_url = each.find_element_by_xpath('./div/a/img').get_attribute('src')
			# 		name = each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').text
			# 		user_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').get_attribute('data-hovercard')))
			# 		friends = each.find_element_by_xpath('./div/div/div[2]/div/div[2]/a').text
			# 		profile_url = each.find_element_by_xpath('./div/div/div[2]/div/div[2]/div/a').get_attribute('href') + '&sk=about'
			# 	except:
			# 		pass
			for each in self.driver.find_elements_by_xpath('//div[@id="globalContainer"]/div/div/div/div/div[3]/div'):
				try:
					pic_url = each.find_element_by_xpath('./a/div/img').get_attribute('src')
					name = each.find_element_by_xpath('./div/div[2]/div[1]/a').text
					user_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div[2]/div[1]/a').get_attribute('data-hovercard')))
					friends = None
					profile_url = each.find_element_by_xpath('./div/div[2]/div[1]/a').get_attribute('href')
					self.list.append({'uid':user_id, 'photo_url':pic_url, 'nick_name':name, 'friends':friends, 'profile_url':profile_url, 'update_time':self.update_time})
				except Exception as e:
					print(e)
		finally:
			self.driver.quit()
		return self.list

	def save(self, indexName, typeName, list):
		self.es.executeES(indexName, typeName, list)

if __name__ == '__main__':
	friend = Friend('8618348831412','Z1290605918')
	list = friend.get_friend()
	print(list)
	#friend.save('facebook_feedback_friends','text',list)

