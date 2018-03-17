# -*- coding: utf8 -*-
#user:gzf

from flask import request, jsonify
from datetime import datetime
import redis
import re

from myapp.api import api
from myapp.models import User, OldUser, Parker
from myapp.models import db
from settings import DAY_FEE, TRAVEL_FEE
from myapp.utils import get_fee
from logger import logger

conn = redis.Redis(host='127.0.0.1', port=6379, db=1)
@api.route('/login.php', methods=['POST'])
def login():
    username = request.form.get('username')
    parker = Parker.query.filter_by(account=username).first()
    # check account
    if parker:
        password = request.form.get('pwd')
        # check pwd
        if parker.varify_password(password):
            token = parker.token
            return jsonify({'status':'2', 'token':token})
        return jsonify({'status':'1'})
    return jsonify({'status':'0'})


# add user.infos to table(user)
@api.route('/index.php', methods=['POST'])
def add_info():
    # token = request.form.get('token')
    # parker = Parker.query.filter_by(token=token)
    # if parker:
    if True:
        CarId = request.form.get('CarId')
        FlightNumber = request.form.get('FlightNumber')
        FlightNumber = FlightNumber.upper() # 确保航班号英文字母都是大写
        FlyDate = request.form.get('FlyTime')
        # ArriveTime = request.form.get('BackDate')
        ParkDate = request.form.get('ParkDate')
        Phone = request.form.get('Phone')
        ParkPlace = request.form.get('ParkPlace')
        BackPersons = request.form.get('BackPersons')
        BoxNum = request.form.get('BoxNum')
        FlyDate = '-'.join(re.findall(r'\d+', FlyDate))
        ParkDate = '-'.join(re.findall(r'\d+', ParkDate))
        user = User(
            CarId = CarId,
            FlightNum = FlightNumber,
            FlyDate = FlyDate,
            # ArriveTime = ArriveTime,
            ParkDate = ParkDate,
            Phone = Phone,
            ParkPlace = ParkPlace,
            BackPersons = BackPersons,
            BoxNum = BoxNum,
        )
        # print(user)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return jsonify({'status':'1'})
        conn.hmset(CarId, {'CarId':CarId, 'FlightNum':FlightNumber, 'FlyDate':FlyDate})
        return jsonify({'status':'2'})
    # token error
    return jsonify({'status':'0'})


# query user_infos by date
@api.route('/query_info.php', methods=['POST'])
def query_info():
    # token = request.form.get('token')
    # parker = Parker.query.filter_by(token=token).first()
    # if parker:
    if True:
        query_date = request.form.get('QueryDate') # 2018-02-03
        all_users = User.query.filter_by(FlyDate=query_date).all() # list
        if not all_users:
            return jsonify({'status':'1'})
        infos = []
        users = []
        for user in all_users:
            info = {}
            ArriveTime = user.ArriveTime
            ParkDate = user.ParkDate
            info['CarId'] = user.CarId
            info['FlightNum'] = user.FlightNum
            info['ArriveTime'] = user.ArriveTime
            info['ParkDate'] = ParkDate.strftime('%Y-%m-%d')
            info['Phone'] = user.Phone
            info['ParkPlace'] = user.ParkPlace
            info['BackPersons'] = user.BackPersons
            info['BoxNum'] = user.BoxNum
            if ArriveTime is not None: # 计算停车费用
                delta = get_fee(ArriveTime, ParkDate)
                Fee = delta * DAY_FEE + TRAVEL_FEE
                info['Fee'] = Fee
                infos.append(info)
                user.Fee = Fee
            infos.append(info)
            users.append(user)
        try:
            db.session.add_all(users) # add user.Fee to db
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return jsonify({'status':'1'})
        return jsonify({'status':'2', 'infos':infos})
    return jsonify({'status':'0'})


# 顾客付完费用离开后，将user add to table(olduser)
@api.route('/user_leave.php', methods=['POST'])
def user_leave():
    # token = request.form.get('token')
    # parker = Parker.query.filter_by(token=token).first()
    # if parker:
    if True:
        CarId = request.form.get('CarId')
        user = User.query.filter_by(CarId=CarId).first()
        if not user:
            return jsonify({'status':'1'})
        today = datetime.now().strftime('%Y-%m-%d')
        olduser = OldUser(
            CarId = user.CarId,
            FlightNum = user.FlightNum,
            FlyDate = user.FlyDate,
            ArriveTime = user.ArriveTime,
            ParkDate = user.ParkDate,
            Phone = user.Phone,
            ParkPlace = user.ParkPlace,
            BackPersons = user.BackPersons,
            BoxNum = user.BoxNum,
            Fee = user.Fee,
            LeaveDate = today,
        )
        try:
            db.session.add(olduser)
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            logger.error(e)
            db.session.rollback()
            return jsonify({'status':'1'})
        # conn.delete(CarId)
        return jsonify({'status':'2'})
    return jsonify({'status':'0'})


@api.route('/count_info.php', methods=['POST'])
def count_info():
    # token = request.form.get('token')
    # parker = Parker.query.filter_by(token=token).first()
    # if parker:
    if True:
        query_date = request.form.get('QueryDate')
        leave_users = OldUser.query.filter_by(LeaveDate=query_date).all()
        if not leave_users:
            return jsonify({'status':'1'})
        infos = []
        for user in leave_users:
            info = {}
            info['CarId'] = user.CarId
            info['FlightNum'] = user.FlightNum
            info['FlyTime'] = user.FlyDate
            info['ArriveTime'] = user.ArriveTime.strftime['%Y-%m-%d']
            info['ParkDate'] = user.ParkDate.strftime('%Y-%m-%d')
            info['Phone'] = user.Phone
            info['ParkPlace'] = user.ParkPlace
            info['BackPersons'] = user.BackPersons
            info['BoxNum'] = user.BoxNum
            info['Fee'] = user.Fee
            info['LeaveDate'] = user.LeaveDate.strftime['%Y-%m-%d']
            infos.append(info)
        return jsonify({'status':'2', 'infos':infos})
    return jsonify({'status':'0'})


@api.route('/change_pwd.php', methods=['POST'])
def change_pwd():
    token = request.form.get('token')
    parker = Parker.query.filter_by(token=token).first()
    if parker:
    # if True:
        old_pwd = request.form.get('old_pwd')
        if parker.varify_password(old_pwd):
            account = parker.account
            new_pwd = request.form.get('new_pwd')
            token = parker.token
            new_parker = Parker(account=account, password=new_pwd, token=token)
            db.session.delete(parker)
            db.session.add(new_parker)
            db.session.commit()
            return jsonify({'status':'2'})
        return jsonify({'status':'1'})
    return jsonify({'status':'0'})
