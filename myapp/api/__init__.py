# -*- coding: utf8 -*-
#user:gzf
from flask import Blueprint

api = Blueprint('api', __name__)

from myapp.api import handle