'''converts jpgs in a folder to a .gif'''
import os, sys
try:
    import nuke
except ImportError:
    print 'Could not import nuke module'
    pass
sys.path.insert(0, "\\\\qumulo\\Libraries\\python-lib")
import imageio
import scipy.misc

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def convert(file):
    '''convert using whats rendered'''
    #file = node['file'].value()
    in_file = file
    path = os.path.dirname(file)
    name = os.path.basename(file)
    new_name = name.split('.')[0]+'.gif'

    out_file = os.path.join(path,new_name)
    maxFrame = int(sorted([i.split('.')[-2] for i in os.listdir(path) if i.split('.')[-1] in ['jpeg','jpg']])[-1])
    maxFrame = 24
    scale = 0.25
    speed = 1
    everyNthFrame = 1

    
    return convertJpegFolderToGif(in_file, out_file, maxFrame, scale, speed, everyNthFrame)

def convertJpegFolderToGif(path, out_file, maxFrame, scale, speed, everyNthFrame):
    '''
    _path = "Q:/TEMP_PROJECT/05_COMP/TEM_001_120/02_OUTPUT/03_comp/TEM_001_120_V005/JPEG/"
    _out_file = "Q:/TEMP_PROJECT/03_COORDINATION/_thumbs/TEM_001_120_V005.gif"
    _maxFrame = '100'
    _scale = '0.1'
    _speed = '1'
    _everyNthFrame = '3'
    '''

    verbose = True

    path = path

    img_folder = os.path.dirname(path)


    imgs = [os.path.join(img_folder, i).replace('\\', '/') for i in sorted(os.listdir(img_folder)) if i.lower().split('.')[-1] in ['jpeg','jpg']]

    speed = float(speed)

    scale = float(scale)

    hold = int(everyNthFrame)   

    maximum = int(maxFrame)

    numpy_imgs = []

    cnt = 0
    cnt_to_use = 0

    imgs = imgs[:maximum]
    imgs = imgs[0::hold]
    print imgs
    for i, image in enumerate(imgs):

        the_img = imgs[i]

        im = imageio.imread(the_img)
        im = scipy.misc.imresize(im, scale)
        numpy_imgs.append(im)
        print 'Processing : {0}'.format(os.path.basename(the_img))

    kargs = { 'duration': ((0.1)*hold)/speed }
    imageio.mimsave(out_file, numpy_imgs, **kargs)
    
    return out_file


convert('Q:/Impulse/IMP210/05_COMP/IMP210_011_010/02_OUTPUT/01_precomp/flicker_effect/jpeg/flicker_effect.%04d.jpeg')