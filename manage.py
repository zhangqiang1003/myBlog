from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 导入启动manage.py的操作
from info import create_app, db

app = create_app('development')

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/index')
def index():
    current_app.logger.debug('debug')
    current_app.logger.error('error')
    return 'index'

if __name__ == '__main__':
    manager.run()
