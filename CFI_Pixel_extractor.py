# -*- coding: utf-8 -*-
"""
Created on Sun Oct 4 21:21:44 2020
************************************************************************************************************************
To run the program, install Anaconda (freeware). After installing Anaconda, you also need to add 'OpenCV'
Use the Windows search to look for 'Anaconda Prompt (Anaconda 3)', type 'pip install opencv-python' to install OpenCV
************************************************************************************************************************
Within Anaconda Navigator run Spyder (that is different version of Python). The current version of this program works with any combinations of Python (3.7.9 ~ 3.9.1), SPYDER (4.1.4 ~ 4.2.0) and OpenCV (4.3.0~4.5.1), but has not been tested with all other versions of Python.
Versions matter! This program may not work with other versions! To check, update or change version of Python, please read the supplemental text file!
 
@Author: Changhyeon Kim (credit to Momo from the Computational Plant Science Lab at UGA, Marc, and Lynne for adding automated thresholding)
 
@Description: Convert chlorophyll fluorescence images into thresholded images and count the pixel number representing the canopy.
Note: the program will automatically analyze all images in the specified folder
 
User can change minimum and maximum pixel number to be analyzed within an image, an optimal pixel intensity threshold (now automated), csv filename, and folder.
 
Output: Integrated pixel number of plants (or a plant) from an image, a csv file including the values, and processed (binary) images in the directory
        
11/10/2020 Update: the program now automatically determines the optimal pixel intensity threshold to separate canopy from beackground. Background has low pixel intensity, canopy has a higher intensity.
The program now looks for a local minimum in the pixel intensity histogram in the intensity range from 20 to 90 (user adjustable in the line 141).

2/5/2021 Update: all parameters can be changed in the only one line (line 141) instead the middle of program.  
Whether the program works well can be easily checked using the binary canopy images that are created, as well as the pixel intensity histogram plot created in Python

2/9/2021 Update: Histogram plots of binary images will be generated as the output of the prgram. That values can be used to determine optimum threshold value for line 141

************************************************************************************************************************
********       ONLY A FEW PARAMETERS SHOULD BE ADJUST BY USERS. ALL NEAR THE BOTTOM OF THE PROGRAM:
********       
********       IN PxEx(0, 3000000, 1, '/*.jpg', 20, 90, 'C:/Pics/Canopy/test.csv', 'C:/Pics/Canopy') (line 141) 
********       THE FIRST AND SECOND PARAMETER ARE MINIMUM AND MAXIMUM PIXEL NUMBER TO BE ANALYZED IN THE PROGRAM. 
********       THE 3RD VALUE IS A CALIBRATION FACTOR (PIXEL SIZE OF A KNOWN DISTANCE) TO CONVERT PIXELS TO AREA, 
********       THE 4TH PARAMETER IS FORMAT OF IMAGES THAT USER HAVE TO SPECIFY THE EXTENSION OF YOUR IMAGES (Note: that JPEG and JPG are different!),
********       THE 5TH and 6TH VALUES ARE VALUES TO GET MINIMUM PIXEL INTENSITY (See the pragraph in line 37 to change the default values),
********       C:/Pics/Canopy/test.csv IS THE NAME OF THE OUTPUT FILE (ONLY CSV FORMAT ALLOWED IN THE PROGRAM),
********       AND C:/Pics/Canopy IS THE FOLDER THAT CONTAINS THE IMAGES. NOTE: VERY LONG FOLDER NAMES MAY CAUSE PROBLEMS!
********          
********       THE PIXEL INTENSITY RANGE MAY NEED TO BE ADJUSTED TO LOOK FOR THE OPTIMAL THRESHOLD BETWEEN BACKGROUND AND CANOPY
********       THE BEST RANGE DEPENDS ON PICTURE QUALITY. IF THE BACKGROUND IS VERY DARK TO MINIMUM VALUE (50 IS THE EXAMPLE BELOW) MAY NEED TO BE LOWERED.  
********       IF NEEDED, ADJUST THAT VALUE (line 141) IN BOTH INSTANCES IN THE INSTRUCTION BELOW. SO FAR I HAVE NOT SEEN EXAMPLES WHERE THE UPPER PART OF THE RANGE
********       NEEDS TO BE ADJUSTED, BUT IF THE CANOPY IS VERY BRIGHT, THE '90' CAN BE INCREASEDE TO A HIGHER VALUE.
********       WHETHER THE RANGE FOR THRESHOLDING NEEDS TO BE ADJUSTED CAN EASILY BE SEEN BY COMPARING THE ORIGINAL IMAGES WITH THE BINARY IMAGES THAT GET CREATED (IN THE SAME FOLDER AS THE ORIGNAL IMAGES)
********       e.g.) minThr = 50 + np.argmin(Hist[50:90]) 
********   
********       THE OUTPUT FILE GETS WRITTEN TO THE SAME DIRECTORY AS WHERE THE PROGRAM IS SAVED. NOT SURE HOW TO CHANGE THAT. OUTPUTY ALSO GETS WRITTEN TO CONSOLE (BOTTOM RIGHT WINDOW)
************************************************************************************************************************    
 
"""
#Libraries (No need to change)
import csv
import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
 
