import pytesseract
import cv2
import os
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from tkinter import * 
from tkinter.ttk import *
# importing askopenfile function 
# from class filedialog 
#from tkinter.filedialog import askopenfile 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image
import imageio

# function to select image from which text is to be extracted
def open_file(): 
    #file = askopenfile(mode ='r', filetypes =[('images', '*.png')])
    global imgpath,Lower_right
    imgpath = askopenfilename(filetypes =[('images', '*.png;*.jpg;*.jpeg')]) 
    # show an "Open" dialog box and return the path to the selected file
    if imgpath != '':
        Lower_right = Label(root, 
                      text ='{} successfully loaded✔️'.format(os.path.basename(imgpath))) 
        Lower_right.place(relx = 0.0,  
                     rely = 1.0,  
                     anchor ='sw')
    
    print(imgpath)



#function to check image color
def img_estim(img, thrshld):
    is_light = np.mean(img) > thrshld
    return 'light' if is_light else 'dark'

#function to extract text from selected image
def ext_txt(): 
    image = cv2.imread(imgpath)
    image_work=np.copy(image)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    smooth = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.Canny(smooth,100,300,)
    contours,heirarcy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    print("contours ",len(contours))
    if(len(contours)!=0):
        areas=[cv2.contourArea(c) for c in contours]
        max_index=np.argmax(areas)
        cnt = contours[max_index]
        
    epsilon=0.05*cv2.arcLength(cnt,True)
    approx=cv2.approxPolyDP(cnt,epsilon,True)
    cv2.drawContours(image_work,[approx],-1,(255,0,0),3)
    cv2.imshow("gray",gray)
    cv2.waitKey(1000)
    
    #find Perspective transformation matrix


    warped = image
    cv2.imshow("warped",warped)
    cv2.waitKey(1000)
    #for detect angle of the text and rotate it for better results
    
    coords = np.column_stack(np.where(thresh>0))
    rect = cv2.minAreaRect(coords)
    angle = cv2.minAreaRect(coords)[-1]
    
    #determines the angle of inclination
    if angle <-45:
        angle = -(90+angle)
    else:
        angle = -angle
        
    #rotate the image
    (h,w) = warped.shape[:2]
    center = (w//2,h//2)
    
    M = cv2.getRotationMatrix2D(center,angle,1.0)
    cv2.imshow("RotatedM",warped)
    warped =cv2.warpAffine(warped,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE) 
    cv2.imshow("RotatedA",warped)
    ########################################################################################
    
    #pre-process image for text extraction
    gray_warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
    cv2.imshow("graywarped",gray_warped)
    ret,thresh_warped = cv2.threshold(warped,80,255,cv2.THRESH_BINARY_INV)
    cv2.imshow("thres_warped",thresh_warped)
    cv2.waitKey(1000)
    #cv2.destroyAllWindows()
    global exttxt
    if img_estim(thresh_warped, 127) == 'light':
        exttxt = pytesseract.image_to_string(thresh_warped)
    else:
        exttxt = pytesseract.image_to_string(warped)
    print('thresh_warped is ',img_estim(thresh_warped, 127))
    #exttxt = pytesseract.image_to_string(warped)
    #exttxt = pytesseract.image_to_string(thresh_warped)
    print(exttxt)
    Lower_right = Label(root, 
                      text ='Text Extracted successfully ✔️    ') 
    Lower_right.place(relx = 0.0,  
                     rely = 1.0,  
                     anchor ='sw')
    #msg = Message( root, text = "Text Extracted ✔️")  
    #msg.pack() 
    #cv2.imshow('Result',image)
    #cv2.waitKey(0)

#function to save extracted text into a text file
def save_ext_txt(): 
    files = [('Text Document', '*.txt')] 
    f = asksaveasfile(filetypes = files, defaultextension = files) 
    file = f.name
    print(file)
    #imgname = os.path.basename(imgpath)
    #imgname = imgname+".txt"
    f1 = open(file, "w") #or f = open("F:\py exe\{}.txt".format(imgname), "w")
    f1.write(exttxt)
    f1.close()

    Lower_right = Label(root, 
                      text ='{} saved successfully ✔️'.format(os.path.basename(file))) 
    Lower_right.place(relx = 0.0,  
                     rely = 1.0,  
                     anchor ='sw')

#declaration of some tkinter functions
def quit():
    cv2.destroyAllWindows()
    root.destroy()
    
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo

def ofh(e):
    status_label.config(text="Click to choose an image")
    
def ofhl(e):
    status_label.config(text="")
    
def exth(e):
    status_label.config(text="Click to extract text from chosen image")
    
def exthl(e):
    status_label.config(text="")
    
def svh(e):
    status_label.config(text="Click to save extracted text into a text file")
    
def svhl(e):
    status_label.config(text="")

def qth(e):
    status_label.config(text="Quit")
    
def qthl(e):
    status_label.config(text="")

#root = Toplevel()
root = Tk()
root.title("Intelligent OCR")
photo = PhotoImage(file = "F:\py exe\ocr_ico1.png")
root.iconphoto(False, photo)
root.geometry('1024x720') 

photo1 = PhotoImage(file = r"F:\py exe\buttons\selimg.png")
photo2 = PhotoImage(file = r"F:\py exe\buttons\text.png")
photo3 = PhotoImage(file = r"F:\py exe\buttons\save.png")
photo4 = PhotoImage(file = r"F:\py exe\buttons\quit.png")

btn4 = Button(root,image=photo4, command =  lambda :quit()) 
btn4.pack(side = BOTTOM,pady = 10)   
btn3 = Button(root,image=photo3, command = lambda : save_ext_txt()) 
btn3.pack(side = BOTTOM, pady = 10)    
btn2 = Button(root,image=photo2, command = lambda:ext_txt())
btn2.pack(side = BOTTOM, pady = 10)
btn = Button(root,image=photo1, command = lambda:open_file()) 
btn.pack(side = BOTTOM, pady = 10)

status_label=Label(root,text='click on choose image to start')
status_label.place(relx = 1.0,  rely = 1.0,  anchor ='se')
#status_label.pack(fill=X,side=BOTTOM)
btn.bind("<Enter>",ofh)
btn.bind("<Leave>",ofhl)    
btn2.bind("<Enter>",exth)
btn2.bind("<Leave>",exthl)
btn3.bind("<Enter>",svh)
btn3.bind("<Leave>",svhl)
btn4.bind("<Enter>",qth)
btn4.bind("<Leave>",qthl)
image = Image.open('F:\\py exe\\bgimg3.png')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = Label(root, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)
    
#root.configure(background='grey')
#background_image=ImageTk.PhotoImage(Image.open("F:\\py exe\\bgimg.png"))
#background_label = Label(root, image=background_image)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)


    

root.mainloop()
