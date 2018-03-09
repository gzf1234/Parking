# -*- coding: utf8 -*-
#user:gzf

from functools import wraps
from flask import request, jsonify
from myapp.models import Parker

def varify_token(f):
    def wrapper(*args, **kwargs):
        token = request.form.get('token')
        parker = Parker.query.filter_by(token=token)
        if not parker:
            return jsonify({'status':'0'})
        return wrapper




