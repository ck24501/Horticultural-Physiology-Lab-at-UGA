#You must use Thonny complier
import arducam_mipicamera as arducam #importing libraries
import RPi.GPIO as GPIO
import v4l2 #sudo pip install v4l2
import time
import os
import csv
import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
import pandas as pd

GPIO.setmode(GPIO.BOARD) #listen for pins
GPIO.setwarnings(False)
GPIO.setup(32, GPIO.OUT) #call pin 32 for use
GPIO.setup(33, GPIO.OUT) #call pin 33 for use
GPIO.setup(35, GPIO.OUT) #call pin 35 to use
GPIO.setup(31, GPIO.OUT) #call pin 31 to use
led = 32 #assign pin 32 to variable 'led'
led2 = 33 #assign pin 33 to variable 'led2'
led3 = 35 #assign pin 35 to variable 'led3'
led4 = 31 #assign pin 31 to variable 'led4'

#Mkae sure all LEDs are off by setting all relevant pins high
GPIO.output(led, GPIO.HIGH)
GPIO.output(led2, GPIO.HIGH)
GPIO.output(led3, GPIO.HIGH)
GPIO.output(led4, GPIO.HIGH)

timestamp = time.strftime("%b-%d-%Y_%H%M") #set timestamp for title of image
  
#parent_dir = "/home/pi/Pictures/"# Parent Directory
parent_dir = "/home/pi/Pictures/"# Parent Directory
directory = str(os.path.join(parent_dir, timestamp))# directory for the IEMI (index analyzer): no '/' in the directory
drct =  str(os.path.join(parent_dir, timestamp)+"/")#directory for taking images: have '/' in drct
os.mkdir(directory)# Create the directory


camera = arducam.mipi_camera() #name the camera
print("Open camera...")
camera.init_camera() #turn on the camera
print("Setting the resolution...")
fmt = camera.set_resolution(1280, 800) #set resolution
print("Current resolution is {}".format(fmt))

time.sleep(0.1) #wait for 0.1 second
    

try:
    print("Setting the Exposure...")
    camera.set_control(v4l2.V4L2_CID_EXPOSURE, 431)#Set relevant exposure (in ms)
    print("Setting the Gain...")
    camera.set_control(v4l2.V4L2_CID_GAIN, 3)#Set gain
    print("Disable Auto Exposure...")
    camera.software_auto_exposure(enable = False)#Disable auto exposure
except Exception as e:
    print(e)
     
GPIO.output(led2, GPIO.LOW) #set led for first picture
time.sleep(0.2) #wait 0.2 seconds
fmt = (timestamp,"RED") #set image title 
frame = camera.capture(encoding = 'jpeg') #take image and store as 'jepg'
frame.as_array.tofile(drct+"{}x{}.jpg".format(fmt[0],fmt[1])) #finalize naming scheme and apply name for storage
#time.sleep(2) #wait for 2 seconds
GPIO.output(led2, GPIO.HIGH) #turn off led

#def set_controls(camera): #set controls and settings for camera

try:
    print("Setting the Exposure...")
    #camera.set_control(v4l2.V4L2_CID_EXPOSURE, 503)#Set relevanmt exposure
    camera.set_control(v4l2.V4L2_CID_EXPOSURE, 543)#Set relevanmt exposure

except Exception as e:
    print(e)

GPIO.output(led3, GPIO.LOW) #set led2 for second picture
time.sleep(0.2) #wait 2 seconds
fmt = (timestamp,"IR")#set image title 
frame = camera.capture(encoding = 'jpeg')#take image and store as 'jepg'
frame.as_array.tofile(drct+"{}x{}.jpg".format(fmt[0],fmt[1]))#finalize naming scheme and apply name for storage
GPIO.output(led3, GPIO.HIGH) #turn off led2

try:
    print("Setting the Exposure...")
    camera.set_control(v4l2.V4L2_CID_EXPOSURE, 184)#Set relevant exposure
except Exception as e:
    print(e)

