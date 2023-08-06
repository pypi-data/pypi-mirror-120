# import onnx
import os
import onnxruntime
import numpy as np
from PIL import Image
# import tensorflow as tf

current_dir = os.path.realpath(os.path.dirname(__file__))
yolo5_path = os.path.join(current_dir, 'yolo5.onnx')
class_names = '''person
bicycle
car
motorbike
aeroplane
bus
train
truck
boat
traffic light
fire hydrant
stop sign
parking meter
bench
bird
cat
dog
horse
sheep
cow
elephant
bear
zebra
giraffe
backpack
umbrella
handbag
tie
suitcase
frisbee
skis
snowboard
sports ball
kite
baseball bat
baseball glove
skateboard
surfboard
tennis racket
bottle
wine glass
cup
fork
knife
spoon
bowl
banana
apple
sandwich
orange
broccoli
carrot
hot dog
pizza
donut
cake
chair
sofa
pottedplant
bed
diningtable
toilet
tvmonitor
laptop
mouse
remote
keyboard
cell phone
microwave
oven
toaster
sink
refrigerator
book
clock
vase
scissors
teddy bear
hair drier
toothbrush'''.split('\n')
cn_class_names = '''人
自行车
车
摩托车
飞机
公共汽车
火车
卡车
船
红绿灯
消防栓
停止标志
停车收费表
长椅
鸟
猫
狗
马
羊
奶牛
大象
熊
斑马
长颈鹿
背包
伞
手提包
领带
手提箱
飞盘
滑雪板
滑雪板
运动球
风筝
棒球棒
棒球手套
滑板
冲浪板
网球拍
瓶子
红酒杯
杯子
叉子
刀
勺子
碗
香蕉
苹果
三明治
橘子
西兰花
萝卜
热狗
比萨
甜甜圈
蛋糕
椅子
沙发
盆栽植物
床
餐桌
洗手间
电视监视器
笔记本电脑
鼠
偏僻的
键盘
手机
微波
烤箱
烤面包机
下沉
冰箱
书
时钟
花瓶
剪刀
玩具熊
吹风机
牙刷'''.split('\n')

# this function is from yolo3.utils.letterbox_image
def letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    iw, ih = image.size
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = image.resize((nw,nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128,128,128))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    return new_image

def preprocess(img):
    model_image_size = (416, 416)
    boxed_image = letterbox_image(img, tuple(reversed(model_image_size)))
    image_data = np.array(boxed_image, dtype='float32')
    image_data /= 255.
    image_data = np.transpose(image_data, [2, 0, 1])
    image_data = np.expand_dims(image_data, 0)
    return image_data

def bb_intersection_over_union(boxA, boxB):
    """
    source
    https://gist.github.com/meyerjo/dd3533edc97c81258898f60d8978eddc
    """
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou

YOLO5 = None

def predict(img_path, threshold=0.45, overlap_threhold=0.45):
    global YOLO5
    if YOLO5 is None:
        YOLO5 = onnxruntime.InferenceSession(yolo5_path)
    ses = YOLO5

    img = Image.open(img_path)
    img_vec = np.array(img.resize((320, 320)), dtype=np.float32)
    img_vec = img_vec[:, :, :3]
    img_vec = img_vec.reshape((1, 320, 320, 3))
    img_vec /= 255.0
    outputs = ses.run(None, {'input_1': img_vec})
    pred = outputs[0]

    pred[..., 0] *= img.size[1]  # x
    pred[..., 1] *= img.size[0]  # y
    pred[..., 2] *= img.size[1]  # w
    pred[..., 3] *= img.size[0]  # h

    ret = []
    for i in range(pred.shape[1]):
        x, y, w, h, score = pred[0, i, :5]
        box = [x, y, w + x, h + y]
        box = [int(x) for x in box]
        cls = np.argmax(pred[0, i, 5:])
        ret.append({
            'score': score,
            'cls': class_names[cls],
            'cn_cls': cn_class_names[cls],
            'box': box,
        })
    ret = sorted(ret, key=lambda x: x['score'], reverse=True)
    filtered_ret = []
    for item in ret:
        if item['score'] > threshold:
            bad = False
            for other in filtered_ret:
                if bb_intersection_over_union(item['box'], other['box']) > overlap_threhold:
                    bad = True
                    break
            if not bad:
                filtered_ret.append(item)
    return filtered_ret
