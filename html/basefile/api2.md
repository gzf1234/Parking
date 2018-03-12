#########################################
查询日期都以20180102或者2018-01-02这种字符串形式
/api/login
post
username, pwd
{'status':num, 'token':token} -> num=0:name_error, num=1:pwd_error, num=2:ok

/api/add_info (录入)
post
CarId, FlightNumber, FlyTime, ArriveTime, ParkDate, Phone, ParkPlace, BackPersons, BoxNum
{'status':str(num)} -> num=0:token有问题, num=1:失败, num=2:ok

/api/query_info
post
QueryDate (2018-02-03/20180203)
{   
	'status':num,
	'infos':[
	{'CarId':str, 'ArriveTime':str, 'ParkPlace':str, 'Fee':int, 'BackPersons':int, 'BoxNum':int},
	{..},
	{..},
	.
	.
	.
	]
} -> num=0:token有问题, num=1:查询失败, num=2:ok

/api/count_info
post
QueryDate(20180102/2018-01-02)
{
	'status':num,
	'infos':[
	{'CarId':str, 'ParkPlace':str, 'Fee':int,  'BackPersons':int, 'BoxNum':int}
	{..},
	{..}
	]
} -> num=0:token有问题, num=1:失败, num=2:ok

/api/user_leave
post
CarId
{'status':num} -> num=0:token有问题, num=1:失败, num=2:ok

#/api/rollback_user （暂时没写）
#post
#CarId
#{'status':num, info:{'CarId':str, 'ArriveTime':str, 'ParkPlace':str, 'Fee':int, 'BackPersons':int, 'BoxNum':int}} -> num=0:failure, num=1:success
# -> num=0:token有问题, num=1:失败, num=2:ok

/api/change_pwd
post
old_pwd, new_pwd
{'status':num} -> num=0:token有问题, num=1:旧密码不正确, num=2:ok

