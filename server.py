#-*-coding:utf-8-*-
from flask import Flask
from flask import request
import cv2
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

@app.route('/')
def test():
    return '服务器正常运行'



#此方法处理用户注册
@app.route('/register',methods=['POST'])
def register():
   # username=request.form['username']
    #password=request.form['password']
    f = request.files['file']
    #print('username:'+username)
    print('连接成功')
   # 当前文件所在路径
    basepath = os.path.dirname(__file__)
    # 一定要先创建该文件夹，不然会提示没有该路径
    #upload_path = os.path.join(basepath, '1115/')
    upload_path = os.path.join(basepath, '1115', secure_filename(f.filename))
    # upload_path="d:/1115/"
    # 保存文件
    f.save(upload_path) 
    os.system("python C://Users//vesper//chineseocr//wwhtest.py")
    return '注册成功'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
