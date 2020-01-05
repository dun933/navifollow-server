#-*-coding:utf-8-*-
from flask import Flask
from flask import request
import cv2
import os
import shutil
import pymysql
from werkzeug.utils import secure_filename
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def test():
    return '服务器正常运行'

#此方法接收图片
@app.route('/upload',methods=['POST'])
def upload():
    tablename=request.form['tablename']
    print(tablename)
    f = request.files['file']
    print('连接成功')
   # 当前文件所在路径
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'txts', secure_filename("5555.3gp"))
    # 保存文件
    f.save(upload_path)
    f = request.files['file2']
    print('连接成功2')
   # 当前文件所在路径
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'txts', secure_filename("6666.txt"))
    # 保存文件
    f.save(upload_path)

    f = request.files['file3']
    print('连接成功3')
    #当前文件所在路径
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'txts', secure_filename("orients.txt"))
    # 保存文件
    f.save(upload_path)
    print('保存成功')
    ################################
    vc = cv2.VideoCapture(basepath+'txts/5555.3gp') #读取视频文件
    c = 1
    rval=False 
    if vc.isOpened():#判断是否正常打开
        rval,frame = vc.read()
    else:
        rval = False
    timeF = 23 #视频帧计数间隔频率
    while rval: #循环读取视频帧
        rval,frame = vc.read()
        if(c%timeF==0):
            cv2.imwrite(basepath+'1115/'+str(c)+'.jpg',frame) # 存储为图像
        c = c + 1
        cv2.waitKey(1)
    vc.release()
    ################################33
    os.system("python wwhtest.py")  
    dirpath=basepath+'1115'
    shutil.rmtree(dirpath) # 能删除该文件夹和文件夹下所有文件
    os.mkdir(dirpath)
    ############################创建数据表
    db = pymysql.connect("localhost","root","123456","db1", autocommit = 1)
    cursor = db.cursor()
    sql = """
            create table %s(
            idnum int not null,doornum char(20),steps int)
        """%tablename
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s"%e)
    # finally:
    #     #关闭游标连接
    #     cursor.close()
    #     # 关闭数据库连接
    #     db.close()
########################################插入数据
    f = open("txts/6666.txt","r")   #设置文件对象
    data1 = f.read().splitlines()  #直接将文件中按行读到list里，效果与方法2一样
    f.close()             #关闭文件
    f = open("txts/result.txt","r")   #设置文件对象
    data2 = f.read().splitlines()  #直接将文件中按行读到list里，效果与方法2一样
    f.close()             #关闭文件
    #####################读orients
    f=open("txts/orients.txt","r")
    data3=f.read().splitlines()
    f.close()
    print(data3)
    di=1
    tempstring=data3[di]
    turnseconds=tempstring[1:]
    turns=tempstring[0:1]
    print('@@@@@@@@@@@')
    ###################
    length=len(data2)
    print(length)
    idnum=0
    sign=0
    for i in range(length):
        if(i==int(turnseconds)-1):
            print('第'+turnseconds+'秒向'+turns+'转')
            idnum+=1
            print('#')
            print(idnum)
            sql = "INSERT INTO `%s`" % tablename + " VALUES(%s, %s, %s)"
            cursor.execute(sql,(idnum, turns, int(data1[i])))
            sign=1
            di+=1
            if(di==len(data3)):
                sign=0
                continue
            tempstring=data3[di]
            turnseconds=tempstring[1:]
            turns=tempstring[0:1]
        # print('-------------daozhe')   
        if sign==1:
            sign=0
            continue
        # if (data2[i]!='NaN'):
        # print('daozhe==========')
        try:
            idnum+=1
            print(idnum)
            print('^^^')
            print(i)
            sql = "INSERT INTO `%s`" % tablename + " VALUES(%s, %s, %s)"
            cursor.execute(sql,(idnum, data2[i], int(data1[i])))
            # print('successaaa')
        except Exception as e:
            print("插入失败：case%s"%e)
        # sql = "insert into %s(`idnum`,`doornum`,`steps`)"%tablename+"values(%s,%s,%s)"
        # cursor.execute(sql,[i+1, data2[i], int(data1[i])])
    cursor.close()
    #     # 关闭数据库连接
    db.close()
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)