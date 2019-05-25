from django.test import TestCase

# Create your tests here.
from models import Account
import time
import random


a1=(1920,1,1,0,0,0,0,0,0)              #设置开始日期时间元组（1976-01-01 00：00：00）
a2=(2019,12,31,23,59,59,0,0,0)    #设置结束日期时间元组（1990-12-31 23：59：59）
phone_list = [3,4,5,6,7,8]
start=time.mktime(a1)    #生成开始时间戳
end=time.mktime(a2)      #生成结束时间戳
for i in range(30):
    t=random.randint(start,end)    #在开始和结束时间戳中随机取出一个
    date_touple=time.localtime(t)          #将时间戳生成时间元组
    date=time.strftime("%Y-%m-%d",date_touple)  #将时间元组转成格式化字符串（1976-05-21）
    phone = '1' + str(random.choice(phone_list)) + str(random.randint(100000000, 999999999))
    new_user = Account()
    new_user.AName = 'NewUser' + str(i)
    new_user.password = hash_code('qq656245')
    new_user.sex = 'male'
    new_user.last_name = 'Zhang'
    new_user.first_name = 'Song'
    new_user.birth = data
    new_user.email = 'NewUser' + str(i) + '@163.com'
    new_user.personal_ID = '32048319980129' + str(random.randint(1000, 9999))
    new_user.phone = '1' + str(random.randint(phone_list)) + str(100000000, 999999999)
    new_user.account_type = 'restaurant'
    new_user.save()


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()