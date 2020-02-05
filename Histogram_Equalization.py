# -*- coding:utf-8 -*-
import tkinter as tk # need to import before using Tkinter
import cv2,time
import numpy as np#  Introducing numpy for matrix operations
from matplotlib import pyplot as plt
# Step 1, instantiate object, create window window
window = tk.Tk()

#Step 2, give the name of the window visualization
window.title('My Window')

# Step 3, set the size of the window (length * width)
def center_window(w, h):
    # Get the screen width, height
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # Calculate x, y position
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
center_window(1000, 700)

#window.geometry('1000x700')  # 这里的乘是小x

# Step 4, set the label on the graphical interface
var = tk.StringVar()  # Set the contents of the label tag to the character type, and use var to receive the outgoing content of the hit_me function for display on the label.
l = tk.Label(window, textvariable=var, bg='green', fg='blue', font=('Arial', 20), width=50, height=10)
# Description: bg is the background, fg is the font color, font is the font, width is long, and height is high. The length and height here are the length and height of the character. For example, height=2, the label has 2 characters so high.
l.pack()

on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('you hit me')
    else:
        on_hit = False
        var.set('')

on_Webcam = False
def Webcam_capture():
    global on_Webcam
    var.set('VideoCapture')
    if on_Webcam == False:
        #set a video capture instance
        cap = cv2.VideoCapture(0)  # open the video

        # Setting the size of the screen
        # Picture width is set to 9920
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 9920)
        # setting the size of the height 9080
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 9080)

        #Create a window called "capture"
        #Window attribute flags
        # * Widow_normal ： Window can shrink
        # * widow_keepration :Maintain ratio during window scaling
        # * window_Gui_expanded : Gui window enhanced with new version features
        cv2.namedWindow('capture', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)

        while (1):
            # get a frame
            # If the screen is read successfully, ret= true, frame is the image object read (numpy ndarry format)
            ret, frame = cap.read()#Get the picture frame by frame If the picture is read successfully
            # show a frame
            # Update window The picture window in capture is automatically adjusted to the image size.
            # The first parameter is the name of the window, followed by the image. Can create multiple windows, but must give them different names

            cv2.imshow("capture", frame)  # Generate camera window


            if cv2.waitKey(1) & 0xFF == ord('q'):  # If you press q, the screenshot is saved and exited.

                cv2.imwrite("/Users/wangxiang/Downloads/test.png", frame)
                break

        cap.release()
        cv2.destroyAllWindows()
        var.set('VideoCapture')
    else:
        on_Webcam = False
        var.set('')


on_showimg = False
def Show_img():
    global on_showimg
    var.set('Show Snapshoot!!!')
    if on_showimg == False:
        # on_showimg = True
        img = cv2.imread("/Users/wangxiang/Downloads/test.png")
        emptyImage = np.zeros(img.shape, np.uint8)

        emptyImage2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#change color space from  BGR to GRAY

        # cv2.imshow("EmptyImage", emptyImage)
        cv2.imshow("test", img)
        # cv2.imshow("EmptyImage2", emptyImage2)

        cv2.waitKey(0)
        #cv2.destroyAllWindows()

    else:
        on_showimg = False
        var.set('')

on_he = False
def Histo_Equ():
    global on_he


    if on_he == False:
        #on_hit = True
        for i in range(1,8):

            img=cv2.imread("/Users/wangxiang/Downloads/%d.bmp"%(i), 0)
            var.set('Histogram Equalization')
            hist, bins = np.histogram(img.flatten(), 256, [0, 256])  # Img.flatten turns an array into a one-dimensional array


            cdf = hist.cumsum()  # Calculate histogram

            cdf_normalized = cdf * hist.max() / cdf.max()

            cdf_m = np.ma.masked_equal(cdf, 0)
            cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
            # Assign a value to the masked element, where the assignment is 0
            cdf = np.ma.filled(cdf_m, 0).astype('uint8')

            img2 = cdf[img]
            cv2.imshow('1.bmp', img2)
            cv2.waitKey(1)

            cv2.imshow('%d.bmp'%(i), img2)
            plt.plot(cdf_normalized, color='b')
            plt.hist(img2.flatten(), 256, [0, 256], color='green')
            plt.xlim([0, 256])
            plt.legend(('cdf', 'histogram'), loc='upper left')
            plt.show()
            cv2.waitKey(1)



    else:
        on_he = False
        var.set('')


on_clahe = False
def CLAHE_img():
    global on_clahe

    if on_clahe == False:
        var.set('Contrast Limited Adaptive Histogram Equalization')

        for i in range(1, 8):
            img = cv2.imread('/Users/wangxiang/Downloads/%d.bmp' %(i), 0)  # Read directly as a grayscale image
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(10, 10))
            cl1 = clahe.apply(img)

            plt.subplot(121)
            plt.imshow(img, 'gray')

            plt.subplot(122)
            plt.imshow(cl1, 'gray')

            plt.show()



    else:
        on_clahe = False
        var.set('')


# Step 5, set the Button button in the window interface setting
b1 = tk.Button(window, text='VideoCapture', font=('Arial', 12), width=15, height=5, command=Webcam_capture)
b1.pack()


b2 = tk.Button(window, text='show snapshoot', font=('Arial', 12), width=15, height=5, command=Show_img)
b2.pack()

b3 = tk.Button(window, text='show Histogram Equalization', font=('Arial', 12), width=15, height=5, command=Histo_Equ)
b3.pack()

b4 = tk.Button(window, text='show Contrast Limited Histogram Equalization', font=('Arial', 12), width=15, height=5, command=CLAHE_img)
b4.pack()

b5 = tk.Button(window, text='hit me', font=('Arial', 12), width=15, height=5, command=hit_me)
b5.pack()
#main window loop display

window.mainloop()








