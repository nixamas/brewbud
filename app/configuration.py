# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    #DATABASE_URI = 'brewbud.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'brewbud.db')
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "MINHACHAVESECRETA"
    CSRF_ENABLED = True
    USERNAME = 'admin'
    PASSWORD = 'default'
    UPLOAD_FOLDER = "app/static/beerimages/"
    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

    #Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
    #RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
    #RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"

class ProductionConfig(Config):
    #DATABASE_URI = 'mysql://user@localhost/foo'
    DATABASE_URI = 'brewbud.db'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
