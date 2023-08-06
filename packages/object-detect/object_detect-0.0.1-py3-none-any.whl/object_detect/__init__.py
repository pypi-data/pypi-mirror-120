# import onnx
import os
import onnxruntime
import numpy as np
from PIL import Image

current_dir = os.path.realpath(os.path.dirname(__file__))
model_path = os.path.join(current_dir, 'tiny-yolov3-11.onnx')
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


SES = None

def predict(img_path, threshold=0.1, overlap_threhold=0.5, ses=None):
    global SES
    if ses is None:
        if SES is None:
            SES = onnxruntime.InferenceSession(model_path)
        ses = SES
    image = Image.open(img_path)
    image = image.resize((456, 456))
    # input
    image_data = preprocess(image)
    image_size = np.array([image.size[1], image.size[0]], dtype=np.float32).reshape(1, 2)
    outputs = ses.run(None, {'input_1': image_data, 'image_shape': image_size})
    n_candidates = outputs[0].shape[1]
    i_batch = 0
    ret = []
    for i in range(n_candidates):
        scores = outputs[1][i_batch, :, i]
        cls = np.argmax(scores)
        score = np.max(scores)
        box = outputs[0][i_batch, i]
        ret.append({
            'score': score,
            'cls': class_names[cls],
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