GPIO.output(led4, GPIO.LOW) #set led3 for third picture
time.sleep(0.2) #wait for 0.2 seconds
fmt = (timestamp,"BLUE")#set image title
frame = camera.capture(encoding = 'jpeg')
frame.as_array.tofile(drct+"{}x{}.jpg".format(fmt[0],fmt[1]))#finalize naming scheme and apply name for storage
GPIO.output(led4, GPIO.HIGH)    #turn off led3    

try:
    print("Setting the Exposure...")
    camera.set_control(v4l2.V4L2_CID_EXPOSURE, 514) #Set relevant exposure
except Exception as e:
    print(e)

GPIO.output(led, GPIO.LOW) #set led4 for fourth picture
time.sleep(0.2) #wait for 2 seconds
fmt = (timestamp,"GREEN")#set image title
frame = camera.capture(encoding = 'jpeg')
#cv2.imwrite(str(directory)+"_Green.jpg",frame)#save the background image
frame.as_array.tofile(drct+"{}x{}.jpg".format(fmt[0],fmt[1]))#finalize naming scheme and apply name for storage
GPIO.output(led, GPIO.HIGH)    #turn off led4   

try:
    print("Setting the Exposure...")
    camera.set_control(v4l2.V4L2_CID_EXPOSURE, 500)#Set relevant exposure. Note: MASK image is overexposed on purpuse, to increase contrast between plant and background.
except Exception as e:
    print(e)

GPIO.output(led4, GPIO.LOW) #set led4 (blue) for fifth picture, that would be used for masking
time.sleep(0.2) #wait for 2 seconds
fmt = (timestamp,"mask")#set image title
frame = camera.capture(encoding = 'jpeg')
#cv2.imwrite(str(directory)+"_mask.jpg",frame)#save the background image
frame.as_array.tofile(drct+"{}x{}.jpg".format(fmt[0],fmt[1]))#finalize naming scheme and apply name for storage
GPIO.output(led4, GPIO.HIGH)    #turn off led4   
        
camera.close_camera() #turn off camera

