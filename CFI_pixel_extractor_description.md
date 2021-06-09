************************************************************************************************************************
To run the program, install Anaconda (freeware). After installing Anaconda, you also need to add 'OpenCV'
Use the Windows search to look for 'Anaconda Prompt (Anaconda 3)', type 'pip install opencv-python' to install OpenCV
************************************************************************************************************************
Within Anaconda Navigator run Spyder (that is different version of Python). The current version of this program works with any combinations of Python (3.7.9 ~ 3.9.1), SPYDER (4.1.4 ~ 4.2.0) and OpenCV (4.3.0~4.5.1), but has not been tested with all other versions of Python.
Versions matter! This program may not work with other versions! To check, update or change version of Python, please read the supplemental text file!
 
@Author: Changhyeon Kim (credit to Momo from the Computational Plant Science Lab at UGA, Marc, and Lynne for adding automated thresholding)
@E-mail: changhyeon.kim@uga.edu

@Description: Convert chlorophyll fluorescence images into thresholded images and count the pixel number representing the canopy.
Note: the program will automatically analyze all images in the specified folder
 
User can change minimum and maximum pixel number to be analyzed within an image, an optimal pixel intensity threshold (now automated), csv filename, and folder.
 
Output: Integrated pixel number of plants (or a plant) from an image, a csv file including the values, and processed (binary) images in the directory
 
Instruction to fill parameters:           
Parameter 1 and 2) The first two values, set the lower and upper boundaries of the pixel size of individual objects in the image that are 
                   included in the pixel count. This can be used to remove background noise. 
Parameter 3) This is a calibration to convert pixels to area. If you don't know that value yet (typical) leave this at 1 and convert later in Excel
Parameter 4) This is the format of your image. You can change jpg (default now) as any other format.
Parameter 5 and 6) They are the minimum and maximum values for adjusting threshold. 
          e.g.: minThr = 20 + np.argmin(Hist[20:90]); 20 is an example minimum value when the background is dark
          Users can change the values to find the best values for images (see line 37 for the detail); No change 90 unless your canopy is very bright 
Parameter 7) The name of output file (only csv format allowed) that writes all numbers getting from the program
Parameter 8) This is where you can specify the folder with your images. The simple solution is to always put your images in the same folder,
             analyze them, and then move them to a permamanet folder. That way, you do not need to ever change the program itself.
             *This program requies '/' for directory, although directory in Window uses '\'. 

 
ONLY A FEW PARAMETERS SHOULD BE ADJUST BY USERS. ALL NEAR THE BOTTOM OF THE PROGRAM:
    IN PxEx(0, 3000000, 1, '/*.jpg', 20, 90, 'C:/Pics/Canopy/test.csv', 'C:/Pics/Canopy') (line 141) 
    THE FIRST AND SECOND PARAMETER ARE MINIMUM AND MAXIMUM PIXEL NUMBER TO BE ANALYZED IN THE PROGRAM. 
    THE 3RD VALUE IS A CALIBRATION FACTOR (PIXEL SIZE OF A KNOWN DISTANCE) TO CONVERT PIXELS TO AREA, 
    THE 4TH PARAMETER IS FORMAT OF IMAGES THAT USER HAVE TO SPECIFY THE EXTENSION OF YOUR IMAGES (Note: that JPEG and JPG are different!),
    THE 5TH and 6TH VALUES ARE VALUES TO GET MINIMUM PIXEL INTENSITY (See the pragraph in line 37 to change the default values),
        C:/Pics/Canopy/test.csv IS THE NAME OF THE OUTPUT FILE (ONLY CSV FORMAT ALLOWED IN THE PROGRAM),
        AND C:/Pics/Canopy IS THE FOLDER THAT CONTAINS THE IMAGES. NOTE: VERY LONG FOLDER NAMES MAY CAUSE PROBLEMS!
    THE PIXEL INTENSITY RANGE MAY NEED TO BE ADJUSTED TO LOOK FOR THE OPTIMAL THRESHOLD BETWEEN BACKGROUND AND CANOPY
    THE BEST RANGE DEPENDS ON PICTURE QUALITY. IF THE BACKGROUND IS VERY DARK TO MINIMUM VALUE (50 IS THE EXAMPLE BELOW) MAY NEED TO BE LOWERED.  
    IF NEEDED, ADJUST THAT VALUE (line 141) IN BOTH INSTANCES IN THE INSTRUCTION BELOW. SO FAR I HAVE NOT SEEN EXAMPLES WHERE THE UPPER PART OF THE RANGE
    NEEDS TO BE ADJUSTED, BUT IF THE CANOPY IS VERY BRIGHT, THE '90' CAN BE INCREASEDE TO A HIGHER VALUE.
    WHETHER THE RANGE FOR THRESHOLDING NEEDS TO BE ADJUSTED CAN EASILY BE SEEN BY COMPARING THE ORIGINAL IMAGES WITH THE BINARY IMAGES THAT GET CREATED 
      (IN THE SAME FOLDER AS THE ORIGNAL IMAGES)
      e.g.) minThr = 50 + np.argmin(Hist[50:90]) 

     THE OUTPUT FILE GETS WRITTEN TO THE SAME DIRECTORY AS WHERE THE PROGRAM IS SAVED. NOT SURE HOW TO CHANGE THAT. OUTPUTY ALSO GETS WRITTEN TO CONSOLE (BOTTOM RIGHT WINDOW)
 
 
11/10/2020 Update: the program now automatically determines the optimal pixel intensity threshold to separate canopy from beackground. Background has low pixel intensity, canopy has a higher intensity.
The program now looks for a local minimum in the pixel intensity histogram in the intensity range from 20 to 90 (user adjustable in the line 141).

2/5/2021 Update: all parameters can be changed in the only one line (line 141) instead the middle of program.  
Whether the program works well can be easily checked using the binary canopy images that are created, as well as the pixel intensity histogram plot created in Python

2/9/2021 Update: Histogram plots of binary images will be generated as the output of the prgram. That values can be used to determine optimum threshold value for line 141

