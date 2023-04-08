#!/usr/bin/python3
import multiprocessing
import ffmpeg
import math
from os.path import exists
import os
from pathlib import  Path
from PIL import Image
import argparse

IMAGES_FOLDER="input_upscaled/"
SCALED_FOLDER="output_frames/"
NPROCS=5
INPUT_FORMAT='png'
OUTPUT_FORMAT='jpg'

def load_image(filename,folder=IMAGES_FOLDER,fformat=INPUT_FORMAT):
    filename=folder+str(filename)+'.'+fformat
    return Image.open(filename)

def gen_frames_out(current):
    pool = multiprocessing.Pool(NPROCS)
    result = pool.map(gen_frame_out, range(0,current-1))

def get_image_size():
    im = Image.open(IMAGES_FOLDER+'/0.png')
    return im.size[0]

def gen_frame_out(current):
    w=3840 
    h=2160
    r=w/h
    print('Starting {}'.format(current))
    frame_count=1000*current
    position = 0
    #bimage = Image.new('RGB', (int((im_width*2)-(im_width/4)), im_width))
    bimage = Image.new('RGB', (int((im_width*4)-(3*(im_width/4))), im_width))
    bimage.paste(load_image(current),(0,0))
    bimage.paste(load_image(current+1),(int(3*(im_width/4)),0))
    bimage.paste(load_image(current+2),(int(6*(im_width/4)),0))
    bimage.paste(load_image(current+3),(int(9*(im_width/4)),0))
    #bimage.save(str(current)+".jpg")
    while position <= int(3*(im_width/4))-speed:
        #If the frame does not exist
        if not exists(SCALED_FOLDER+str(frame_count).zfill(12)+".jpg"):
            outimage = Image.new('RGB', (w,h))
            sbit=bimage.crop((position,0,int(im_width*r)+position,im_width)) 
            outimage.paste(sbit.resize((w,h),Image.LANCZOS),(0,0))
            #outimage.paste(sbit,(0,0) )
            outimage.save(SCALED_FOLDER+str(frame_count).zfill(12)+".jpg")
            #sbit.save(SCALED_FOLDER+str(frame_count).zfill(12)+".jpg")
        position = position+speed
        frame_count=frame_count+1
    print('   Finished {}'.format(current))
    return True

def gen_video():
    output = ( ffmpeg
    .input(SCALED_FOLDER+'*.jpg', pattern_type='glob', framerate=25)
    #.filter('crop',im_width,int(math.floor(im_width/1.77777)))
    .output('walk.mp4')
    .run())
    
def get_current():
    count=0
    for path in os.listdir(IMAGES_FOLDER):
        if os.path.isfile(os.path.join(IMAGES_FOLDER, path)):
            count += 1
    return count-2

argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--speed",type=int, required=False, help="Movement speed. Default is 10",default=20)
args = argParser.parse_args()
speed=args.speed
im_width=get_image_size()
current=get_current()
print('Moving speed: {}. Image width: {}. Total images: {}.'.format(speed,im_width,current))
gen_frames_out(current)
gen_video()
#assure output croped size is 4k, no matter what input size it is, or maybe even select output resolution
