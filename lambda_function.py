from PIL import Image
import PIL.Image
import os
import io
from io import BytesIO

import sys
import base64

print(sys.argv)

# 500 X 300

download_path = '../nodejs/pexels-julius-silver-753626.jpg';
upload_path = '../nodejs/resized.webp';


custom_width = 400
custom_height = 400

def getQuality(img):

    bytes = img.tobytes()
    quality = 60
    fileSize = sys.getsizeof(bytes);
    
    if(fileSize > 1024*1024):
        quality = 30;
    elif(fileSize > 1024*512):
        quality = 40;
    elif(fileSize > 1024*256):
        quality = 50;
    return quality;
     
def get_image(image_path, resized_path):
    my_image = None;
    
    try:
        with Image.open(image_path) as image:
            print(image.size)
            my_image = image.copy();
    except Exception as e:
        print("Something went wrong",e);
        return;

    if(my_image!=None):
        getResizingDimensions = resize_image(my_image,custom_width,custom_height);
        print("Original size: "+str(my_image.size)+str(" Resized dimension ")+str(getResizingDimensions));
        top = getResizingDimensions[0]
        upper = getResizingDimensions[1]
        fwidth = getResizingDimensions[2]
        fheight = getResizingDimensions[3]
        z = my_image.crop((top,upper,fwidth,fheight)).resize((custom_width,custom_height),resample=PIL.Image.ADAPTIVE).convert("RGB");
        z.save(upload_path,"webp",quality=getQuality(z));
        # y.show()
    return;

def resize_image(origImage,reqWidth,reqHeight):
    srcWidth = origImage.size[0];
    srcHeight = origImage.size[1];
    scaleX = float(srcWidth / reqWidth);
    scaleY = float(srcHeight / reqHeight);
    scale =  scaleY if scaleX > scaleY else scaleX  
    finalHeight  = int(reqHeight*scale);
    finalWidth  = int(reqWidth*scale);
    x = int((srcWidth -finalWidth)/2);
    y = int((srcHeight -finalHeight)/2);
    vals = [x,y,finalWidth+x,finalHeight+y];
    return vals;


get_image(download_path,upload_path);
