import numpy as np
from PIL import Image

import _init_paths

import caffe
import time

# load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
im = Image.open('data/pascal/VOC2012/JPEGImages/2007_000129.jpg')
in_ = np.array(im, dtype=np.float32)
in_ = in_[:,:,::-1]
in_ -= np.array((104.00698793,116.66876762,122.67891434))
in_ = in_.transpose((2,0,1))

# load net
net = caffe.Net('voc-fcn8s/deploy.prototxt', 'voc-fcn8s/fcn8s-heavy-pascal.caffemodel', caffe.TEST)
# shape for input (data blob is N x C x H x W), set data
net.blobs['data'].reshape(1, *in_.shape)
net.blobs['data'].data[...] = in_
# run net and take argmax for prediction
raw_input('start timer')
start_time = time.time()
net.forward()
total_time = time.time() - start_time
print "total_time:", total_time
out = net.blobs['score'].data[0].argmax(axis=0)

#------------------------------------------
arr=out.astype(np.uint8)
im=Image.fromarray(arr)

palette=[]
for i in range(256):
    palette.extend((i,i,i))
palette[:3*21]=np.array([[0, 0, 0],
                            [128, 0, 0],
                            [0, 128, 0],
                            [128, 128, 0],
                            [0, 0, 128],
                            [128, 0, 128],
                            [0, 128, 128],
                            [128, 128, 128],
                            [64, 0, 0],
                            [192, 0, 0],
                            [64, 128, 0],
                            [192, 128, 0],
                            [64, 0, 128],
                            [192, 0, 128],
                            [64, 128, 128],
                            [192, 128, 128],
                            [0, 64, 0],
                            [128, 64, 0],
                            [0, 192, 0],
                            [128, 192, 0],
                            [0, 64, 128]], dtype='uint8').flatten()

im.putpalette(palette)
im.show()
im.save('test.png')
