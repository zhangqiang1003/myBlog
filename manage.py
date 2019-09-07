from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 导入启动manage.py的操作
from info import app, db

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/index')
def index():
    return 'index'

if __name__ == '__main__':
    manager.run()