def IEMI(minPxs, maxPxs, MinTHR, csvname, imageformat, folder):
    filePath = folder# tells program where to look for images. D0 NOT change. If you need to change the folder, do so near the bottom of the program.
    # Make sure to specify the correct file extension for your images!!!
    fileList=glob.glob(filePath+imageformat)
    
    for a in fileList[::-1]:# A for loop if statement to extract all file list except 'histogram.png' and 'filterd.png'
        if a.find('_binary.png')>-1 or a.find('_inverted_histogram.png')>-1 or a.find('inverted.png')>-1: #if the list contains a filename matches with these texts
            fileList.remove(a)#remove these filenames from the list

    with open(csvname, 'a', newline='') as csvfile: #to create csv file which will include the data
        writer = csv.DictWriter(csvfile, fieldnames = ["File name","Avg_Hist_ACI", "Std_Hist_ACI", "Avg_Hist_NDVI", "Std_Hist_NDVI", "Area"]) #header of each column within the csv file,
        writer.writeheader()
        
    for fdx, filename in enumerate(fileList): #A For loop statment: iteration from all indices (the filenames) within the folder
        fname = filename.rsplit(".", 1)[0] #Treating the string into a list following the separator "."    
        #print(fname)
        if filename.find('mask')!= -1:#mask = image to be used for masking
            masking = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            
            inverted_masking = cv2.bitwise_not(masking) #np.invert(img)
            cv2.imwrite(str(fname)+"_inverted.png",inverted_masking)
            Hist = cv2.calcHist([inverted_masking], [0], None, [255], [0,255]) #make a histogram of pixel intensity
            plt.plot(Hist),plt.yscale('log'),plt.xlabel('Intensity'),plt.ylabel('Pixel frequency'),plt.title('Mask Pixel frequency'),plt.savefig(str(fname)+"_inverted_histogram.png"),plt.close()

            # Find the location in the histogram with the lowest pixel intensity (within a specified range of pixel intensities)
            # Underlying assumption is that the lowest value between background and plant is somewhere 
            # at a pixel intensity between 20 and 90. That range can be easily adjusted in the following instruction.
            # If you change the lower pixel intensity at which to start looking for a minimum, make sure to change that value
            # both after the '=' sign and in the Hist[xx:90] range.
            # print(Hist) This instruction can be used to output the histogram
            minThr = 120 + np.argmin(Hist[120:230])
            print ("Mask threshold = ", minThr)
            
            #threshold the grayscaled-image as two channel (black and white) based on threshold values; 'ret': return
            ret, thres = cv2.threshold(inverted_masking, minThr, 255, cv2.THRESH_BINARY)
        
        
            #The function yields the information of the every seperated components from the thresholded two-channel-image
            nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(thres)
            #labels: matrix size, stats: the stats in the matrix, centroids: x and y locations within the matrix
        
            #CC_STAT_AREA: function to get area from the stats in the components of the image. it can be changed to width or height of the image; please refer https://stackoverflow.com/questions/35854197/how-to-use-opencvs-connected-components-with-stats-in-python
            areas = stats[1:,cv2.CC_STAT_AREA]#with the 'stats' from the two-channel treshold, area can be calculated.
            result = np.zeros((labels.shape), np.uint8)#empty matrix, will be used to write the thresholded two-channel image
 
            #For loop statement to remove pixels outside of the given range; associated to first two parameter of line 114 
            for i in range(0, nlabels - 1):    
                if areas[i] > minPxs and areas[i] <=maxPxs: #if the components within the image meets the conditions, keep and others are discarded
                    result[labels == i + 1] = 255 #convert the only components meeting the conditions
            cv2.imwrite(str(fname)+"_binary.png",result)#save the background image
            bg = cv2.imread(fname+"_binary.png", cv2.IMREAD_UNCHANGED)#open background image without format change
            PCS = cv2.countNonZero(bg)
        elif filename.find("RED") != -1:#Find the image taken under red light
            Pch0 = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) #Read the spectral image at 450nm and define it as Pch0;
            R660 = np.float64(Pch0) #generate R450 objects as arrays in float64 format from Pch0; 
        elif filename.find('IR')!= -1:#ch1 = 870 nm
            Pch1 = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            R870 = np.float64(Pch1)
        elif filename.find('BLUE')!= -1:#ch2 = 440 nm
            Pch2 = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            R440 = np.float64(Pch2) 
        elif filename.find('GREEN')!= -1:#ch3 = 521 nm
            Pch3 = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            R521 = np.float64(Pch3)  
    
    #Generate a RGB image from red-, green-, and blue- grascale images
    RGB = cv2.merge((R440,R521,R660))
    cv2.imwrite(str(fname)+"_RGB.png",RGB)
    
    #Calculate Anthocyanin content index; these calculation need float64 format
    with np.errstate(divide='ignore'):# to ignore zero values of denominator during the index calculation
    #ACI calculation (R660 - R521)/(R660+R521), where R is reflectance value extracted from the multipsectral images
        ACI_before_masking = np.true_divide(np.subtract(R660,R521), np.add(R660,R521))+1 #to have unique values between the object and background 
    #remove the background by conjugating foreground (ACI image) and the background (binary image for object of interest) 
    ACI = cv2.bitwise_and(ACI_before_masking,ACI_before_masking, mask=bg)#mask contains 1 or 0, where 1 is the object of interet and 0 is background
    ACI = np.where(ACI == 0, -1, ACI)#replace the background value, 0, as -1 to have better contrast between background and the object of interest
    ACI = np.where(ACI != -1, ACI-1, ACI)#after the separation between the object and background, subtract 1 again to have the orginial index value
         
    #Calculate Normalized difference vegetation index
    with np.errstate(divide='ignore'):# to ignore zero values of denominator during the index calculation
    #NDVI calculation (R870 - R660)/(R870+R660), where R is reflectance value extracted from the multipsectral images
        NDVI_before_masking = np.true_divide(np.subtract(R870,R660), np.add(R870,R660))+1#to have unique values between the object and background 
    #remove the background by conjugating foreground (NDVI image) and the background (binary image for object of interest) 
    NDVI = cv2.bitwise_and(NDVI_before_masking,NDVI_before_masking, mask=bg)#mask contains 1 or 0, where 1 is the object of interet and 0 is background
    NDVI = np.where(NDVI == 0, -1, NDVI)#replace the background value, 0, as -1 to have better contrast between background and the object of interest
    NDVI = np.where(NDVI != -1, NDVI-1, NDVI)#after the separation between the object and background, subtract 1 again to have the orginial index value

    # Plot a picture of ACI
    plt.colorbar(plt.imshow(ACI), fraction = 0.046, pad=0.04)# to generate a color scale bar
    plt.clim(-1,1)#range of the color gradient for normalized index image
    plt.axis('off') #Not to show the axis info of the image
    plt.savefig(str(fname)+"_ACI.jpg", dpi = 300) #save the ACI image in the directory of where the image is located
    plt.close() #close the ACI image
         
    # Plot a picture of NDVI
    plt.colorbar(plt.imshow(NDVI), fraction = 0.046, pad=0.04)# to generate a color scale bar
    plt.clim(-1,1)#range of the color gradient for normalized index image
    plt.axis('off') #Not to show the axis info of the image
    plt.savefig(str(fname)+"_NDVI.jpg", dpi = 300) #save the NDVI image in the directory of where the image is located
    plt.close() #close the NDVI image
            
    #Plot a histogram of ACI
    ACI_Hist = ACI[ACI !=-1]#remove the background, which has value of -1
    weights = np.ones_like(ACI_Hist)/float(len(ACI_Hist))
    plt.hist(ACI_Hist, weights=weights, bins=300, rwidth =0.85)
    plt.xlabel('ACI')#put a label on x-axis
    plt.ylabel('Proportion')#put a label on y-axis
    plt.title('Normalized ACI') #title of the histogram
    plt.savefig(str(fname)+"_ACI_HIST.jpg", dpi = 300) #save the Histogram in the directory of where the image is located
    plt.close() #close the histogram
    Avg_ACI = np.mean(ACI_Hist) #averaged value from the histogram
    Std_ACI = np.std(ACI_Hist) #standard deviation from the histogram

    #Plot a histogram of NDVI
    NDVI_Hist = NDVI[NDVI !=-1]#remove the background, which has value of -1
    weights = np.ones_like(NDVI_Hist)/float(len(NDVI_Hist))
    plt.hist(NDVI_Hist, weights=weights, bins=255 , rwidth =0.85)
    plt.xlabel('NDVI')#put a label on x-axis
    plt.ylabel('Proportion')#put a label on y-axis
    plt.title('Normalized NDVI') #title of the histogram
    plt.savefig(str(fname)+"_NDVI_HIST.jpg", dpi = 300) #save the Histogram in the directory of where the image is located
    plt.close() #close the histogram
    Avg_NDVI = np.mean(NDVI_Hist) #averaged value from the histogram
    Std_NDVI = np.std(NDVI_Hist) #standard deviation from the histogram

    #write the filename, averaged value of histogram, std value of histogram and PCS into a given csv file name
    with open(csvname, "a", newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow([filename, Avg_ACI, Std_ACI, Avg_NDVI, Std_NDVI, PCS])

    # IF THE ABOVE LINE GIVES AN ERROR MESSAGE, REPLACE WRITEROW WITH WRITE. THE CORRECT FORMAT APPEARS TO DEPENDS ON THE VERSION OF THE OpenCV package
    csvfile.close()
            
IEMI(15000, 300000, 127, "/home/pi/Pictures/Pigment_index_HIST.csv",'/*.jpg',directory) #Trial Run

print("Finished. Images saved in 'Pictures' folder in a subfolder with date and time stamp.")
