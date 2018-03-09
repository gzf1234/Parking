# -*- coding: utf8 -*-
#user:gzf

import os

class Config(object):
    SECRET_KEY = os.environ.get('SERCET_KEY') or 'this is a secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://car:car@192.168.200.129:3306/car'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://car:car@localhost:3306/car'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
}