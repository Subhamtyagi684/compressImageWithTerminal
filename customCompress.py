from pickletools import optimize
from PIL import Image
import PIL.Image
import os
import io
from io import BytesIO
import argparse
import sys
import base64


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


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
     
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

def get_image(image_path,resized_path=None,width=None,height=None):
    my_image = None;
    
    try:
        with Image.open(image_path) as image:
            my_image = image.copy();
    except Exception as e:
        print("Something went wrong",e);
        return;

    if(my_image!=None):
        getResizingDimensions = resize_image(my_image,width,height);
        print("Original dimension: "+str(my_image.size)+str(" Resized dimension ")+str(getResizingDimensions));
        top = getResizingDimensions[0];
        upper = getResizingDimensions[1];
        fwidth = getResizingDimensions[2];
        fheight = getResizingDimensions[3];


        filename, ext = os.path.splitext(image_path)
        print(filename,ext);
        # if(resized_path and (ext in ['png', 'jpg', 'jpeg'])):
        #     new_filename = resized_path;
        # else:
        #     print("Please provide upload path");
        #     return ;

        # z = my_image.crop((top,upper,fwidth,fheight)).resize((width,height),resample=PIL.Image.ADAPTIVE).convert("RGB");
        # z.save(new_filename,ext,quality=getQuality(z),optimize=True);
        # print("[+] New file saved:", new_filename);
    return;


if(__name__=="__main__"):
    parser = argparse.ArgumentParser(description="Simple Python script for compressing and resizing images")
    parser.add_argument("src", help="Target image to compress and/or resize")
    parser.add_argument("dest", help="Path to upload compressed and/or resized image")
    parser.add_argument("-t", "--type", type=str, help="Extension to save image after compression",default="webp")
    parser.add_argument("-w", "--width", type=int, help="The new width image, make sure to set it with the `height` parameter")
    parser.add_argument("-hh", "--height", type=int, help="The new height for the image, make sure to set it with the `width` parameter")
    args = parser.parse_args();
    print(list(map(lambda x: x, vars(args))));
    x = input("Are you sure to execute function with above details :  (yes/no) ")
    if(x in ['y','yes',"Yes","yES","YES"]):
        print("Now execute the function");
        # get_image(download_path,upload_path);
    else:
        print("Successfully exited.");