#Pixel extractor (Developers defined function; all you need to change are in line 141)============
def PxEx(minPxs, maxPxs, calibrator, imageformat, Histmin, Histmax, csvname, directory):
    #minPxs: minimum pixel number range of components within an image
    #maxPxs: mxaimum pixel number range of components within an image
    #calibrator: pixel number of a known distance; to convert pixel as an area
    #imageformat: format of the images that users want to analyze (e.g.: jpg, png, or tif)
    #Histmin: minimum pixel intensity in the histogram of intensity to look for the optimal threshold between background and canopy
    #Histmax: maximum pixel intensity in the histogram of intensity. Most of time, it is 90 (default)
    #csvname: a file name for the result in csv format with its directory
    #directory: a location of the images that users want to analyze
    
    path= directory# tells program where to look for images. D0 NOT change. If you need to change the folder, do so near the bottom of the program.
    # Make sure to specify the correct file extension for your images!!!
    fileList=glob.glob(path+imageformat)
    for a in fileList[::-1]:# A for loop if statement to extract all file list except 'histogram.png' and 'filterd.png'
        if a.find('_filterd.png')>-1 or a.find('histogram.png')>-1: #if the list contains a filename matches with these texts
            fileList.remove(a)#remove these filenames from the list
    
    with open(csvname, 'w', newline='') as csvfile: #to create csv file 
        writer = csv.DictWriter(csvfile, fieldnames = ["File name","Minimum threshold", "Pixel Number", "Area"]) #header of each column within the csv file
        writer.writeheader()
 
    for fdx, filename in enumerate(fileList): #A For loop statment: iteration from all indices (the filenames) within the folder
        fname = filename.rsplit(".", 1)[0] #Treating the string into a list following the separator "."    
        img = cv2.imread(filename) #Define 'img' that reads an image corresponding to a filename;
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#Although we use generally grayscale image, for color or RGB image, convert image as grayscale.
        #To move on, make sure the images are in 8 bits (or grayscale), that is necessary to convert the image as a two-channel image.
    
        #Automated method to find pixel intensity for thresholding from a histogram of pixel intensity
        Hist = cv2.calcHist([gray], [0], None, [255], [0,255]) #make a histogram of pixel intensity
        # Find the location in the histogram with the lowest pixel intensity (within a specified range of pixel intensities)
        # Underlying assumption is that the lowest value between background and plant is somewhere 
        # at a pixel intensity between 20 and 90. That range can be easily adjusted in the following instruction.
        # If you change the lower pixel intensity at which to start looking for a minimum, make sure to change that value
        # both after the '=' sign and in the Hist[xx:90] range.
        # print(Hist) This instruction can be used to output the histogram
        minThr = Histmin + np.argmin(Hist[Histmin:Histmax])
        
        #threshold the grayscaled-image as two channel (black and white) based on threshold values; 'ret': return
        ret, thres = cv2.threshold(gray, minThr, 255, cv2.THRESH_BINARY)    
        
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
        
        #Generate thresholded two channel images along with their original filename
        cv2.imwrite(str(fname)+"_filterd.png",result) #Save a masked image
        plt.plot(Hist), plt.yscale('log'), plt.savefig(str(fname)+"_histogram.png"), plt.close()
        #Print the histogram plot of 'gray', #Convert the y-axis of histogram in log scale, #Save the histogram plots as png files, #close the file
        pixel_number = cv2.countNonZero(result) #Count the pixel number of white (255) of the two chanel image
        area = pixel_number//(calibrator*calibrator) #Convert the pixel number as an area upon the calibrator (pixel number of a known distance)
        # Print file name, pixel intensity threshold, and total number of pixels
        print(filename, minThr, pixel_number, area) 
 
        #write the pixel numbers, area and the minimum threshold value as a given csv file name
        with open(csvname, "a", newline='') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow([filename, minThr, pixel_number, area])
            # IF THE ABOVE LINE GIVES AN ERROR MESSAGE, REPLACE WRITEROW WITH WRITE. THE CORRECT FORMAT APPEARS TO DEPENDS ON THE VERSION OF THE OpenCV package
        csvfile.close()
'''
#Input code              
# Parameter 1 and 2) The first two values, set the lower and upper boundaries of the pixel size of individual objects in the image that are 
#                    included in the pixel count. This can be used to remove background noise. 
# Parameter 3) This is a calibration to convert pixels to area. If you don't know that value yet (typical) leave this at 1 and convert later in Excel
# Parameter 4) This is the format of your image. You can change jpg (default now) as any other format.
# Parameter 5 and 6) They are the minimum and maximum values for adjusting threshold. 
#           e.g.: minThr = 20 + np.argmin(Hist[20:90]); 20 is an example minimum value when the background is dark
#           Users can change the values to find the best values for images (see line 37 for the detail); No change 90 unless your canopy is very bright 
# Parameter 7) The name of output file (only csv format allowed) that writes all numbers getting from the program
# Parameter 8) This is where you can specify the folder with your images. The simple solution is to always put your images in the same folder,
#                   analyze them, and then move them to a permamanet folder. That way, you do not need to ever change the program itself.
#              *This program requies '/' for directory, although directory in Window uses '\'. 
'''

PxEx(10, 3000000, 1, '/*.png', 20, 70, 'C:/Users/Username/Downloads/Pxex_example/result.csv', 'C:/Users/Username/Downloads/Pxex_example')
