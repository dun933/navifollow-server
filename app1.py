#-*-coding:utf-8-*-
from flask import Flask
from flask import request
import model
import cv2
import os.path
import re
from apphelper.image import union_rbox,adjust_box_to_origin
# import cv2
import os
from werkzeug.utils import secure_filename
import MySQLdb
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def test():
    return '服务器正常运行'

@app.route('/confirm',methods=['POST'])
def confirm():
    db = MySQLdb.connect("localhost", "root", "123456", "db1", charset='utf8' )
    cursor = db.cursor()
    tablename=request.form['tablename']
    print('tablename:'+tablename)
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    # print(tables)
    # print('@@@')
    table_list = re.findall('(\'.*?\')',str(tables))
    # print(table_list)
    table_list = [re.sub("'",'',each) for each in table_list]
    # print(table_list)
    if tablename in table_list:
        return '1'
    else:
        return '0'


#此方法接收图片
@app.route('/upload',methods=['POST'])
def upload():
    db = MySQLdb.connect("localhost", "root", "123456", "db1", charset='utf8' )
    cursor = db.cursor()
    tablename=request.form['tablename']
    f = request.files['file']
    print('连接成功')
   # 当前文件所在路径
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, '1115/1.jpg')
    # 保存文件
    f.save(upload_path) 

    rootdir="1115/"
    list= os.listdir(rootdir)
    # print(list)
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        print(path)
        if os.path.isfile(path):
            img = cv2.imread(path)##GBR
            _,result,angle= model.model(img,
                                        detectAngle=True,##是否进行文字方向检测，通过web传参控制
                                        config=dict(MAX_HORIZONTAL_GAP=50,##字符之间的最大间隔，用于文本行的合并
                                        MIN_V_OVERLAPS=0.6,
                                        MIN_SIZE_SIM=0.6,
                                        TEXT_PROPOSALS_MIN_SCORE=0.1,
                                        TEXT_PROPOSALS_NMS_THRESH=0.3,
                                        TEXT_LINE_NMS_THRESH = 0.7,##文本行之间测iou值
                                               ),
                                        leftAdjust=True,##对检测的文本行进行向左延伸
                                        rightAdjust=True,##对检测的文本行进行向右延伸
                                        alph=0.01,##对检测的文本行进行向右、左延伸的倍数
                                        )
            result = union_rbox(result,0.2)
            res = [{'text':x['text'],
                    'name':str(i),
                    'box':{'cx':x['cx'],
                    'cy':x['cy'],
                    'w':x['w'],
                    'h':x['h'],
                    'angle':x['degree']
                     }
                } for i,x in enumerate(result)]
            res = adjust_box_to_origin(img,angle, res)##修正box
            if res:
                aa=res[0]['text']
                try: 
                    sql="select * from %s where doornum='%s'"%(tablename,aa)
                    # print(sql)
                    cursor.execute(sql)
                    db.commit()
                    results = cursor.fetchall()
                    print(results)
                    return str(results[0][0])
                #     sql="select count(*) from %s"%tablename
                #     # print(sql)
                #     cursor.execute(sql)
                #     db.commit()
                #     lines=cursor.fetchall()#lines[0][0]代表总共有几条记录
                #     #print(lines)
                #     tablelines=int(lines[0][0])
                #     print('tablelines'+str(lines[0][0])
                #     # i=results[0][0]+1
                #     for i in range(results[0][0]+1,tablelines+1):
                #         sql="select * from %s where idnum='%s'"%(tablename,i)
                #         cursor.execute(sql)
                #         db.commit()
                #         results = cursor.fetchall()
                #         print('&&&')
                #         print(results)
                #         if(results[0][1]=='L'):
                #             astr='L'+str(results[0][0])
                #             print('$$$')
                #             print(astr)
                #             # print(alist)
                #             # print(atuple)
                #             # print(atuple[0])
                #             # print(atuple[1])
                #             # return 'test'
                #             return astr
                #         elif(result[0][1]=='R'):
                #             astr='R'+str(results[0][0])
                #             return astr
                #     # return str(results[0][0])
                except Exception as e:
                    print("查询失败：case%s"%e)
                    return '不存在此门牌号'
                # sql = "INSERT INTO `%s`" % tablename + " VALUES(%s, %s, %s)"
                # cursor.execute(sql,(idnum, data2[i], int(data1[i])))
                # sql="SELECT steps FROM %s where doornum='"%tablename+aa+"'"
                # cursor.execute(sql)
                # results = cursor.fetchall()
                # print(results)
                # print("识别结果",i+1,res[0]['text'])
                # if results:
                # return str(results[0][0])
                # else:
                #     return '1'
            else:
                # print("识别结果",i+1,res)
                return '识别失败'
   

if __name__ == '__main__':
    # db = MySQLdb.connect("localhost", "root", "123456", "db1", charset='utf8' )
    # cursor = db.cursor()
    tablename='0'
   # sql="SELECT steps FROM A309B311 where doornum='"++"'"
    # sql = "SELECT * FROM A309B311"
    # try:
    #    # 执行SQL语句
    #    cursor.execute(sql)
    #    # 获取所有记录列表
    #    results = cursor.fetchall()
    #    for row in results:
    #       idnum = row[0]
    #       doornum = row[1]
    #       steps = row[2]
    #       # 打印结果
    #       print("idnum=%s,doornum=%s,steps=%s" % \
    #              (idnum, doornum, steps))
    # except:
    #    print("Error: unable to fecth data")
    app.run(host='0.0.0.0')
