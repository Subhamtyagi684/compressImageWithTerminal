from PIL import Image
import PIL.Image
import os
import argparse
import sys


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

def get_image(obj):
    my_image = None;
    width = obj['width'];
    height = obj['height']
    image_path = obj['src'];
    dest_path = str(obj['dest']);
    if not dest_path.endswith('/'):
        dest_path+='/' 

    image_name = str(image_path).split("/")[-1];
    ext = obj['type']
    try:
        with Image.open(image_path) as image:
            my_image = image.copy();
    except Exception as e:
        print("Something went wrong:",'{',e,'}');
        return;

    if(my_image!=None):
        getResizingDimensions = resize_image(my_image,width,height);
        print("Original dimension: "+str(my_image.size)+str(" Resized dimension ")+str(getResizingDimensions));
        top = getResizingDimensions[0];
        upper = getResizingDimensions[1];
        fwidth = getResizingDimensions[2];
        fheight = getResizingDimensions[3];
        filename, dext = os.path.splitext(image_name)
        z = my_image.crop((top,upper,fwidth,fheight)).resize((width,height),resample=PIL.Image.ADAPTIVE).convert("RGB");
        z.save(f"{dest_path}{filename}_compressed.{ext}",ext,quality=getQuality(z),optimize=True);
        print("[+] New file saved:");
    return;


if(__name__=="__main__"):
    parser = argparse.ArgumentParser(description="Simple Python script for compressing and resizing images")
    parser.add_argument("src", help="Target image to compress and/or resize")
    parser.add_argument("dest", help="Path to upload compressed and/or resized image")
    parser.add_argument("-t", "--type", type=str, help="Extension to save image after compression",default="webp")
    parser.add_argument("-width", "--width", type=int, help="The new width image, make sure to set it with the `height` parameter")
    parser.add_argument("-height", "--height", type=int, help="The new height for the image, make sure to set it with the `width` parameter")
    args = vars(parser.parse_args());
    width = args['width']
    while(width==None):
        cust_width = input("Enter the width to resize image: ")
        if(cust_width.isnumeric()):
            args['width'] = cust_width;
            width = cust_width;
        else:
            print("Please provide width in numbers only")
    
    height = args['height']
    while(height==None):
        cust_height = input("Enter the height to resize image: ")
        if(cust_height.isnumeric()):
            args['height']= cust_height;
            height = cust_height
        else:
            print("Please provide height in numbers only")

    if(args['type']!="webp" and (args['type'] not in ['jpg','jpeg','png'])):
        print("Please check your type of extension again")
        exit();
    
    print(args)

    x = input("Are you sure to execute function with above details :  (yes/no) ")
    if(x in ['y','yes',"Yes","yES","YES"]):
        get_image(args);
    else:
        print("Successfully exited.");
