#!/bin/bash
mkdir output_frames/
mkdir input_upscaled
mkdir input
rm walk.mp4
rm walk_reversed.mp4
rm input/*
rm input_upscaled/*
rm output_frames/*
rm reversed/tmp/*
rm reversed/*.jpg
cp str2imgwalk/out/*[0-9].png input/
waifu2x-ncnn-vulkan-20220728-ubuntu/waifu2x-ncnn-vulkan -f png -i input/ -o input_upscaled/ -s 8 -n 3 -g 0 
./render_walk.py 
