# Otsu's method

The project implements Otsu's method to perform automatic image thresholding. The code reads an image from the 'data' directory and then calculates the optimum threshold separating the two classes of pixels. The code then thresholds the image using the calculated threshold and displays the original and thresholded images.

> Otsu's method is used to perform automatic image thresholding. It is used to separate the foreground from the background of an image. The algorithm assumes that the image contains two classes of pixels following bi-modal histogram (foreground and background pixels), it then calculates the optimum threshold separating the two classes so that their combined spread (intra-class variance) is minimal.

## Note

Before running the code, make sure you have installed the required libraries. Also, add the image inside the 'data'. If you make a change to the image path and/or filename, make sure to update the code accordingly.
