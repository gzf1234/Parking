# -*- coding: utf8 -*-
#user:gzf
'''
启动脚本
'''
import os
from myapp import create_app
from myapp.models import User, OldUser, Parker
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from myapp.models import db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app)

db.init_app(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, OldUser=OldUser, Parker=Parker)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # manager.run()
    app.run(host='0.0.0.0', port=8080, debug=app.debug)