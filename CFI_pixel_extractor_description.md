Description for Chlrophyll fluorescence image pixel extractor

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

11/10/2020 Update: the program now automatically determines the optimal pixel intensity threshold to separate canopy from beackground. Background has low pixel intensity, canopy has a higher intensity.
The program now looks for a local minimum in the pixel intensity histogram in the intensity range from 20 to 90 (user adjustable in the line 141).

2/5/2021 Update: all parameters can be changed in the only one line (line 141) instead the middle of program.  
Whether the program works well can be easily checked using the binary canopy images that are created, as well as the pixel intensity histogram plot created in Python

2/9/2021 Update: Histogram plots of binary images will be generated as the output of the prgram. That values can be used to determine optimum threshold value for line 141

