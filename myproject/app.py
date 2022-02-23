from flask import Flask,flash
import os
import sys
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
app = Flask(__name__)
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
basedir= os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    admin=db.Column(db.Integer)
    username=db.Column(db.String(20))
    password=db.Column(db.String(20))

import click
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
from flask_login import LoginManager
login_manager = LoginManager(app)  # 实例化扩展类
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象
from flask_login import UserMixin
class User(db.Model, UserMixin):
  pass
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
from flask_login import login_user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin=request.form['admin']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('index'))
        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and password==user.password:
            login_user(user)  # 登入用户
            flash('Login success.')
            if admin == 1:
             return redirect(url_for('guess'))  # 重定向到主页
            '''elif admin == 2:
                return redirect(url_for('business'))
            else:
                return redirect(url_for('motor'))'''
        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('index'))  # 重定向回登录页面
    return render_template('index.html')
@app.route('/guess')
def guess():
    return render_template('guess.html')
@app.route('/motor')
def motor():
    return render_template('motor.html')
@app.route('/business')
def business():
    return render_template('business.html')
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')
@app.route('/sign_up_load',methods=['GET','POST'])
def sign_up_load():
    username = request.form['username']
    password = request.form['password']
    admin=request.form['admin']
    u=User(admin=admin,username=username,password=password)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('index'))
@app.route('/delete',methods=['GET','POST'])
def delete():
    return render_template('delete.html')
if __name__=='__main__':
    app.run()