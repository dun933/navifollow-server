import model
import cv2
import os.path
from apphelper.image import union_rbox,adjust_box_to_origin
rootdir="1115/"
fo = open("txts/result.txt", "w")
list= os.listdir(rootdir)
print(list)
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
            print("识别结果",i+1,res[0]['text'])
            fo.write(res[0]['text']+'\r\n')
        else:
            print("识别结果",i+1,res)
            fo.write('NaN'+'\r\n')
fo.close()